#!/usr/bin/env python3
"""Read-only validation of film production evidence. See --help for usage."""

import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


LIMITATION = (
    "Validates recorded approvals, file provenance, media metadata and review coverage; "
    "cannot authenticate user approval, judge review observations, prove motion from "
    "metadata, detect falsely declared native framing, or determine whether a repair "
    "preserves approved intent. Human and audiovisual review remain required."
)
METHODS = {
    "identity": {"image_inspection", "playback"},
    "appearance": {"image_inspection", "playback"},
    "action": {"playback", "temporal_sequence"},
    "speech_content": {"listening", "transcription"},
    "audio_performance": {"listening"},
    "audiovisual_timing": {"audiovisual_playback"},
    "viewer_review": {"audiovisual_playback"},
}
STAGES = ("script", "mode", "characters", "storyboard")
SHA256 = re.compile(r"[a-fA-F0-9]{64}\Z")
ASPECT = re.compile(r"([1-9][0-9]*):([1-9][0-9]*)\Z")


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def probe_media(path, executable):
    """Return display dimensions and media type from ffprobe, not filename suffixes."""
    result = subprocess.run(
        [executable, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30,
    )
    if result.returncode:
        raise ValueError("ffprobe could not inspect the media: " + result.stderr.strip()[:300])
    data = json.loads(result.stdout)
    streams = [s for s in data.get("streams", []) if s.get("codec_type") == "video"
               and not s.get("disposition", {}).get("attached_pic")]
    if len(streams) != 1:
        raise ValueError("expected exactly one playable video/image stream")
    stream = streams[0]
    width, height = int(stream["width"]), int(stream["height"])
    if width <= 0 or height <= 0:
        raise ValueError("media dimensions must be positive")
    sar = stream.get("sample_aspect_ratio", "1:1")
    pixel_ratio = Fraction(sar.replace(":", "/")) if sar not in ("N/A", "0:1") else Fraction(1)
    if pixel_ratio <= 0:
        raise ValueError("invalid sample aspect ratio")
    display_width, display_height = Fraction(width) * pixel_ratio, Fraction(height)
    rotation = float(stream.get("tags", {}).get("rotate", 0))
    for side in stream.get("side_data_list", []):
        if "rotation" in side:
            rotation = float(side["rotation"])
    if not math.isfinite(rotation) or rotation % 90:
        raise ValueError("unsupported video rotation")
    if rotation % 180:
        display_width, display_height = display_height, display_width
    names = set(data.get("format", {}).get("format_name", "").split(","))
    image_formats = {"image2", "image2pipe", "png_pipe", "jpeg_pipe", "webp_pipe", "bmp_pipe",
                     "tiff_pipe", "ppm_pipe", "pgm_pipe", "avif", "heif"}
    frames = stream.get("nb_frames")
    duration = float(stream.get("duration", data.get("format", {}).get("duration", 0)))
    if not math.isfinite(duration) or duration < 0:
        raise ValueError("invalid media duration")
    is_still = frames == "1" or (bool(names & image_formats) and frames in (None, "N/A", "1"))
    if not is_still and duration <= 0:
        raise ValueError("video needs a positive duration; cannot verify this file as video")
    return {"ratio": display_width / display_height, "display_width": display_width,
            "display_height": display_height, "media_type": "still" if is_still else "video"}


def source_aspect_matches(media, target):
    """Allow at most one display pixel of source rounding; final exports stay exact."""
    if media["ratio"] == target:
        return True
    width, height = media.get("display_width"), media.get("display_height")
    if width is None or height is None:
        return False
    return abs(width - height * target) <= 1 or abs(height - width / target) <= 1


class Validator:
    def __init__(self, packet_path, phase, ffprobe="ffprobe"):
        self.base = Path(packet_path).resolve().parent
        self.phase = phase
        self.ffprobe = ffprobe
        self.errors = []
        self.hashes = {}
        self.probes = {}

    def fail(self, location, message):
        self.errors.append(f"{location}: {message}")

    def object(self, value, location):
        if not isinstance(value, dict):
            self.fail(location, "must be an object")
            return {}
        return value

    def array(self, value, location, required=False):
        if not isinstance(value, list):
            self.fail(location, "must be an array")
            return []
        if required and not value:
            self.fail(location, "must not be empty")
        return value

    def text(self, value, location):
        if not nonempty(value):
            self.fail(location, "must be a nonempty string")
            return False
        return True

    def choice(self, value, options, location):
        if not isinstance(value, str) or value not in options:
            self.fail(location, "must be one of " + ", ".join(sorted(options)))
            return False
        return True

    def ref(self, value, location):
        ref = self.object(value, location)
        valid_path = self.text(ref.get("path"), location + ".path")
        digest = ref.get("sha256")
        valid_hash = isinstance(digest, str) and SHA256.fullmatch(digest)
        if not valid_hash:
            self.fail(location + ".sha256", "must be a 64-character SHA-256 digest")
        if not valid_path or not valid_hash:
            return None
        try:
            path = (self.base / ref["path"]).resolve()
            if path not in self.hashes:
                with path.open("rb") as source:
                    self.hashes[path] = hashlib.file_digest(source, "sha256").hexdigest()
            if self.hashes[path] != digest.lower():
                self.fail(location, "stale sha256: file bytes differ from the recorded artifact")
            return (path, digest.lower())
        except (OSError, ValueError, RuntimeError) as exc:
            self.fail(location, "cannot read artifact: " + str(exc))
            return None

    def refs(self, value, location):
        found = set()
        for i, ref in enumerate(self.array(value, location)):
            key = self.ref(ref, f"{location}[{i}]")
            if key is not None:
                found.add(key)
        return found

    def probe(self, ref, location):
        if ref is None:
            return None
        path = ref[0]
        if path not in self.probes:
            try:
                self.probes[path] = probe_media(path, self.ffprobe)
            except (OSError, ValueError, KeyError, TypeError, AttributeError,
                    ZeroDivisionError, OverflowError, subprocess.SubprocessError) as exc:
                self.fail(location, "media verification failed: " + str(exc))
                self.probes[path] = None
        return self.probes[path]

    def checks(self, value, location, target, required, static_still=False):
        kinds = set()
        for i, item in enumerate(self.array(value, location, required=True)):
            loc = f"{location}[{i}]"
            check = self.object(item, loc)
            self.text(check.get("criterion"), loc + ".criterion")
            self.text(check.get("evidence"), loc + ".evidence")
            kind = check.get("kind")
            if self.choice(kind, METHODS, loc + ".kind"):
                kinds.add(kind)
                allowed = METHODS[kind] | ({"image_inspection"} if kind == "action" and static_still else set())
                self.choice(check.get("method"), allowed, loc + ".method")
            if check.get("status") != "pass":
                self.fail(loc + ".status", "must be pass; failed or unverified work is incomplete")
            if target is None or not isinstance(check.get("target_sha256"), str) or check["target_sha256"].lower() != target[1]:
                self.fail(loc + ".target_sha256", "review must target the selected file's current sha256")
        for kind in sorted(required - kinds):
            self.fail(location, "missing required " + kind + " review")

    def validate(self, packet):
        data = self.object(packet, "packet")
        if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
            self.fail("schema_version", "must be integer 1")
        self.text(data.get("scope"), "scope")
        contract = self.object(data.get("contract"), "contract")
        self.choice(contract.get("media_type"), {"video"}, "contract.media_type")
        self.choice(contract.get("framing"), {"native", "reframed"}, "contract.framing")
        aspect = contract.get("aspect_ratio")
        match = ASPECT.fullmatch(aspect) if isinstance(aspect, str) else None
        ratio = Fraction(int(match[1]), int(match[2])) if match else None
        if ratio is None:
            self.fail("contract.aspect_ratio", "must be a positive integer W:H ratio, such as 9:16")
        approvals = {}
        for i, item in enumerate(self.array(data.get("approvals"), "approvals")):
            loc = f"approvals[{i}]"
            approval = self.object(item, loc)
            stage = approval.get("stage")
            if not self.choice(stage, STAGES, loc + ".stage"):
                continue
            if stage in approvals:
                self.fail(loc + ".stage", "duplicate approval stage")
            self.choice(approval.get("status"), {"approved", "waived"}, loc + ".status")
            self.text(approval.get("evidence"), loc + ".evidence")
            refs = self.refs(approval.get("artifacts"), loc + ".artifacts")
            if approval.get("status") == "approved" and stage in {"script", "storyboard"} and not refs:
                self.fail(loc + ".artifacts", "approved script/storyboard needs its exact artifact")
            approvals[stage] = (approval.get("status"), refs)
        for stage in STAGES:
            if stage not in approvals:
                self.fail("approvals", "missing " + stage + " approval or explicit user waiver")
        ids = set()
        for i, item in enumerate(self.array(data.get("shots"), "shots", required=True)):
            loc = f"shots[{i}]"
            shot = self.object(item, loc)
            shot_id = shot.get("id")
            if self.text(shot_id, loc + ".id"):
                if shot_id in ids:
                    self.fail(loc + ".id", "duplicate shot id")
                ids.add(shot_id)
            board = self.ref(shot.get("board"), loc + ".board")
            identities = self.refs(shot.get("identity_refs"), loc + ".identity_refs")
            attachments = self.refs(shot.get("attachments"), loc + ".attachments")
            if board is not None and board not in attachments:
                self.fail(loc + ".attachments", "the actual selected uploads must include this shot's board")
            repair_source = None
            repair_valid = False
            if "board_repair" in shot:
                repair_loc = loc + ".board_repair"
                repair = self.object(shot["board_repair"], repair_loc)
                repair_source = self.ref(repair.get("approved_source"), repair_loc + ".approved_source")
                authorized = self.text(repair.get("authorization"), repair_loc + ".authorization")
                evidenced = self.text(repair.get("evidence"), repair_loc + ".evidence")
                repair_valid = authorized and evidenced and repair_source is not None
            status, approved = approvals.get("storyboard", (None, set()))
            if status == "approved" and board is not None and board not in approved:
                if not repair_valid or repair_source not in approved:
                    self.fail(loc, "storyboard refs are not covered by the approved artifacts or a documented restorative board repair")
            status, approved = approvals.get("characters", (None, set()))
            if status == "approved" and not identities <= approved:
                self.fail(loc, "characters refs are not covered by the approved artifacts")
            exceptions = self.object(shot.get("exceptions", {}), loc + ".exceptions")
            for key in exceptions:
                if key not in {"still", "reframe"}:
                    self.fail(loc + ".exceptions", "unknown exception: " + key)
                else:
                    self.text(exceptions[key], loc + ".exceptions." + key)
            board_media = self.probe(board, loc + ".board")
            if board_media:
                if board_media["media_type"] != "still":
                    self.fail(loc + ".board", "storyboard input must be an image")
                reframe_allowed = contract.get("framing") == "reframed" or nonempty(exceptions.get("reframe"))
                if ratio is not None and not source_aspect_matches(board_media, ratio) and not reframe_allowed:
                    self.fail(loc + ".board", "storyboard aspect ratio differs from contract; needs this shot's reframe approval")
            if identities:
                binding = self.object(shot.get("identity_binding"), loc + ".identity_binding")
                mode = binding.get("mode")
                self.choice(mode, {"attached", "verified_in_board"}, loc + ".identity_binding.mode")
                if mode == "attached" and not identities <= attachments:
                    self.fail(loc + ".attachments", "attached identity binding requires every identity ref in the actual uploads")
                if mode == "verified_in_board":
                    self.text(binding.get("evidence"), loc + ".identity_binding.evidence")
            intent = self.object(shot.get("intent"), loc + ".intent")
            for field in ("actor", "action", "end_state"):
                self.text(intent.get(field), loc + ".intent." + field)
            self.choice(intent.get("motion"), {"required", "static"}, loc + ".intent.motion")
            if self.phase == "delivery":
                self.selected(shot, loc, identities, intent, ratio, contract, exceptions)
        if self.phase == "delivery":
            delivery = self.object(data.get("delivery"), "delivery")
            ref = self.ref(delivery, "delivery")
            media = self.probe(ref, "delivery")
            if media:
                if media["media_type"] != "video":
                    self.fail("delivery", "final export must be an actual video")
                if ratio is not None and media["ratio"] != ratio:
                    self.fail("delivery", "final export aspect ratio differs from contract")
            self.checks(delivery.get("checks"), "delivery.checks", ref, {"viewer_review"})
        return self.errors

    def selected(self, shot, loc, identities, intent, ratio, contract, exceptions):
        selected = self.object(shot.get("selected"), loc + ".selected")
        ref = self.ref(selected, loc + ".selected")
        declared_type = selected.get("media_type")
        self.choice(declared_type, {"video", "still"}, loc + ".selected.media_type")
        self.choice(selected.get("framing"), {"native", "crop", "blur"}, loc + ".selected.framing")
        still_allowed = nonempty(exceptions.get("still"))
        reframe_allowed = contract.get("framing") == "reframed" or nonempty(exceptions.get("reframe"))
        if declared_type == "still" and not still_allowed:
            self.fail(loc + ".selected", "still substitution needs this shot's explicit user approval")
        if declared_type == "still" and intent.get("motion") == "required":
            self.fail(loc + ".intent.motion", "a still cannot fulfill required movement; revise the approved intent first")
        if contract.get("framing") == "native" and selected.get("framing") in {"crop", "blur"} and not reframe_allowed:
            self.fail(loc + ".selected.framing", "native contract needs this shot's explicit reframe approval")
        media = self.probe(ref, loc + ".selected")
        if media:
            if media["media_type"] != declared_type:
                self.fail(loc + ".selected.media_type", "declared media type differs from ffprobe evidence")
            if ratio is not None and not source_aspect_matches(media, ratio) and not reframe_allowed:
                self.fail(loc + ".selected", "source aspect ratio differs from contract; needs this shot's reframe approval")
        required = {"action"} | ({"identity"} if identities else set())
        static_still = declared_type == "still" and still_allowed and intent.get("motion") == "static"
        self.checks(shot.get("checks"), loc + ".checks", ref, required, static_still)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path, help="JSON packet; relative artifact paths are relative to this file")
    parser.add_argument("--phase", required=True, choices=("preflight", "delivery"))
    parser.add_argument("--ffprobe", default="ffprobe", help="ffprobe executable; required in both phases")
    args = parser.parse_args(argv)
    try:
        with args.packet.open("r", encoding="utf-8-sig") as source:
            packet = json.load(source)
        validator = Validator(args.packet, args.phase, args.ffprobe)
        errors = validator.validate(packet)
    except (OSError, ValueError, RuntimeError, RecursionError) as exc:
        errors = ["packet: could not read/validate JSON: " + str(exc)]
    print(json.dumps({"mechanical_checks_passed": not errors, "phase": args.phase, "errors": errors, "limitation": LIMITATION}, ensure_ascii=True, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
