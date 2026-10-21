# Production packet and mechanical checker

Use one current JSON packet per production episode or batch. Build it from actual user decisions and files after the review stages; do not fabricate approvals to fill fields. Link it from the current project status. This is a small execution record, not a second script or a replacement for the existing take/edit manifest.

Resolve `scripts/check_production.py` from the film-director skill directory. Run with Python 3.11+ and ffprobe on PATH, or pass its executable through `--ffprobe`. On Windows, `-X utf8` avoids locale-dependent text decoding.

```powershell
python -X utf8 skills/film-director/scripts/check_production.py /path/to/project/preproduction/production-packet.json --phase preflight
python -X utf8 skills/film-director/scripts/check_production.py /path/to/project/preproduction/production-packet.json --phase delivery
```

Exit 0 and `mechanical_checks_passed: true` mean the recorded mechanical requirements passed. Exit 1 lists errors. Neither result proves artistic quality, truthful observations, actual user intent, or that a file declared native was generated natively. The owner must verify those facts from real artifacts, provider history, and user messages. Both phases inspect actual storyboard dimensions, so ffprobe is required before a production submission too. Source images/clips allow at most one displayed pixel of aspect-ratio rounding; final exports require the exact target ratio. Display dimensions account for pixel aspect and rotation.

## Fields

A **ref** is `{"path":"path to the actual file","sha256":"64 hexadecimal characters"}`. Relative paths resolve from the packet's directory. Compute the digest from the actual bytes, for example with `Get-FileHash -Algorithm SHA256`; preserve approved source files rather than overwriting them. Every referenced file must exist and match its recorded digest.

| Field | Required content |
| --- | --- |
| `schema_version` | Integer `1`. |
| `scope` | Identifiable episode/batch and current revision. |
| `contract` | `media_type: "video"`, `aspect_ratio: "W:H"` such as `9:16`, `framing: "native"` or `"reframed"`, based on the user's requirements. |
| `approvals` | Four records for stages `script`, `mode`, `characters`, and `storyboard`. |
| `shots` | Nonempty array of the shots in this packet. IDs must be unique. |
| `delivery` | Required in delivery phase: a ref to the actual export plus its `checks`. |

Each approval record has `stage`, `status` (`approved` or `waived`), `evidence`, and `artifacts` (array of refs). Evidence identifies the actual user reply/quote and its scope. A waiver must be explicit. Approved script and storyboard stages need exact artifacts. Mode may have an empty artifact list; characters may be empty only when no characters are needed. Record the chosen mode in project state and its approval evidence. Canonical character references in a shot must belong to the approved character artifacts.

Keep other film requirements—voice/provider, period/wardrobe/props, character knowledge, sound, and take ranges—in the linked current shot list or manifest. These require the directing checks in the production guide; the checker does not infer them from pixels or prose.

That linked record also carries each release's opening plan: 0.00–3.00-second shot IDs and beats, viewer question, story payoff, and intended audio. At delivery, bind the opening review and timecodes to the current export's checks, using the observation methods below. It may be a clearly identified portion of `viewer_review`; a separate field or schema revision is unnecessary. The checker does not judge whether an opening is interesting or whether audiences stayed.

## Per-shot preflight

Each shot has:
- `id`, `board` (ref), `identity_refs` (array of canonical refs), and `attachments` (array of actual selected upload refs). The board must be among the actual attachments.
- `identity_binding` when identity refs exist: `{"mode":"attached"}` requires them in the upload list. For a single-image provider, use `{"mode":"verified_in_board","evidence":"actual comparison of the board against the selected identity/state"}`. Do the comparison; do not merely write the phrase.
- `intent`: strings `actor`, `action`, `end_state`, and `motion` (`required` or `static`). Include the object/target in the action when relevant. Static intent describes an accepted still moment, not a way to relabel a missing movement.

Normally the board must be among approved storyboard artifacts. For a technical repair that restores accepted intent, preserve the original approval and record:

```json
"board_repair": {
  "approved_source": {"path": "original approved board", "sha256": "original file digest"},
  "authorization": "Actual repair request or existing authorized repair scope",
  "evidence": "Observed comparison explaining how the new board restores the accepted event and identity"
}
```

The approved source must match an approved storyboard artifact and its current bytes. The new board still needs its own digest, attachment, and aspect checks. This binding does not approve changed events, a new identity, or new reveal timing; those follow the parent skill's review rules. It prevents a purely restorative repair from creating an unnecessary new approval stage.

Optional `exceptions` is a shot-local object with `still` and/or `reframe`, each containing actual explicit user authorization. A still exception applies only to that shot and the accepted duration/use recorded in the edit manifest. A reframe exception permits this shot's source/board ratio or crop/blur treatment under a native contract. A user-approved `reframed` contract already permits source reframing; the final export must always match the contract's target ratio.

Preflight does not need output takes or completed review checks. Include the shots about to be submitted, and retain historical submission packets if the current batch later changes. A whole-batch preflight is reusable only while all relevant file hashes, attachments, scope, and settings remain the same.

## Selected takes and delivery checks

In delivery phase, every shot also needs:
- `selected`: a ref to the actual selected provider source (or explicitly accepted still), with `media_type: "video"` or `"still"`, and `framing: "native"`, `"crop"`, or `"blur"`. Keep actual provider source dimensions and provenance traceable even if editing later changes the canvas.
- `checks`: nonempty array of checks against that selected file. Every shot requires an `action` check; shots with identity refs also require an `identity` check. Add speech, performance, or timing checks wherever the accepted requirements depend on them.

Each check has `criterion`, `kind`, `status`, `method`, `evidence`, and `target_sha256`. Evidence states the actual observation and timecode/range, or links the actual observation record. The target digest must match the selected source for a shot check, or the final export for a delivery check. Compare selected take ranges and their cut boundaries, and identify those ranges in the evidence.

| Kind | Accepted methods |
| --- | --- |
| `identity`, `appearance` | `image_inspection`, `playback` |
| `action` | `playback`, `temporal_sequence` |
| `speech_content` | `listening`, `transcription` |
| `audio_performance` | `listening` |
| `audiovisual_timing`, `viewer_review` | `audiovisual_playback` |

An explicitly accepted still with `intent.motion: "static"` may use `image_inspection` for its action check. A still cannot pass an intended movement. The production guide defines what each observation method can establish; merely naming a method is not evidence it occurred.

Record `status` as `pass`, `fail`, or `unverified`. All recorded checks must be pass to pass the delivery checker. Keep failed/unverified observations truthful while repairing; do not delete a criterion or change its intent to obtain a passing result. An unverified check can name its missing observation method as evidence, but remains unverified.

The top-level `delivery` ref points to the actual combined export and includes `checks` with at least a `viewer_review` against that export's digest. A changed source or export invalidates reviews bound to its old digest. Recheck affected content and integration before recording a new pass.

A review copy can still be handed off when this completion check fails, provided the handoff names the unresolved criteria and does not claim completion. Technical decoding, audiovisual review, and story judgment remain required to the extent specified by the production guide; the checker itself probes metadata and validates the recorded evidence structure.

## Post-edit release binding

For complete film/episode deliveries, read [postproduction-guide.md](postproduction-guide.md). Add a top-level `release_manifest` ref to the current release manifest, and link it from project status. Keep `delivery` pointing to the actual video export. The release manifest binds the exact video/Thai audio revision to its cover, English MP3, subtitles, transcripts, and verification.

This is an additional workflow requirement, not a change to checker schema version 1: `check_production.py` does not enforce `release_manifest` or inspect those derivative assets. Run its existing checks and the release guide's separate file, timing, content, and perception checks. A passing video report does not establish a complete release package. After a cut or audio revision, mark affected package items stale and rebuild/recheck them as the release guide specifies; preserve earlier reports as history.
