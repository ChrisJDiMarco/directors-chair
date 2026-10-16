# The Director’s Chair — implementation specification

Status: locked for this build. Visual target: design/01-on-set.png through design/05-studio-collection.png. The owner requests accurate recreation; any visible differences remain limitations, not redefined success.

## Product

A native Mac filmmaking studio in which a beginner arranges a real 3D scene, chooses lens and lighting, captures camera takes, arranges a cut and plays it back.

## Primary loop

Open the diner → explore stage → frame the two actors → adjust lens/light → capture take → reorder and trim takes → screen scene → save/reopen project or export footage.

## Screens

- Stage: dominant navigable dollhouse set, amber lesson rail, film-camera inset, equipment, view presets, walk/orbit controls.
- Camera: film view, lens/aperture/focus, physical camera position and aim, composition grid, shot presets, depth of field and capture.
- Blocking: top view and actor positioning/standing/turning with conversation axis and camera marks.
- Cut: actual captured take thumbnails, selection, reorder, duration, playback, removal, frame/film export.
- Studio: selectable cast/equipment/prop choices and mood, real 3D scene changes.
- Review: task-specific technical observations and suggestions, completed shot list and playback. Artistic responses are suggestions, not objective grades.

## Scene and interaction

Walnut and green leather diner, ivory tiled floor with dark diamond insets, chrome counter, stools, rain windows, warm lamps, cups, saucers, condiment racks, coffee equipment, wall art, entry door. Actual cinema camera, tripod/dolly, Fresnel and softbox stand geometry. Two rigged human actors. Three lighting moods. Orbit/zoom/pan/reset; walk controls; camera presets and film lens; live inset; actor selection/position/pose; set-dressing changes.

## Persistence

Versioned project: mode, lens, aperture, focus, camera pose, lighting, actor poses, scene dressing, saved takes with camera and scene state, duration and thumbnail. Local disk through minimal validated IPC; draft autosave. Invalid projects leave the current project intact. Explicit file dialogs for importing/exporting. No network required after packaging.

## Teaching

Three authored challenges: unspoken goodbye, suspicious encounter, beginning of romance. Parameter-based feedback on coverage, shot variation, axis crossing and light. No live AI claims. No professional endorsement claimed.

## Acceptance

1. Packaged arm64 .app opens a visible Mac window with real local 3D content and no fatal console errors.
2. Actual pointer orbit and zoom/preset change the scene; film view uses the same geometry.
3. Lens changes field of view; camera position/aim and light controls visibly alter rendering.
4. Actor position and seated/standing pose change actual model transforms.
5. Capture at least three takes, reorder, change durations and play the resulting camera sequence.
6. Save and reopen preserves take/state; malformed input is rejected without losing current scene.
7. Snapshot export and video export produce readable files; canceled dialogs are harmless.
8. All five workspaces are usable at 1440×900 and minimum 1120×740; keyboard focus and help exist.
9. App is packaged and locally signed; signature verification and final window screenshots preserved.
10. Compare actual rendering with references. Report likeness, geometry and animation limits plainly; do not claim perfect recreation without matching evidence.

## Security and distribution

Local assets, contextIsolation, sandbox, no nodeIntegration, deny navigation/popups and permissions, minimal IPC. No public distribution or notarization in this build. Local ad-hoc signature only. No spend or external sends.
