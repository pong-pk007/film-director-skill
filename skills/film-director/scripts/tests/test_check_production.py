"""Regression cases for production substitutions and overstated QA evidence."""

import copy
import hashlib
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "check_production.py"
SPEC = importlib.util.spec_from_file_location("check_production", MODULE_PATH)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class PacketTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.packet_path = self.root / "packet.json"
        self.refs = {}
        for name in ("script.txt", "board.png", "identity.png", "take.mp4", "final.mp4", "still.png"):
            content = name.encode()
            (self.root / name).write_bytes(content)
            self.refs[name] = {"path": name, "sha256": hashlib.sha256(content).hexdigest()}
        self.packet = {
            "schema_version": 1,
            "scope": "Episode 1 / shot 1",
            "contract": {"media_type": "video", "aspect_ratio": "9:16", "framing": "native"},
            "approvals": [
                {"stage": stage, "status": "approved", "evidence": "User turn 12: approve this version",
                 "artifacts": [self.refs[filename]] if filename else []}
                for stage, filename in (("script", "script.txt"), ("mode", None),
                                        ("characters", "identity.png"), ("storyboard", "board.png"))
            ],
            "shots": [{
                "id": "S01", "board": self.refs["board.png"],
                "identity_refs": [self.refs["identity.png"]],
                "attachments": [self.refs["board.png"], self.refs["identity.png"]],
                "identity_binding": {"mode": "attached"},
                "intent": {"actor": "Pee", "action": "walk to the door", "end_state": "outside", "motion": "required"},
                "selected": dict(self.refs["take.mp4"], media_type="video", framing="native"),
                "checks": [self.check("action", "playback"), self.check("identity", "image_inspection")],
            }],
            "delivery": dict(self.refs["final.mp4"], checks=[self.check("viewer_review", "audiovisual_playback", "final.mp4")]),
        }
        self.metadata = {
            name: {"ratio": Fraction(9, 16), "media_type": "still" if name.endswith("png") else "video"}
            for name in self.refs
        }

    def check(self, kind, method, filename="take.mp4"):
        return {"criterion": "Visible approved event", "kind": kind, "status": "pass", "method": method,
                "evidence": "Reviewed actual target at 00:02; end state visible",
                "target_sha256": self.refs[filename]["sha256"]}

    def errors(self, phase="delivery"):
        with patch.object(checker, "probe_media", side_effect=lambda path, _: self.metadata[path.name]):
            return checker.Validator(self.packet_path, phase).validate(self.packet)

    def assertError(self, fragment, phase="delivery"):
        errors = self.errors(phase)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_valid_packet_and_preflight_without_outputs(self):
        self.assertEqual([], self.errors())
        del self.packet["shots"][0]["selected"]
        del self.packet["shots"][0]["checks"]
        del self.packet["delivery"]
        self.assertEqual([], self.errors("preflight"))

    def test_board_must_be_in_actual_uploads(self):
        self.packet["shots"][0]["attachments"] = [self.refs["identity.png"]]
        self.assertError("must include this shot's board", "preflight")

    def test_changed_approved_file_is_stale(self):
        (self.root / "script.txt").write_text("unreviewed revision")
        self.assertError("stale sha256", "preflight")

    def test_horizontal_board_blocked_before_generation(self):
        self.metadata["board.png"]["ratio"] = Fraction(16, 9)
        self.assertError("storyboard aspect ratio differs", "preflight")

    def test_landscape_generated_source_cannot_pass_native_ratio(self):
        self.metadata["take.mp4"]["ratio"] = Fraction(16, 9)
        self.assertError("source aspect ratio differs")

    def test_one_pixel_source_rounding_passes_but_final_ratio_stays_exact(self):
        dimensions = {"ratio": Fraction(941, 1672), "display_width": Fraction(941), "display_height": Fraction(1672)}
        self.metadata["board.png"].update(dimensions)
        self.metadata["take.mp4"].update(dimensions)
        self.assertEqual([], self.errors("preflight"))
        self.assertEqual([], self.errors())
        self.metadata["final.mp4"].update(dimensions)
        self.assertError("final export aspect ratio differs")

    def test_pixel_tolerance_rejects_landscape_and_two_by_three_sources(self):
        for width, height in ((1920, 1080), (1024, 1536)):
            with self.subTest(dimensions=(width, height)):
                dimensions = {"ratio": Fraction(width, height), "display_width": Fraction(width), "display_height": Fraction(height)}
                self.metadata["board.png"].update(dimensions)
                self.metadata["take.mp4"].update(dimensions)
                self.assertError("storyboard aspect ratio differs", "preflight")
                self.assertError("source aspect ratio differs")

    def test_near_ratio_without_display_dimensions_has_no_rounding_allowance(self):
        self.metadata["board.png"]["ratio"] = Fraction(941, 1672)
        self.assertError("storyboard aspect ratio differs", "preflight")

    def test_reframe_exception_cannot_waive_final_export_ratio(self):
        self.metadata["take.mp4"]["ratio"] = Fraction(16, 9)
        self.packet["shots"][0]["exceptions"] = {"reframe": "User turn 15: crop S01 to portrait"}
        self.assertEqual([], self.errors())
        self.metadata["final.mp4"]["ratio"] = Fraction(16, 9)
        self.assertError("final export aspect ratio differs")

    def test_reframed_contract_allows_source_ratios_but_final_must_match(self):
        self.packet["contract"]["framing"] = "reframed"
        self.metadata["board.png"]["ratio"] = Fraction(16, 9)
        self.metadata["take.mp4"]["ratio"] = Fraction(16, 9)
        self.packet["shots"][0]["selected"]["framing"] = "crop"
        self.assertEqual([], self.errors("preflight"))
        self.assertEqual([], self.errors())
        self.metadata["final.mp4"]["ratio"] = Fraction(16, 9)
        self.assertError("final export aspect ratio differs")

    def test_crop_or_blur_under_native_contract_needs_specific_approval(self):
        for framing in ("crop", "blur"):
            with self.subTest(framing=framing):
                self.packet["shots"][0]["selected"]["framing"] = framing
                self.assertError("native contract needs this shot's explicit reframe approval")

    def make_still(self):
        shot = self.packet["shots"][0]
        shot["selected"] = dict(self.refs["still.png"], media_type="still", framing="native")
        shot["intent"] = {"actor": "Pee", "action": "stand beside the door", "end_state": "still beside door", "motion": "static"}
        shot["checks"] = [self.check("action", "image_inspection", "still.png"),
                          self.check("identity", "image_inspection", "still.png")]
        return shot

    def test_still_exception_is_scoped_to_shot(self):
        second = copy.deepcopy(self.packet["shots"][0])
        second.update(id="S02", exceptions={"still": "User turn 15: S02 may use a still"})
        self.packet["shots"].append(second)
        self.make_still()
        self.assertError("still substitution needs this shot's explicit user approval")

    def test_explicit_static_still_can_pass_without_claiming_motion(self):
        shot = self.make_still()
        shot["exceptions"] = {"still": "User turn 15: S01 may be a static image"}
        self.assertEqual([], self.errors())
        shot["intent"]["motion"] = "required"
        self.assertError("a still cannot fulfill required movement")
        self.assertError("checks[0].method")

    def test_static_inspection_cannot_certify_action_in_video(self):
        self.packet["shots"][0]["checks"][0]["method"] = "image_inspection"
        self.assertError("checks[0].method")

    def test_failed_or_unverified_check_blocks_completion(self):
        for status in ("fail", "unverified"):
            with self.subTest(status=status):
                self.packet["shots"][0]["checks"][0]["status"] = status
                self.assertError("failed or unverified work is incomplete")

    def test_transcript_cannot_certify_audio_performance(self):
        self.packet["shots"][0]["checks"].append(self.check("audio_performance", "transcription"))
        self.assertError("checks[2].method")

    def test_old_review_hash_rejected_even_when_selected_file_is_fresh(self):
        self.packet["shots"][0]["checks"][0]["target_sha256"] = "a" * 64
        self.assertError("review must target the selected file's current sha256")

    def test_single_image_generator_can_bind_identity_through_reviewed_board(self):
        shot = self.packet["shots"][0]
        shot["attachments"] = [self.refs["board.png"]]
        shot["identity_binding"] = {"mode": "verified_in_board", "evidence": "Compared board to approved identity; face, hair and clothing match"}
        self.assertEqual([], self.errors())
        shot["identity_binding"]["evidence"] = " "
        self.assertError("identity_binding.evidence", "preflight")

    def test_required_reviews_cannot_be_omitted(self):
        self.packet["shots"][0]["checks"] = []
        self.packet["delivery"]["checks"] = []
        self.assertError("missing required action review")
        self.assertError("missing required identity review")
        self.assertError("missing required viewer_review review")

    def test_waiver_evidence_and_approved_membership(self):
        approval = self.packet["approvals"][3]
        approval["artifacts"] = [self.refs["identity.png"]]
        self.assertError("storyboard refs are not covered", "preflight")
        approval.update(status="waived", evidence="User turn 18 explicitly waived storyboard review")
        self.assertEqual([], self.errors("preflight"))
        approval["evidence"] = ""
        self.assertError("evidence", "preflight")

    def make_board_repair(self):
        content = b"restored approved neck proportions and removed annotation"
        (self.root / "board_repaired.png").write_bytes(content)
        repaired = {"path": "board_repaired.png", "sha256": hashlib.sha256(content).hexdigest()}
        self.metadata["board_repaired.png"] = {"ratio": Fraction(9, 16), "media_type": "still"}
        shot = self.packet["shots"][0]
        shot["board"] = repaired
        shot["attachments"][0] = repaired
        shot["board_repair"] = {
            "approved_source": self.refs["board.png"],
            "authorization": "Existing production authorization permits restoration of the approved character without another design choice",
            "evidence": "Compared both boards: restored approved neck proportions and removed labels; action, design and reveal unchanged",
        }
        return shot

    def test_restorative_board_repair_preserves_approved_source_binding(self):
        self.make_board_repair()
        self.assertEqual([], self.errors("preflight"))
        self.assertEqual([], self.errors())

    def test_board_repair_needs_authorization_and_comparison_evidence(self):
        shot = self.make_board_repair()
        valid_repair = copy.deepcopy(shot["board_repair"])
        for field in ("authorization", "evidence"):
            with self.subTest(field=field):
                shot["board_repair"] = copy.deepcopy(valid_repair)
                del shot["board_repair"][field]
                self.assertError("board_repair." + field, "preflight")
                self.assertError("storyboard refs are not covered", "preflight")

    def test_board_repair_source_must_be_approved_and_current(self):
        shot = self.make_board_repair()
        shot["board_repair"]["approved_source"] = self.refs["identity.png"]
        self.assertError("storyboard refs are not covered", "preflight")
        shot["board_repair"]["approved_source"] = self.refs["board.png"]
        (self.root / "board.png").write_bytes(b"changed after approval")
        self.assertError("board_repair.approved_source: stale sha256", "preflight")

    def test_board_repair_cannot_bypass_canonical_identity_approval(self):
        shot = self.make_board_repair()
        shot["identity_refs"] = [self.refs["still.png"]]
        shot["attachments"].append(self.refs["still.png"])
        self.assertError("characters refs are not covered", "preflight")

    def test_duplicate_id_and_missing_ref_fail_cleanly(self):
        self.packet["shots"].append(copy.deepcopy(self.packet["shots"][0]))
        (self.root / "identity.png").unlink()
        self.assertError("duplicate shot id", "preflight")
        self.assertError("cannot read artifact", "preflight")

    def test_declaring_still_as_video_does_not_pass(self):
        self.metadata["take.mp4"]["media_type"] = "still"
        self.assertError("declared media type differs")

    def test_no_character_stage_needs_no_artifact_or_binding(self):
        shot = self.packet["shots"][0]
        shot["identity_refs"] = []
        del shot["identity_binding"]
        self.packet["approvals"][2]["artifacts"] = []
        self.assertEqual([], self.errors())

    def test_missing_ffprobe_is_json_error_without_traceback(self):
        self.packet_path.write_text(json.dumps(self.packet), encoding="utf-8")
        output = io.StringIO()
        with patch.object(checker, "probe_media", side_effect=FileNotFoundError("ffprobe unavailable")), redirect_stdout(output):
            result = checker.main([str(self.packet_path), "--phase", "preflight"])
        payload = json.loads(output.getvalue())
        self.assertEqual(1, result)
        self.assertFalse(payload["mechanical_checks_passed"])
        self.assertIn("ffprobe unavailable", payload["errors"][0])
        self.assertIn("cannot authenticate user approval", payload["limitation"])

    def test_unicode_error_paths_are_safe_on_windows_ascii_stdout(self):
        self.packet["shots"][0]["board"]["path"] = "ภาพที่หาย.png"
        self.packet_path.write_text(json.dumps(self.packet), encoding="utf-8")
        output = io.StringIO()
        with redirect_stdout(output):
            result = checker.main([str(self.packet_path), "--phase", "preflight"])
        self.assertEqual(1, result)
        output.getvalue().encode("ascii")
        self.assertTrue(any("ภาพที่หาย.png" in error for error in json.loads(output.getvalue())["errors"]))

    def test_bad_json_and_missing_fields_fail_without_traceback(self):
        for content in ("{oops", "{}", "[]", "null", '{"schema_version":true,"shots":[null]}'):
            with self.subTest(content=content):
                self.packet_path.write_text(content, encoding="utf-8")
                output = io.StringIO()
                with redirect_stdout(output):
                    self.assertEqual(1, checker.main([str(self.packet_path), "--phase", "preflight"]))
                self.assertTrue(json.loads(output.getvalue())["errors"])


class ProbeTests(unittest.TestCase):
    def probe(self, stream, format_info):
        result = subprocess.CompletedProcess([], 0, stdout=json.dumps({"streams": [stream], "format": format_info}), stderr="")
        with patch.object(checker.subprocess, "run", return_value=result) as run:
            media = checker.probe_media(Path("file with spaces.mp4"), "ffprobe")
        self.assertFalse(run.call_args.kwargs.get("shell", False))
        return media

    def test_rotation_display_ratio_and_real_image_classification(self):
        media = self.probe({"codec_type": "video", "width": 1920, "height": 1080, "duration": "2.0", "nb_frames": "48",
                            "side_data_list": [{"rotation": -90}]}, {"format_name": "mov,mp4"})
        self.assertEqual({"ratio": Fraction(9, 16), "display_width": Fraction(1080),
                          "display_height": Fraction(1920), "media_type": "video"}, media)
        media = self.probe({"codec_type": "video", "width": 1080, "height": 1920}, {"format_name": "png_pipe"})
        self.assertEqual("still", media["media_type"])

    def test_rounding_uses_dimensions_after_sar_and_rotation(self):
        media = self.probe({"codec_type": "video", "width": 836, "height": 941, "sample_aspect_ratio": "2:1",
                            "duration": "2.0", "nb_frames": "48", "side_data_list": [{"rotation": 90}]},
                           {"format_name": "mov,mp4"})
        self.assertEqual((Fraction(941), Fraction(1672)), (media["display_width"], media["display_height"]))
        self.assertTrue(checker.source_aspect_matches(media, Fraction(9, 16)))

    def test_audio_cover_art_is_not_a_video(self):
        with self.assertRaisesRegex(ValueError, "playable video/image"):
            self.probe({"codec_type": "video", "width": 1080, "height": 1920, "disposition": {"attached_pic": 1}}, {"format_name": "mp3"})


if __name__ == "__main__":
    unittest.main()
