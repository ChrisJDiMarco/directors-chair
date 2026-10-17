# Third-party assets and software

## Cast

Female_Adult_05 and Male_Adult_02 from Microsoft Rocketbox Avatar Library.
Copyright (c) 2020 Microsoft. MIT license.
Source: https://github.com/microsoft/Microsoft-Rocketbox
License: assets/actors/LICENSE-Microsoft-Rocketbox.md

Modifications: converted FBX to GLB in Blender, reconstructed PBR materials with supplied color/normal/opacity textures, posed at runtime, female clothing tint. Original geometry counts: female 4,570 vertices / 8,288 triangles, male 4,022 vertices / 7,312 triangles. Three material groups each: body, head, hair/opacity. Included maps remain local. These are approximate cast replacements, not exact recreations of the AI concept faces.

## Casting reference images

The avatar preview images in `design/` (Female_Adult_01-06 and 11, Male_Adult_02, 06 and 16) and `design/actor-candidates.jpg` (Rocketbox's `Docs/AvatarsSample.jpg`, renamed) are unmodified preview images from the Microsoft Rocketbox Avatar Library, used only to choose the cast.
Copyright (c) 2020 Microsoft. MIT license.
Source: https://github.com/microsoft/Microsoft-Rocketbox
License: assets/actors/LICENSE-Microsoft-Rocketbox.md

## Software

Three.js, copyright three.js authors, MIT (node_modules/three/LICENSE).
Electron, copyright Electron contributors, MIT (bundled Electron framework licenses).

Diner architecture, furniture, ceramics, cinema camera, dolly, light stands, street, procedural material maps and scene code were authored for this project. The five AI design images are references only and are not used as 3D viewport backgrounds.

## Material maps added in 0.2

Poly Haven CC0 materials, retrieved September 6, 2026:
- Leather White: https://polyhaven.com/a/leather_white (green upholstery tint)
- Wood Table Worn: https://polyhaven.com/a/wood_table_worn (walnut-toned furniture and counters)
- Marble 01: https://polyhaven.com/a/marble_01 (cropped slab maps on modeled floor tiles)
- Metal Plate: https://polyhaven.com/a/metal_plate (normal/roughness data for fittings)
- Grey Plaster: https://polyhaven.com/a/grey_plaster (warm plaster wall panels)
- Brown Leather: https://polyhaven.com/a/brown_leather (preserved downloaded candidate, not used in current scene)

License: https://polyhaven.com/license — CC0-1.0 permits use and redistribution.
Original download URLs, resolutions in filenames and byte sizes are recorded in assets/materials/sources.json. Color, OpenGL normal and roughness maps are bundled locally. Runtime UV projection, cropping, color tint, roughness and clearcoat values are authored adaptations.
