# The Director’s Chair

A local Electron Mac filmmaking studio with five editable Three.js sets, fifteen scenarios, one-to-eight cast slots, camera banks, a full lighting rig, blocking, a take timeline and media export.

## Open

`dist/v0.4.0/The Directors Chair-darwin-arm64/The Directors Chair.app`

Built for Apple silicon. Locally ad-hoc signed; not notarized for public distribution. All scene assets are bundled and work offline.

## Studio Expansion 0.4

Open Locations to choose Philadelphia Diner, Loft Apartment, Interview Room, Rooftop Terrace or Television Studio. Each contains three original directed scenarios with cast counts from one to eight. Loading one keeps recorded takes; Undo restores the previous setup. The family diner setup joins three tables and rearranges six supported seats.

Blocking adds cast slots, names and two appearance choices, using independent skeleton clones of the existing licensed meshes. There are eight controllable people, not eight unique base appearances. Camera and Lighting can target every named cast member. Wide coverage fits the ensemble; close coverage uses the selected person. Save/load camera banks A, B and C from the Camera inspector. Banks store position, target, lens, aperture, focus and exposure without changing the set or lighting.

Takes carry their complete location, scenario, cast and arrangement. A cut can switch between locations. All runtime scenes are manually authored modular geometry; no new external 3D generation is claimed.

The complete build prompt is in BUILD-PROMPT.md and the native Google Doc: https://docs.google.com/document/d/1UGBmLBfAi6eFbunGqOxG57YR3-Ar-JVaPBGWVJMquCM/edit

## What changed in 0.2

Fitted seated poses with cushion contact and floor-level soles; corrected booth proportions; seat-constrained blocking and an aisle standing position. Added local 2K material maps, surface relief, worn tile and wood, contact shading, smoother edges and a grounded telescoping light stand. Camera presets follow actors; precise numeric entry, double-click focus, undo/redo, a panel-free view and consistent 1.85:1 framing improve the working controls. Existing projects and takes remain supported. Seated positions are fitted to the hero booth when displayed.

## Controls

- Stage: drag to orbit, scroll to dolly, Shift-drag to pan. Overview / Top / On set presets. W A S D moves through the set in On set mode.
- Camera: focal length, aperture, focus, camera position, target, key-light position/intensity, mood and exposure. Type exact values beside sliders. Double-click a visible actor or prop to focus. R captures a take; H hides/shows panels. Coverage and Grid remain available above the image.
- Blocking: slide either seated actor along their fitted cushion, or choose Stand in aisle to move/rotate freely. Seat in booth restores their supported pose.
- Cut: select, rename, reorder, remove or adjust the duration of takes. Space screens the cut.
- Studio: change hero-table dressing, hide equipment, or export a GLB of the dressed set.
- Undo/Redo: header buttons or Command-Z / Command-Shift-Z restore the last 24 settled project states. Text inputs retain normal typing behavior.
- Save/Open: portable JSON project. Automatic recovery uses the local app data directory.
- Export frame: 1920×1038 PNG. Export film: real-time silent WebM at viewport resolution. Escape stops playback or an in-progress recording.

## Evidence

`npm run check` validates syntax, project data and GLB files. `tools/verify.cjs` exercises the actual Electron renderer in isolated QA storage: pointer orbit, presets, capture, lens/light, actor transform, dressing, reorder/duration, save/open, frame/video export, corrupt input rejection, reload recovery and minimum layout.

Results: `evidence/verification.json` (26 integration checks) and `evidence/visual-validation.json` (seating geometry, renderer errors and frame timing). Screenshots are in `evidence/`. Integration testing uses controlled file-dialog responses; packaged native-window verification is tracked separately in `evidence/release-status.md`.

## Fidelity and scope

This is a working prototype, not a perfect recreation of the AI concept art. The overall layout, diner palette, tools, scene structure and filmmaking loop are implemented. Actor likenesses, clothing, hair, facial performance and photoreal lighting still differ from the reference. Scene complexity varies with location and active cast; measured counts are in evidence/expansion-verification.json. Most set/equipment geometry is original parametric work; actors use Microsoft Rocketbox with attribution.

Fifteen authored scenario prompts and parameter-based review notes are present. Cross-location takes and three camera setup banks are supported. There is no live AI tutor, recorded dialogue, full performance animation, advanced color grading or professional certification. Depth of field is a real-time approximation, not a calibrated lens test instrument. Walk mode does not provide collision avoidance.

## Development

`npm install` then `node node_modules/electron/install.js` when needed.

`npm start` — run source.
`npm run check` — validation.
`npm run package` — produce Mac bundle.

Asset sources, licensing and modifications: `THIRD_PARTY_LICENSES.md`.
Concept references: `design/`. Specification: `PRD.md`. Research: `RESEARCH.md`.


## Scene control — version 0.3

Open **Lighting** for an outliner of the key, fill, rim and four practical lamps. Select a source in the list or click its diamond handle. Drag the colored gizmo to move it; **G** selects Move, **E** selects Rotate, and **Aim** moves a spotlight target. Exact numeric positions, aim targets, actor targeting, color, intensity, beam spread, approximate source softness, shadow on/off, solo and reset are available in the inspector. You can add or duplicate point/spot lights and delete unused sources; the key is retained for legacy camera controls. The scene supports eight simultaneous lights. Snap uses 10 cm or 15° increments.

Open **Studio** to move, rotate, hide or reset the floor/platform, window walls/door, booth seats, tables, coffee cups, the counter, espresso machine, director’s chair and hero-table dressing. Furniture uses parent-relative transforms: moving a table carries its cups, and moving or rotating a booth carries its seated actor. Actors can still stand and move independently in Blocking. Black flags are real shadow-casting geometry; up to twelve can be placed to cut direct light. Select flowers or the menu under Hero table dressing to show those props.

Every take, portable save and autosave includes the lighting rig, custom flags and object arrangement. Old version-1 projects and takes migrate when loaded. Undo/redo restores these changes. Existing owner saves are not rewritten by automated QA, which uses a separate temporary profile.

### Lighting limits

Point and spot lights use inverse-square distance falloff, dynamic direct illumination/specular response and shadow maps. Source width controls a filtered soft-shadow approximation; it is not a physically measured emitter or contact-hardening solution. Ambient fill and environment reflections are approximate. This renderer does not calculate reflected light bounce, diffusion fabrics, volumetric beams or calibrated lux values. Placement is manual, without collision, gravity or automatic foot-to-floor adjustment after moving an entire booth. A raised or rotated booth carries the actor as one assembly. The surrounding exterior remains fixed. This is a hands-on filmmaking prototype, not a finished photoreal production simulator.
