# Film production and verification

Use this guide after the required script, mode, character, and storyboard decisions are evidenced, or explicitly waived by the user for this scope. Follow [Loop Engineer](../../loop-engineer/SKILL.md) for iteration, retries, resources, and worker routing; the rules here define film-specific inputs and evidence.

## Bind production to the current work

Before the first submission, assemble a small production packet for the episode or batch using [production-packet.md](production-packet.md). Link it from the project's current `production-status.md`; keep that link on the current revision. Each episode or materially revised batch gets its own scope and current packet. Reuse existing manifests as source records rather than maintaining conflicting duplicate shot lists.

The packet and linked shot list must identify:
- Latest brief, exact production scope, accepted script/mode/board versions, selected character variants, and real user approval or scoped waiver evidence.
- Requested media type, output aspect ratio, native framing versus explicitly accepted reframing, chosen providers, and authorized quality/budget.
- Opening 0.00–3.00 seconds for each separately released episode/part: shot IDs, first image, visible change, viewer question, story payoff, and planned audio. Keep this in the linked shot/edit record.
- Per-shot board and identity references; period/age/hair/wardrobe/props; who can see or knows what; start state, actor/action/object, intended end state, and relevant sound.
- Actual selected attachments, provider job/download, chosen take and in/out, checks with evidence/timecodes, unresolved criteria, and next action.
- Original voice preset, provider/model, style/settings and speaker mapping; final edit timeline and retained speech/music/effects stems. These supply the automatic release workflow in [postproduction-guide.md](postproduction-guide.md).

A filename, copied approval label, or worker summary does not establish these facts. Inspect the linked messages and files. Changed content invalidates affected verification. Material creative changes return to the applicable user review stage; repairs restoring accepted intent reuse existing approval and record their approved source through the packet's `board_repair` binding.

Run the packet checker in **preflight** mode before generating the representative pilot, then before each submission with changed references or settings. Record actual attachments after choosing them in the provider, and keep them unchanged between the check and submission. Fix failures before that dependent submission.

## References, format, and generation

Use the approved shot board as actual image input for image-to-video. Attach applicable character/prop/state references when the provider supports them. For a single-image provider, first compare the board against the canonical references, repair identity or state differences, and record `verified_in_board` evidence. The board must itself bind the approved identity; merely naming a person in the prompt is insufficient. Record which inputs were actually sent.

For Meta AI, explicitly select and verify the current board plus compatible identity/state references for each new shot or retry; a previous chat attachment is not proof it remains an input. Use the current Codex in-app browser workflow required by the parent skill.

Choose references that agree: student and adult, ordinary and supernatural, or different wardrobe/prop states need distinct bindings. A normal face reference should not override an approved faceless state. Check the image after important movement as well as at its opening frame.

Lock the requested format in the clean board, provider setting, downloaded source, and final export. Distinguish **native generation** from **crop, blur-backed inset, or other reframing**. When native portrait is required, changing a landscape export's canvas does not satisfy the request. Check dimensions and visually inspect composition at the pilot stage before producing the rest.

For every animation request, describe the visible start state, motivated continuous action, and end state, plus character behavior, position/eyeline, camera, light, and invariants. Use observable verbs. Break complex events into shots if needed while preserving the accepted event. Timing targets must be checked in the result.

For Meta action shots, express the useful beats as short timed intervals, using per-second cues where they resolve ambiguity. In an opener, explicitly direct the first frame and what changes by three seconds. Keep one understandable action per interval. Numbered motion guides may supplement a clean board when needed, but labels/grids must stay outside the rendered film. Timing instructions are targets, not proof the generator followed them.

Complete one representative risky shot through real upload, generation, download, identity/action/format inspection, and selected trim before expanding a new workflow. A returned download must be matched to the correct shot; similar filenames or provider success banners are insufficient.

Validate the opening's usable motion before expanding a new episode batch. The opener can be the representative pilot; if the greatest production risk is elsewhere, check that shot as well. Favor a take that begins with the intended event and supplies clean editing handles.

Use selected ranges for film rhythm, not the generator's whole clip by default. Preserve direction, positions, props, listening/reaction, and reveal order across cuts. A trimmed take is usable when its chosen range still communicates the accepted event and joins coherently.

A ten-second take with five or six useful seconds may supply that shorter range. Cut off setup or later drift when the accepted action survives; repair missing story information rather than filling time with unusable frames.

Maintain the trace from board → actual input → provider result → selected trim → export. Keep rejected takes identifiable and unselected. Pending jobs remain pending until their actual result is known; use the loop's duplicate-submission and retry controls.

## Verify events and identity

Before selecting a take, inspect the requested outcome rather than only its appearance. Examples of observable criteria:
- A pulling action moves the intended person/object to the required position, or the accepted cut clearly communicates that movement.
- A door's locked/open state agrees across the action and the dialogue.
- A warning occurs with the intended speaker and listener in a comprehensible interaction.
- A supernatural reveal reaches only the audience or characters intended to know at that moment.

Evaluate action, identity/state, story information, and emotion separately. For each failure, record a timecode and likely cause, repair the smallest relevant source or trim, and recheck the affected cut. A held rope or a resisting actor alone does not demonstrate successful dragging. A recurring failed action remains failed when generation resources are exhausted.

Important story, identity, or reveal errors require repair or an explicit user-approved creative change. Minor differences may be retained only when consistent with the user's accepted tolerance and without changing the event or meaning. Missing evidence remains unverified.

## Dialogue, narration, and sound

Use Google AI Studio's speech interface inside Codex's in-app browser under the parent skill's provider rule. Confirm the visible service, selected voice, current model/settings, script, and result before download; a Gemini chat page or a local substitute is not evidence of AI Studio speech generation. Prepare a representative sample with difficult Thai words and the intended emotion before generating a new voice batch. Reuse the user's selected voice and accepted settings; do not copy another story's narrator by default.

For full-film mode, direct speech with intention, listening, breaths, pauses, and responses. For narrated mode, keep spoken phrasing, breathing room for action, and dialogue at meaningful moments. Off-screen speech is valid when staging establishes the speaker.

Keep add, remove, and replace requests distinct. Read the exact user wording and the affected audio before editing; if the intended change is materially ambiguous, clarify that part while continuing independent work. Preserve accepted stems outside the repair. A transcription that misses a reported sound does not disprove the user's observation.

Match speaker, words, pronunciation, emotional performance, timing, and spatial distance. Keep atmosphere across cuts and align doors, steps, fabric, and contact sounds with visible actions. Volume alone does not establish distance or performance.

Store provider/voice settings, actual script, source files, and selected trims. Verify the actual audio after mixing/export: source correctness does not prove the final mix retained it.

Keep a recoverable dialogue/narration stem and separate music/effects stems with their timeline offsets. Preserve the spoken text actually selected into the edit, including late pickups, ghost lines, and teaser dialogue; the preproduction script alone is not a final transcript. Retain pronunciation notes and an actual voice sample for later English localization.

Keep the opening line concise and aligned with the first visible event. Let silence and performance work when the image already carries the hook. Preserve breathing room and intelligibility rather than speeding the narrator up to force a duration.

## Music and editing

Place music, exits, and silence around changes in emotion and pressure. Keep speech intelligible and let performance carry its own meaning. Use chosen or supplied music for its intended scene function.

Build the cut from selected action and reaction. Adjust timing through legitimate shot selection and authorized script changes. Preserve the accepted event when choosing another angle or take; a substitution that changes the event or reveal returns to the affected review stage.

Check image and sound together at every important event, especially after replacing footage. What narration says is touched, attached, pulled, released, seen, or gone must agree with the cut's meaning. Intentional sound anticipation is allowed when the resulting sequence makes sense.

Generate footage that supplies a missing event instead of stretching unrelated clips to fill narration. Animatics, still inserts, flicker montages, and repeated frames are valid only within an explicitly accepted format or shot-specific fallback. Keep that exception scoped; it does not authorize stills throughout the film.

Place requested titles/subtitles in editing, maintaining readable safe areas around faces and actions.

## Verify each release's opening

Review the final export from 0.00 to at least 3.00 seconds and through its transition into the next beat, using the parent skill's opening criteria. Check each separately delivered part, not just the combined movie. Judge the exported cut, because trims, titles, fades, and sound edits can delay an otherwise good source opening.

Record the observed first image, when the intriguing action/change becomes legible, the viewer's question, and how the next beat carries it forward. First inspect the image without narration, then check the intended picture/sound relationship with the available modalities. Repair an opening that spends the whole window warming up, hides its focal action, promises an unrelated scene, or spoils a protected reveal.

Link the opening judgment and timecodes to the current export in the packet's delivery checks. This is an editorial judgment, not a predicted retention score. Apply the evidence limits below: sampled frames can support visible content; they cannot certify uninterrupted audiovisual rhythm. Mark any missing modality unverified rather than treating a played file or a checkmark as a review.

## Match claims to evidence

| Claim | Evidence that can support it | Limit |
| --- | --- | --- |
| File dimensions, duration, codec, integrity | Probe/decode of the actual file | Does not establish composition, identity, or meaning. |
| Identity, wardrobe, static composition | Compared full-size frames and canonical references | Does not certify every intermediate frame. |
| A specific movement or state transition | Playback or a sufficiently dense, ordered temporal sequence covering the event | A sparse contact sheet cannot certify motion quality or overall film rhythm. |
| Spoken words | Listening or transcription checked against the actual exported audio | Transcription does not certify singing, screams, tone, or naturalness. |
| Audio performance | Listening to the actual audio | Levels and transcripts are insufficient. |
| Audiovisual timing and viewer experience | Continuous audiovisual playback of the relevant cut/export through a tool that exposes both modalities | A playback button being pressed is not evidence that the agent perceived the content. |

Check available observation capabilities before committing to a large batch. Use tools that expose the required modality when available. If the environment lacks it, keep the criterion unverified and make the limitation visible; changing reviewer models or collecting more text-only opinions does not supply that evidence.

Give an independent reviewer the accepted requirements, references, and actual export, with a focused scope and without the creator's verdict. Require observations and timecodes. The owner resolves findings and verifies repairs.

## Check the actual delivery

Review the assembled export in two complementary passes:
1. **Viewer pass:** Follow the story and emotional rhythm through continuous image and sound. Check point of view, comprehension, performance, pauses, and reveal timing.
2. **Correctness pass:** Check identity/body/hands, age/wardrobe/props, speaker/words, necessary lip timing, contacts, sound effects, subtitles, aspect/composition, and playable file output.

After repair, recheck the altered region and its boundaries, plus export/integration properties affected by the change. Repeat broad checks only when new edits or evidence justify them.

Run the packet checker in **delivery** mode on the current selected sources and export. Mechanical success is necessary for the recorded delivery checks, but is not an artistic judgment or proof that supplied review claims are true. Inspect every error and preserve actual evidence for human/agent judgments.

For a complete episode delivery, finishing this export is the handoff to [postproduction-guide.md](postproduction-guide.md), not the end of the task. Read and execute that guide automatically before declaring the release package complete. The video packet checker does not validate covers, English MP3 timing, or SRT/TXT; record their actual checks separately and link them from the current packet/status. Keep failed or unverified film checks visible while preparing any provisional package.

Call the deliverable complete when requested files exist and open, critical criteria pass on the current versions, picture and sound communicate the accepted events, and required integration checks are evidenced. Otherwise deliver a clearly labeled review copy if useful, naming unresolved important defects and missing checks in the handoff itself. Do not turn a failed or unverified criterion into pass to obtain a clean validator result.

Keep source files, selected take ranges, matching script/board versions, and the exported master recoverable. Record verified repairs in current project state so the next episode and future resume retain them.
