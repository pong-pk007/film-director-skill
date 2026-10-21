# Post-edit covers, English audio, and subtitles

Read this guide when planning a complete film/episode delivery, finishing or revising its cut, or preparing its cover, English dub, or subtitles. It implements the reusable kit's default release package, stated when defining a new delivery scope. Apply the current user's narrower requests, cover style, languages, and story-specific choices first. Use the parent skill for creative review, providers, and browser operation; use [Loop Engineer](../../loop-engineer/SKILL.md) for bounded repairs and evidence.

## 1. Lock the actual delivery timeline

For each separately released episode/part, continue **finished cut → cover → English audio → subtitles/transcripts → package QA** without another start confirmation. Work episode by episode when the user requested that review cadence. Prepare derivative assets from accepted content; return only material story/design/voice changes to the relevant review stage.

Identify the current master from actual user decisions and the current edit record, not a filename containing `final`, newest modification time, or an obsolete script. Record its path, SHA-256, video duration, frame rate, aspect ratio, Thai audio source/hash and timeline mapping, episode ID/title, current review status, and established delivery folder. Include prepended hooks, silent openings, cutaways, pickups, repeated lines, and appended ghost dialogue. Time zero is the beginning of the delivered video; never add a memorized four-second offset across stories.

Store package work in the existing project layout, or `<episode>/release/<revision>/`. Link one `release-manifest.json` and `qa/release-checks.md` from the top current block of `production-status.md`. Use existing edit/voice records as sources instead of duplicating their authority. Plan these records early; create the cover and final English assets after the cut is finished.

An explicitly unfinished cut stays `review`; derivative files made for it are provisional. If a completed cut lacks perceptual verification, independent package work may continue, but release readiness remains unverified. Completing a package never approves the underlying film. This guide does not launch historical backfills, publish uploads, or create scheduled jobs. Each currently running production task must read the updated guide before relying on it.

**Exit:** Exact master and voice records are identified; current defects and approval scope are truthful; every downstream item has a known source revision.

## 2. Create the cover automatically

Use the imagegen skill and image-generation tool. Produce one selected cover for each released episode/part, using actual approved character/state references and frames from that episode. A multi-episode release gets distinct episode compositions with a coherent series title, lettering treatment, color family, and episode badge.

Default visual direction: **สไตล์การ์ตูนผีไทยเล่มละ 5 บาท** — hand-painted color over bold black brush/pen contours, expressive Thai faces, ink hatching, rough inexpensive print/paper texture, deep shadows, and a simple dramatic focal scene. Use Thai place, clothes, and objects from the story. Adapt the horror intensity to the film's actual tone; retain tenderness or comedy where appropriate. “Five-baht” describes the visual style, not an instruction to add a price or change the existing series name.

Build curiosity from a real episode event. Preserve cast identity, hair, wardrobe, props, age, and supernatural state. Show enough threat to invite viewing while preserving the episode's withheld reveal. A cover must not invent an event, duplicate a character, display a future transformation, or promise another episode's scene without authorization.

Set exact Thai series title, part/episode number, and existing episode title where useful. Favor a short title and large episode number over plot-summary copy. Render in the video's release aspect by default (9:16 for an existing portrait release); produce a different platform crop only when requested or already established. Keep text inside about 8% margins and clear of likely interface overlays; verify the actual platform layout when specified.

Inspect the actual generated image at full size and roughly 180–240 px thumbnail width: Thai spelling/vowels, episode number, title contrast, faces/hands, duplicate people, framing, and spoiler leakage. Repair defects through imagegen; for persistent lettering errors, use generated art with separately typeset exact text during normal cover layout. Retain the generated source, exact prompt, reference paths, selected export, and observations. Deliver PNG or high-quality JPEG; preserve an editable/lossless source if exported as JPEG.

**Exit:** A real, readable, episode-specific cover exists, its checks are recorded, and it matches the locked episode and series style. Deliver it without imposing an additional cover-selection round unless the user asked for one.

## 3. Build English speech against Thai timing

### Preserve the actual voices

Create English speech in **Google AI Studio inside Codex's in-app browser**, following the parent skill. Recover the exact original preset/voice ID for each speaking role, including narrator and ghost/character dialogue. Record provider, model, voice name/ID, speaker mapping, style instruction, available generation settings, pronunciation choices, and a reference sample from the accepted Thai performance. Reuse those identities and tonal qualities, adapting language instructions to natural English. “Same type” does not mean any similar male/female voice. Story-specific presets such as Riko or Gacrux are examples from prior work, not global defaults.

Verify visible settings and downloaded-source provenance for the actual generation. If the original preset or required bilingual capability is unavailable, mark that dependency blocked and continue independent packaging; obtain the user's choice before substituting another voice/provider. A UI rename or unavailable historical model requires verification and a recorded decision, not a guessed equivalence. Shared preset names alone do not prove that English sounds like the Thai performance.

### Translate by timed meaning units

Transcribe the speech actually present in the locked Thai export, checked against its source stems and accepted text. Include every speaking role, late pickup, and audible repeated line; reconcile ASR differences rather than blindly correcting the script to match a recognizer. Create a stable cue/anchor ID for every sentence or short dramatic beat, with Thai start/end, speaker, visible event window, intended English meaning, and critical reveal/contact/reaction points. Preserve purposeful silence and breaths as timing space.

Write concise, spoken English for each window. Preserve names, relationships, negation, agency, threat, tone, cultural meaning, and reveal order. Maintain a name/pronunciation glossary; phonetic TTS spellings belong in the generation script while canonical names belong in captions. Shorten wording without losing meaning. Semantic translation does not require equal word counts, and matching durations alone does not establish synchronization.

Pilot a demanding passage containing a short line, a long line, a meaningful pause, and a critical event. Then generate in scene/beat groups with enough context for consistent performance. Measure actual speech and place it at the Thai cue times. Prefer rewriting within the same meaning, directed regeneration, and editing genuine silence. Preserve complete syllables and natural phrasing. Use pitch-preserving local speed adjustment only after those measures, normally within 0.95–1.05× and only after listening confirms quality; never globally accelerate an episode to hide drift.

### Timing contract

These are project defaults chosen for this workflow, not claims about a platform standard. Record any stricter user requirement. A wider exception needs the user's specific scope and evidence; do not silently loosen tolerances or remove failing anchors.

| Check | Default acceptance |
| --- | --- |
| Time origin and silence | Drop English audio at video 0.000; preserve the actual opening/tail and all required pauses. |
| Lossless English timeline | Same duration as the locked video within one output frame. |
| Decoded delivery MP3 | Total duration difference at most 0.10 s, after accounting for encoder delay/padding. Check decoded speech timestamps, not just container duration. |
| Every matched sentence/beat | Absolute English–Thai start difference and end difference each at most 0.50 s; aim for 0.25 s or less. |
| Critical event/reveal/contact word | Difference from the corresponding Thai event anchor at most 0.20 s, and inside its intended visual beat. Mark these anchors before generation. |
| Meaning and picture | No premature reveal or late explanation after its relevant event; no unintended speech overlap or clipped words. |

Record each anchor's measured Thai and English start/end, signed differences, critical-word times where applicable, picture window, result, and evidence method. Report the maximum error, median error, and every failing/unverified anchor; averages cannot conceal an outlier. Check the opener, every sentence, all scene joins, each critical event, and the final word. ASR/forced alignment supplies estimates; inspect uncertain boundaries with the waveform and listening, and keep confidence limitations explicit. Sentence correspondence must cover the entire transcript, not a few favorable examples.

When the original Thai narration and picture conflict, record both timings and the exact conflict. Do not silently advance the English several seconds to fit the picture and claim it matches Thai. Repair English within the locked contract where possible; if satisfying both is impossible, present the affected timecodes and obtain the user's choice before changing accepted Thai audio/picture or permitting that timing exception. Continue unaffected episodes/assets.

### Export the actual deliverable

Keep an archival aligned PCM WAV at 48 kHz. Export a clean English speech stem as `.mp3`, normally 48 kHz / 256 kbps, including narrator and all translated character speech with original speaker identities and intended voice processing. Preserve timeline silence. Keep music/effects separate; label a combined alternate mix explicitly if it was requested. A speech stem placed over an intact Thai mix would double the dialogue: the handoff must state how to replace the Thai speech stem and retain music/effects. If only a mixed Thai master exists, disclose the missing separate stems instead of promising a clean replacement track.

Decode and inspect the exported MP3 itself. Check first/last syllables, clicks, clipping/true peaks, loudness consistency, encoding delay, words, timing, and voice continuity. Use listening for pronunciation, emotion, naturalness, and voice similarity; use continuous audiovisual review against the locked video for picture/speech timing. A local temporary review mux is allowed for this check and is not an unrequested final English video.

**Exit:** English MP3 exists, voice provenance and all measured timings pass, and content/performance/audiovisual checks have real evidence. Otherwise retain the files as a clearly marked review package with exact failures or missing modalities.

## 4. Export subtitles and transcripts from final audio

Default complete delivery includes **Thai SRT + TXT and English SRT + TXT**. Thai files follow the actual Thai master; English files follow the decoded final English MP3 on the same video time origin. `en.srt` means captions for the English dub. English translation subtitles intended for the Thai soundtrack are a separate optional asset with a name such as `en-for-th-audio.srt`; their timing must follow Thai, and they cannot silently replace dub captions.

Build captions after final audio alignment. Generate SRT and TXT from one corrected cue source per language so their words agree. Use the canonical spelling of names while preserving what was actually spoken; retain all spoken narrative/dialogue and relevant repetitions. Exclude directing prompts, unsaid script notes, invented ASR words, and sentences removed during editing. Include meaningful non-speech descriptions only under the chosen caption convention, consistently labeled; do not present them as dialogue.

SRT must be UTF-8 with sequential numeric cue IDs, `HH:MM:SS,mmm --> HH:MM:SS,mmm`, nonempty cue text, and blank separators. Times must be nonnegative, increasing, within the actual master, and start before end. Use at most two lines; split at readable semantic boundaries without separating Thai combining marks or a speaker's name. Ordinary cues should not overlap; combine genuinely simultaneous speakers clearly or record an intentional exception.

Aim for 1–6 s cues, at most about 42 displayed characters per line and about 17 English characters/s (20 maximum before repair), counting spaces. Treat very brief exclamations as explicit exceptions, not a reason to stretch subtitles over silence. Thai needs visual and reading review with Thai-aware text segmentation; English character-count heuristics alone cannot certify it. Match caption onset/end to the spoken phrase, generally within 0.20 s, while preserving readable grouping and scene/reveal timing. Split long cues before resorting to excessive reading speed.

The plain `.txt` files contain complete, readable, untimed transcripts of the same caption/spoken content for people and AI during upload. Keep production metadata, summaries, tags, and prompts out of these files. Also create `transcript-timed.txt` with a compact header (story/episode, master revision, language-to-audio mapping) and rows containing cue/anchor ID, speaker, Thai time range/text and English time range/text. This companion preserves meaning correspondence for AI without forcing identical Thai/English subtitle splits.

Parse every SRT, check numbering/timestamps/ranges/overlaps, compare normalized cue text with its plain TXT, and inspect rendered captions at representative opening, dense, dialogue, reveal, and ending passages. Verify actual speech coverage over the full timeline and every name/late pickup. UTF-8 readability, successful parsing, and matching text are mechanical checks; they do not prove timing, translation, or reading comfort.

**Exit:** Both languages have valid SRT and matching readable TXT tied to current audio, with no missing spoken sections; timed bilingual text and subtitle checks are present.

## 5. Package, verify, and resume safely

Reuse the user's established delivery folder and episode naming. Keep a consistent basename/revision across the package. Example layout (adapt names to the existing project):

```text
<story>_EP01_<revision>.mp4
<story>_EP01_<revision>_cover.png
ENG/<story>_EP01_<revision>.en.mp3
SUB/<story>_EP01_<revision>.th.srt
SUB/<story>_EP01_<revision>.en.srt
TXT/<story>_EP01_<revision>.th.txt
TXT/<story>_EP01_<revision>.en.txt
TXT/<story>_EP01_<revision>.transcript-timed.txt
release-manifest.json
qa/release-checks.md
```

The manifest is a release record, not a substitute for existing project sources. Record:

- `schema_version: 1`, scope/episode, revision, overall status (`pending`, `review`, `ready`, or `stale`), and current step/next action.
- Exact base video and Thai/English audio references (path + SHA-256), durations, time origin, frame rate, source edit/approval/voice-record links, and delivery folder.
- Every required asset's path, hash, language/purpose, source revision, and state (`pending`, `generated`, `verified`, `stale`, or `blocked`). Name an explicit user omission when an asset is outside scope.
- Voice mapping and observed provider settings, timing-table path and tolerances, measured maxima/median, failed/unverified cue IDs, review evidence, scoped user exceptions, and copied-file hash results.

For each required check, `qa/release-checks.md` records **pass / fail / unverified**, exact target file/hash, observed evidence/timecodes, and method. Cover visual/title/identity/spoiler review, translation completeness, voice provenance and listening, every-beat sync, full audiovisual review, MP3 decode/duration, subtitle parsing/text/reading/timing, and final-copy consistency are separate checks. A reviewer must have access to the modality being judged. A play button, ASR success, or another agent's unsupported assertion cannot establish heard speech or watched audiovisual rhythm.

Run the production packet's existing delivery check for the video and carry its unresolved findings into release status. Separately perform the checks above on the cover/MP3/text artifacts; the video checker does not implement them. Mark the release `ready` only when required files exist and open, required checks pass on current versions, and any applicable user review has been honored. Missing perception tools leave those checks unverified: provide a useful review package and disclose the limit, rather than implying readiness.

Before copying a package into the delivery folder, confirm the source master has not changed. Copy selected assets and check destination hashes. Preserve previous accepted versions. A ZIP is optional convenience and must contain the current selected files; it does not replace accessible individual files. Handoff links to the cover, MP3, SRT/TXT folder, states that English starts at video zero, explains speech-stem use, and identifies any exact remaining checks. Uploading/publishing is a separate user action unless explicitly requested.

On resume, compare recorded hashes with actual current sources and reuse verified work only while its dependencies remain valid. A cut/Thai-audio change invalidates English timing, captions, transcripts, and associated QA; a new English take invalidates English caption/timing/listening checks. A cover-only change invalidates its own visual/text checks. Recheck unaffected cover content against a new master and record why it still applies. Update the current block and manifest rather than creating contradictory `final` records. Stop rerendering passed assets without a changed dependency or new defect.

**Exit:** The current complete package is delivered and evidenced, or the review handoff explicitly names what prevents completion. The agent has not stopped merely because an MP4 or MP3 file was created.
