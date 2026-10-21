---
name: film-director
description: Direct films and story-led videos through user-reviewed preproduction, production, and automatic post-edit covers, English dubbing, and subtitles. Use for film creation, continuation, creative repair, or film delivery packaging (ทำหนัง ทำคลิป บทหนัง สตอรี่บอร์ด ปกคลิป พากย์อังกฤษ ซับ). Exclude media conversion, video-player code, and standalone images outside a film.
---

# Film Director

This reusable kit supplies workflow defaults, not another user's approvals. The current user's brief, provider choices, delivery scope, tools, and budget take precedence. Resolve linked skills from the sibling folders in this kit. For provider order, identity-preserving repairs, bounded retries, and review-cut cadence, read [workflow.md](references/workflow.md) when starting production or repairing a shot.

Direct what the audience sees, knows, and feels. Preserve the user's story, approved designs, and intended delivery format through every production step. Write operational records in concise English when useful; keep the user's language, dialogue, names, and cultural context intact.

## Start or resume

Read this skill, the latest user instructions, and the project's current state before creating or revising film assets. Work only on the requested scope: a script request ends with a script; an episode request does not authorize the whole series.

Reuse the established project location, or use `output/<story>/preproduction/`. A new story gets a new project state. Carry over standing user preferences such as tools and workflow, while treating story-specific approvals, characters, and footage as belonging to their original project unless the user asks to reuse them.

Keep one current block at the top of `production-status.md`, followed by history:
- Current brief and delivery requirements, including aspect ratio and whether footage must be generated natively in that format.
- Accepted script, selected storytelling mode, character/state references, and accepted storyboard scope, each linked to the actual user reply and artifact version.
- Current corrections, production packet path/revision, unresolved criteria, and next permitted action.
- For an episode delivery: exact current master, original voice/settings per speaker, delivery folder, and release-package state/link. Keep picture completion distinct from package completion.

The record is an index of evidence, not approval itself. Reconcile conflicting records with actual user messages and files. Resume from the first unfinished requirement; an old file named final does not establish acceptance.

Carry forward these standing production preferences: a compelling visual opening within the first three seconds of every separately released episode or part, Google AI Studio narration, and web production inside Codex's in-app browser. Apply them to new work and the requested repair scope; changing this skill does not itself authorize recutting previously accepted films.

For multi-asset batches, production, or recurring defects, read [Loop Engineer](../loop-engineer/SKILL.md) and use its bounded iteration and model-routing rules. Use [production-guide.md](references/production-guide.md) when preparing a production packet, generating video/audio/music, editing, or checking a deliverable. Complete the appropriate user review stages first.

**Automatic post-edit continuation:** When planning a complete film/episode delivery, after its cut is finished, when revising a delivered master, or when asked for film covers/English audio/subtitles, read [postproduction-guide.md](references/postproduction-guide.md). The kit's default complete package continues through **finished cut → Thai five-baht ghost-comic cover → English MP3 using the original speaker voices and matched timing → Thai/English SRT and TXT → verified delivery package**. State these defaults when defining a new delivery scope; honor the current user's cover style, languages, narrower scope, and exceptions. Within that established scope, continue the derivative steps without a redundant start question. The reference owns file requirements, timing tolerances, review evidence, and revision handling.

A script-only, storyboard-only, or explicitly narrow asset request remains limited to that scope. An unfinished review cut retains its review status; do not call its package final. Updating this skill alone does not start backfilling old films. Apply the workflow when an authorized delivery task next runs; it is an in-task continuation, not a scheduler. Preserve existing preproduction reviews, episode-by-episode review instructions, and explicit user exceptions. Faithful translation, covers from accepted designs, and subtitle preparation need no additional creative approval; changed story, identity, reveal order, voice/provider, or locked Thai picture/sound uses the affected review rule.

## User review stages

The normal sequence is **script → storytelling mode → character choices → visual storyboard for the entire requested production scope → production**. Character and storyboard images are preproduction work permitted in their respective stages.

Approval applies to the version and scope the user has seen. A reply such as “โอเค” or “ทำต่อ” may advance from the work just presented; it does not approve unseen work at later stages. Reuse recorded selections and approvals without asking again. Within the same film or series, the established storytelling mode and shared character choices carry into later episodes unless the user limited their scope or changed them; new episode boards still need their own review. Silence is not approval.

An explicit user instruction can change or waive a stage. Record the exact instruction and affected scope. A general request to make a film or an available generation tool does not waive review stages. When a decision is required, first finish and show the artifact the user can actually judge, then ask only for the missing decision. Explain the requirement with a link to this skill and the relevant rule.

### 1. Script

Extract the story, audience, duration, tone, ending, and required elements. If the brief is sufficient, write the script immediately. Ask only about missing information that materially changes the story.

Present a readable story with scenes, place/time, physical action, cause and effect, turns, ending, and necessary dialogue or narration samples. Each scene must change the situation, relationship, information, or feeling. Track what the audience and each character know separately: a reveal to the audience need not be a reveal to a character.

Identify each episode's opening 0.00–3.00 seconds in the script using the opening criteria below. Include it in the normal script review, not a separate approval round.

Before mode selection, ground the draft in events and action and mark the audio structure as undecided. Show the script before asking for the storytelling mode; both may be in the same response.

**Exit:** The user has seen and accepted an identifiable script version; requested story corrections are shown and resolved.

### 2. Storytelling mode

Offer both choices unless the user already selected one clearly:

| Choice | Story and sound |
| --- | --- |
| หนังเต็มรูปแบบ 100% | Characters act, speak, listen, and react within scenes. No default explanatory narrator. |
| เล่าด้วยเสียงบรรยาย มีโต้ตอบเล็กน้อย | Narration carries the story with brief dialogue at key moments; the images still contain events and performance. |

“Cinematic” alone does not select a mode. Adapt the script to the chosen mode, separating action, named speakers, narration, meaningful silence, and reactions. Show substantive changes to accepted story, key dialogue, or reveal timing for review. Formatting alone does not need renewed approval.

**Exit:** The selected mode is explicit and the production script matches the accepted content.

### 3. Character choices

Generate actual character-sheet images for important characters. Usually two or three meaningfully different options help selection; do not treat different poses of the same design as distinct options.

When editing supplied footage with an established cast, use clear frames from those clips as the identity references and review their intended use. Generate new character sheets only for new or redesigned characters; preserve the supplied cast within the requested edit.

Design from age, background, occupation, region, and period. Include useful face views, full body, wardrobe, and expressions. Use the imagegen skill and available image-generation tool for raster creation or editing. Descriptions alone are not reviewable character sheets.

Label choices clearly. Once selected, lock exact references for face, hair, age, proportions, clothes, and story-relevant possessions. Keep separate references for required time periods, costumes, or supernatural states. Display the identified approved design when resuming; propose new options only for new or requested changes.

**Exit:** The user has seen and chosen all important designs, and the exact selected files and state variants are traceable.

### 4. Visual storyboard

Generate actual storyboard images for every scene in the requested production scope using the accepted script and character references. Use the target aspect ratio. If unknown and consequential for framing, obtain that choice before generating the board batch.

Distinguish scenes (events in a place/time) from shots (camera views between cuts). Provide enough separate frames to show actions, reactions, and key transitions. If standalone shot images are requested, create or compose each actual shot as such; slicing a contact sheet is not a substitute when it reduces quality or changes composition. Contact sheets are review overviews.

For each shot, record its stable ID, approximate duration, actor and intention, visible start/action/end, camera and motivated movement, dialogue/narration, planned sound, cut, and audience/character knowledge at that point. Check direction, eyelines, positions, props, light, age/wardrobe, and reveal order across neighboring shots.

Choose shot duration for action and audience comprehension. A generator's eight- or ten-second limit determines production chunks, not the rhythm of every shot.

Mark which shot or shots cover each release's first three seconds. Make the focal action and question visible in the clean opening board and record the intended beat timing; a caption saying “hook” or “horror” is not the event.

Show the ordered overview and accessible separate images. Keep shot labels and review annotations outside the clean image sent to video generation. Resolve requested board corrections before dependent video, audio, music, or editing; those assets are not work to do while storyboard acceptance is pending.

**Exit:** The user has seen and accepted a specific complete board version for the requested scope, with no unresolved important scene corrections.

## Directing criteria

Apply these from script through selected take:

- **Point of view:** Know whose experience anchors the moment and which image changes the viewer's understanding or feeling. Motivate framing, concealment, and reveal.
- **Performance:** Give characters intention, hesitation, subtext, and filmable behavior. Let listeners react. Use silence, looks, and specific small actions rather than one stock expression per emotion.
- **World:** Maintain a coherent visual language, motivated light, period and regional detail, lived-in clothing and locations. Animation can use the same cinematic reasoning as live action.
- **Specificity:** Choose objects and spaces the story uses. Decorative graphics, neon, polish, or shallow focus do not replace story-specific imagery.
- **Sound:** Narration should add what images cannot carry efficiently. Space, distance, ambience, and silence help scenes feel inhabited.
- **Editing:** Cut for changed attention, action, or emotion. Allow perception and reaction. Repetition, slow motion, and held images need a story or explicitly accepted format reason; they are not filler for an overlong narration track.

Cinematic labels, 24 fps, letterboxing, grain, and color grading are not evidence that the scene works. Judge what happens and how the viewer receives it.

### Episode opening: the first three seconds

Give every separately released episode or part its own visual reason to keep watching, including installments that continue a cliffhanger. A viewer arriving without the previous part should recognize an immediate situation, even if its explanation comes later.

Specify the opening image, the visible change by 3.00 seconds, the question it creates, and where the accepted story pays that question off. A useful planning split is 0–1 seconds for a legible focal image and 1–3 seconds for a disturbing change, urgent action, contradiction, or reaction. This is a timing aid, not a requirement to cut every second or use a jump scare.

Start on the intriguing event. Put routine establishing shots, logos, titles, greetings, and recaps after that event, or integrate them without delaying it. A quiet opening works when a concrete anomaly or consequential action is already readable. Generic darkness, a slow zoom, or the word “หลอน” alone does not create a hook.

Choose the hook from the actual story. Keep withheld information withheld when the reveal matters; use a partial detail, consequence, or reaction instead of automatically showing the final ghost or twist. A flash-forward must make its return to the story understandable. The following shots must develop the opening's promise rather than reset into unrelated exposition.

Check that the visual situation remains intriguing with sound off, then use the chosen sound mode to sharpen it. Narration should enter with a specific event or question, not a generic introduction; a strong silent opening remains valid. Preserve the film's tone: horror can use restrained dread, empty space, and purposeful silence instead of festive lighting or constant loud stings.

Separate creative judgment from audience evidence. Record user-reported preference as such; claim retention or a causal improvement only when actual comparable audience data supports it. A successful reference teaches principles, not permission to copy its characters, plot, or approvals into another story.

## Production and repairs

Use **Google AI Studio for generated project audio, including narration and dialogue**. Generate actual speech with the selected voice; within an ongoing story or series retain the accepted narrator and settings unless changed by the user. For a new story, honor an explicit voice choice or choose a suitable available voice from the requested tone and record it; a tonal brief does not require another preset-selection approval unless the user reserves that choice. If the service is unavailable or cannot produce the required result, explain the limitation and obtain the user's choice before switching audio-generation providers. Reuse a recorded explicit provider override within its scope.

Run web production—such as Meta AI video, Google AI Studio speech, and an authorized Gemini music workflow—inside **Codex's in-app browser**, using the available browser-control tool and its current documentation. Keep routine work in background tabs so the user can work elsewhere. Reuse the correct logged-in tab; read its current state before acting and retain useful production/delivery tabs. A different browser, API, or speech engine requires the user's explicit choice rather than a silent fallback. Local file preparation, FFmpeg editing, and built-in image generation remain appropriate for their respective work.

After the required approvals, follow the production guide through actual generated footage, sound, editing, and verification. Use the user's chosen tools and authorized tier/budget.

Return only to the affected stage for creative changes: changed events may require script/board revision; changed identity requires its design and affected shots. Repairs that restore already accepted intent—such as an extra hand, folded neck, incorrect face, missed required format, timing, or a typo—proceed within existing authorization. Preserve accepted content and avoid asking the user to approve the same repair again.
