# Director’s Chair — build research

The owner requests a native Electron Mac app with genuine 3D geometry and interactive filmmaking tools, matching the five approved concept images. This is an implementation of that direction, not a new product selection.

## Technical decision

Use a local Three.js scene inside a sandboxed Electron shell. Keep set, actor geometry, textures, camera states and saved takes offline. A hosted viewer cannot support actor blocking, set dressing and editable shots together. A still-image interface cannot satisfy the request.

Official references consulted:
- https://threejs.org/docs/pages/BokehPass.html — depth-of-field pass for film camera.
- https://threejs.org/docs/pages/RectAreaLight.html — area lighting; use spot/point lights for shadow casting.
- https://www.electronjs.org/docs/latest/tutorial/security — isolated renderer, sandbox, restricted navigation and IPC.
- https://github.com/microsoft/Microsoft-Rocketbox — MIT licensed rigged human geometry and textures. Previewed ten adult candidates; female 05 has the nearest short dark hair and blazer, male 02 the nearest neutral wardrobe. Neither is an exact likeness of the fictional AI actors. Use local GLBs with attribution.
- https://github.com/microsoft/Microsoft-Rocketbox/blob/master/LICENSE.md — MIT terms retained with the application.
- https://www.blackmagicdesign.com/ca/products/davinciresolve/training — editing, color and sound as connected practical work.
- https://www.studiobinder.com/blog/blocking-and-staging-scenes/ — spatial staging as a narrative tool.

## Alternatives and challenge

Scores 1–5 (value / differentiation / existing evidence / trust / lower build risk / faster proof):
- Full professional editor: 4/2/2/4/1/1. Too much general-purpose machinery before filmmaking lessons work.
- One diner teaching studio: 5/4/4/5/4/5. Selected: one scene covers staging, lens, light, cut and review.
- Entire virtual film school: 5/4/1/3/1/1. Longer-term direction; cannot be honestly certified from one build.
- Skeptic / shot-only camera toy: 2/2/3/5/5/5. Useful first rendering check but insufficient for the owner’s role-complete request.

Strongest dissent: cinematic human performance and photoreal asset fidelity are content-production problems, not solved by UI controls. Preserve that limitation in release notes and compare actual screenshots to the concepts.

## Asset rail

Diner, booths, tables, equipment, practical lamps, street, rain, props: original parametric 3D geometry, with locally generated procedural surface textures. Actors: licensed textured, rigged meshes converted through Blender to local GLB; poses adjusted for sitting/standing. No concept screenshot used as a substitute for 3D viewport content.

All educational feedback is authored and parameter-based. No simulated AI connection, outside communication, account changes, paid asset purchases or deployment.
