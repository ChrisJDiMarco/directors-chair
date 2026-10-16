# Director’s Chair 0.4.0 — Studio Expansion

Application: `dist/v0.4.0/The Directors Chair-darwin-arm64/The Directors Chair.app`.
Complete build prompt and implementation status: https://docs.google.com/document/d/1UGBmLBfAi6eFbunGqOxG57YR3-Ar-JVaPBGWVJMquCM/edit
Editable source prompt: BUILD-PROMPT.md. Executable scope: PRD.md. Scenario definitions: catalog.js. New authored scene geometry: locations.js.

## Implemented

Five locations (diner, loft, interview, rooftop, television), fifteen scenarios, one-to-eight named cast slots using two existing appearance bases, independently cloned skeletons, stable identities and assigned seating, full-cast framing and targeting, saved camera banks A/B/C, cross-location takes, and scenario-specific teaching prompts. Existing scene/light manipulation and editing/export features retained. Playback completion now saves the final viewed scene consistently.

Previous releases remain available. The existing seven-take owner project was validated and backed up in tools/backups/v0.3/owner-project-before-expansion.director.json. QA uses isolated temporary profiles.

## Verified

- Native Google Doc created, populated with the complete adapted prompt, and read back. Its sixteen original headings and complete text were verified before implementation status was appended.
- Nine packaged expansion checks passed, exercising all fifteen scenario loads, cast bounds/name/appearance/removal, independent skeletons, A/B/C setup operations, automatic location changes at cuts, camera-bank/project persistence and minimum 1120×740 layout. No JavaScript/WebGL errors reported. See expansion-verification.json.
- Foot grounding in all five sets, eight-person camera framing, stable removal and seat reuse passed. See cast-geometry.json.
- Existing 26-check integration suite and nine scene/light editor checks passed on the expanded source. PNG/WebM export, save/open, undo/redo and prior diner behavior remain covered.
- Apple-silicon package locally ad-hoc signed; deep/strict verification passed. Ten packaged runtime files exactly match final source. See bundle-validation-v0.4.json.
- Stage and film-camera screenshots of all four new worlds were captured and inspected; ensemble framing and excessive defocus were corrected during visual review.
- Warm static eight-actor QA sampled roughly 8.3 ms median frame callback intervals and approximately 4.5–5.7 ms CPU submission. These are isolated QA observations, not direct GPU timings or a guarantee during editing. Full multipass draw calls are substantially higher than single-pass geometry counts. See expansion-performance.json.

## Remaining limits

The exact owner-visible live Mac-window check remains unverified. Prior Cabinet desktop inspection was blocked by guest-only routing, and no bypass was used. Packaged test-window interactions are separate evidence.

Eight cast slots reuse two licensed base appearances; they are not eight unique scanned people. New worlds are manually authored modular geometry and are less detailed than the original AI concept art. Shadows/defocus are approximate; no computed bounce, diffusion, collision or gravity. Full authored acting, timed marks, continuous camera moves, synchronized multicamera live feeds, dialogue/audio editing and advanced color scopes remain Production-release work in the Google Doc.
