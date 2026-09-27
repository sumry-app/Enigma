# Visual assets

All images in this folder are original to Enigma. They are generated as plain SVG by [`src/build_assets.py`](src/build_assets.py) (standard-library Python, fixed random seeds), so every mark in them can be traced to code. No third-party imagery, stock art, or reference images are included.

```
python3 assets/src/build_assets.py
```

| File | What it is |
| --- | --- |
| `enigma-mark.svg` | Project mark: a halftone grid with an empty centre. Evidence around a gap it can't fill. |
| `enigma-hero.svg` | Illustration of the idea: sources → structured evidence → ordered rules → evidence states, with one trace back to its sources. Sources are the synthetic ones from [`examples/`](../examples/). |
| `enigma-concept.svg` | **Design concept — not current implementation.** A mockup of how one result (synthetic result P-1) could be inspected. No Enigma interface exists. The label is part of the image itself. |

## Visual language

Color carries meaning. It is never decoration.

| Color | Hex | Meaning |
| --- | --- | --- |
| Ink | `#0C0C0E` | Ground |
| Bone | `#ECE8E1` | Evidence, support, primary text |
| Ember | `#E4502E` | Conflict, and nothing else |
| Haze | `#7FA0CF` | Insufficient or unresolved evidence |
| Dim | `#8E8A81` | Secondary text, structure |

Each evidence state has one texture, and the textures are used the same way everywhere:

| State | Texture |
| --- | --- |
| `SUPPORTED_RELATIONSHIP` | Dense, regular halftone |
| `NO_RELATIONSHIP` | Regular rings: an established absence |
| `CONTRADICTORY_EVIDENCE` | Two opposing halftones, bone and ember, both kept |
| `MISSING_EVIDENCE` | Haze halftone that thins out inside a dashed outline it never fills |
| `UNKNOWN_RELATIONSHIP` | Irregular haze grain |
| `UNEXPLORED_RELATIONSHIP` | Empty dashed outline |

Type is a monospace stack for labels and data and a system sans stack for prose. Both are system fonts, so nothing is downloaded.

## Rules for new visuals

- No imagery of brains, robots, circuit boards, or glowing networks.
- No mockups that could pass for screenshots. Any interface concept carries "Design concept — not current implementation" inside the image, in its caption, and in its alt text.
- Data shown in a visual comes from the synthetic examples, never from real studies, real students, or evaluation material.
- Every image needs alt text that states what it shows.
