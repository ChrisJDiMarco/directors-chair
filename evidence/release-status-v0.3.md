# Director's Chair 0.3.0 — September 6, 2026

Updated application: `dist/v0.3.0/The Directors Chair-darwin-arm64/The Directors Chair.app`.
The earlier 0.2 application remains in its original destination; no existing running owner bundle was replaced or relaunched.

## Delivered

- Lighting workspace: seven initial independent sources; add/duplicate/delete to a maximum of eight. Source XYZ, spotlight aim XYZ and actor targets, intensity, gel color, beam spread, approximate shadow softness, shadows, on/off, solo and reset.
- Direct 3D translation and rotation, target manipulation, optional 10 cm / 15 degree snapping. Existing camera/light controls retained.
- Studio outliner: floor/platform, walls/door, booths, tables, cups, counter/stools, espresso machine, director chair and table dressing. Translation, rotation, visibility and reset. Seated actors follow their booth; table props follow their table.
- Custom black flags block direct light and cast actual shadows. Up to twelve flags.
- Extended project validation and legacy migration; complete arrangement saved in takes, autosave and portable projects; undo/redo retained.

## Checks

- Source syntax and legacy/new project validation passed, including malformed light/object rejection.
- Existing 26-check integration suite passed on the 0.3 source implementation: camera, seating, editing, save/open/recovery, PNG/WebM exports, numeric entry, undo/redo and layout.
- Nine new checks passed against the packaged 0.3.0 application, including actual pointer dragging, source settings, rendered-light response, duplication/deletion, booth/actor and table/prop parenting, flags, undo/redo, takes and reload persistence. No renderer or JavaScript errors were reported. See `editor-verification.json`.
- Controlled source-render check: floor luminance sample 198.83 with near source, 125.04 with farther source, 0 under the flag with ambient off, 0 with the narrow beam aimed away. Images visually inspected; see `light-response.json` and `light-*.jpg`.
- Eight packaged runtime files exactly match final source; packaged version 0.3.0 verified. Package metadata was intentionally pruned by Electron Packager. See `bundle-validation-v0.3.json`.
- Local ad-hoc signing and deep/strict signature verification passed.
- QA launches use temporary test profiles, not the owner's saved project.

## Remaining limits

The requested native before/after interaction check on the owner's live Mac window remains unverified. Cabinet previously rejected that inspection because computer control was routed to the isolated guest; no host-target retry or alternate desktop-control bypass was used. Packaged application testing is separate evidence and does not substitute for that live-window check.

Source softness uses filtered shadow maps; there is no reflected bounce, fabric diffusion, volumetric lighting, calibrated exposure measurement, collision or gravity simulation. The exterior remains fixed. Character likeness and scene fidelity still differ from the AI concepts. This is a working prototype, not a perfect photoreal reconstruction.
