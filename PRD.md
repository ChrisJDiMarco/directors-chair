# The Director’s Chair — Studio Expansion 0.4

Governing build brief: BUILD-PROMPT.md, also delivered as a native Google Doc. The original diner specification is preserved in tools/backups/v0.3/PRD.md. This release extends the existing application and does not claim exact photoreal parity with the AI concepts.

## Executable release

Five distinct locations: diner, loft, interview room, rooftop, television studio. Fifteen scenario definitions in catalog.js include location, cast count, dramatic mission, teaching concept and shot experiment. Locations browser loads a coherent setup without dropping recorded footage.

One-to-eight named cast slots using two licensed base appearances, independent cloned skeletons, supported seat attachments and standing placement. Stable cast identities survive removals; assigned seat indices preserve seating ownership. Other actors must not be unexpectedly moved or reposed when removing one slot.

Camera banks A/B/C store camera position, target, lens, aperture, focus and exposure. Camera and lighting target all active cast members. Ensemble wide shots fit the complete cast; single-person mode never references a missing second actor.

Existing lighting, scene editing, black flags, material maps, camera controls, project saves, undo/redo, cuts, PNG and silent WebM exports remain. Every take includes its location, cast and scene state. Legacy projects migrate on display; invalid new data is rejected before changing state.

## Verification

Test all fifteen loads, one/eight cast limits, rename/appearance/removal, independent skeletons, supported seating, banks, cross-location takes and restart recovery. Capture every new set from stage and film camera. Test eight-person framing, small-window fit, geometry support, hidden-world isolation and bounded pooled actors. Rerun existing integration checks for regressions. Package and locally sign an arm64 Mac app; verify runtime source and packaged interactions. Native owner-window proof is separate and must not be claimed from isolated QA.

## Production roadmap — not implemented in 0.4

Authored performance clips, timed actor marks, continuous camera moves, synchronized multicamera live feeds, sound editing, dialogue/lip sync, color scopes, physically calculated bounce and diffusion, and unique expanded actor assets. These remain future requirements in the complete build brief, not working controls or promised completion in this release.
