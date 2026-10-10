# ExquisiteFin

A custom Jellyfin 12 Modern theme based on ElegantFin.

## Status

**v0.1.0 — compatibility baseline**

ExquisiteFin is being built as an independent, maintainable theme rather than a collection of one-off Jellyfin Custom CSS or DevTools overrides.

The first release deliberately preserves ElegantFin's appearance. It establishes a known-good loading order for Jellyfin 12 Modern so that later design changes can be made in one place and versioned cleanly.

## Install

In Jellyfin, open **Dashboard → General → Custom CSS** and import:

```css
@import url("https://cdn.jsdelivr.net/gh/laytnight-coder/ExquisiteFin@main/Theme/ExquisiteFin.css");
```

For development, the stylesheet can also be pasted directly into Jellyfin's Custom CSS field.

## v0.1 architecture

`Theme/ExquisiteFin.css` currently loads:

1. ElegantFin.
2. ElegantFin's Media Bar support layer.
3. The ElegantFin Jellyfin 12 Modern companion.
4. An ExquisiteFin-owned settings section.
5. An ExquisiteFin-owned override section.

All ExquisiteFin overrides intentionally come after the upstream layers.

## Development plan

- Establish the v0.1 baseline in Jellyfin 12 Modern.
- Add a clearly separated ExquisiteFin settings/variables section.
- Correct library card sizing using the actual Modern UI structure.
- Refine cards, buttons, borders, glow, spacing, navigation, and typography.
- Study other Jellyfin themes for inspiration and selectively recreate useful ideas.
- Gradually replace upstream-dependent pieces where doing so improves independence and maintainability.

## Project structure

```text
ExquisiteFin/
├── Theme/
│   ├── ExquisiteFin.css
│   └── assets/
├── docs/
│   └── design-notes.md
├── README.md
├── CHANGELOG.md
└── LICENSE
```

## License

ExquisiteFin is released under the **GNU General Public License v2.0 (GPL-2.0)**, consistent with its ElegantFin starting point. See [`LICENSE`](LICENSE).

ElegantFin is by **lscambo13**. The Jellyfin 12 Modern companion is by **mihaif7**. ExquisiteFin is an independent project and is not an official ElegantFin project.
