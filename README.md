# ExquisiteFin

**ExquisiteFin** is a custom CSS theme for Jellyfin 12's Modern interface, built on ElegantFin and its Jellyfin Modern compatibility companion. It keeps ElegantFin's dark foundation while adding a restrained teal accent, more expressive card controls, and a more polished movie-detail hero.

> **Current stylesheet:** v0.5.3  
> **Compatibility focus:** Jellyfin 12 Modern  
> **Project status:** actively developed; visual changes are tested incrementally.

## Features

### Theme identity
- Teal/emerald accent built around `#00c79f`.
- Centralized ExquisiteFin colour, surface, focus, and layout variables.
- Teal hover borders and visible keyboard focus styling.

### Home and library
- Wide 4:1 collection and library-folder cards.
- Larger Continue Watching cards using ElegantFin's `--resumeCardScale: 1.20`.
- Hides the “My Media” heading above the home library shortcuts.
- Teal library/status indicators and top-left card indicators.

### Card actions
- Large centered play control with a teal outline.
- Clean white secondary icons without idle circles, borders, or glow.
- Hides the card three-dot menu.
- Keeps selected actions distinct: bookmark blue, Mark Played green, Favorite red.
- Slightly raised card playback progress strip.

### Movie details
- Movie backdrop artwork is anchored at the top.
- Synopsis and IMDb/TMDb links are centered.
- On desktop-sized layouts (901px and wider), the Genres row is styled as a compact rounded dark pill beneath the hero action buttons rather than remaining in the lower metadata list.
- The Genres relocation rule intentionally does not apply to mobile-sized and TV layouts.

## Install

In Jellyfin, open **Dashboard → General → Custom CSS** and add:

```css
@import url("https://cdn.jsdelivr.net/gh/laytnight-coder/ExquisiteFin@main/Theme/ExquisiteFin.css");
```

This follows the latest contents of the `main` branch. To pin your setup to the current v0.5.3 stylesheet, use this commit-specific URL instead:

```css
@import url("https://cdn.jsdelivr.net/gh/laytnight-coder/ExquisiteFin@39b119075159f9e7157f75fa5225c3f623566486/Theme/ExquisiteFin.css");
```

After saving the Custom CSS, refresh Jellyfin. If an older temporary testing stylesheet is still configured, replace its import with one of the main stylesheet imports above.

## Settings

The most useful ExquisiteFin-owned values are grouped near the top of `Theme/ExquisiteFin.css`:

| Variable | Default | Purpose |
|---|---|---|
| `--exquisite-accent` | `#00c79f` | Main accent colour |
| `--exquisite-accent-border` | `#00c79f` | Accent borders on interactive elements |
| `--exquisite-library-card-padding` | `25%` | Height of targeted library-folder cards; 25% produces a 4:1 shape |
| `--resumeCardScale` | `1.20` | Continue Watching card scale |
| `--backdropTrimFromTop` | `0%` | Prevents the upstream theme from trimming the top of movie backdrops |

The stylesheet also maps these ExquisiteFin variables into ElegantFin's accent, surface, selector, and card-action settings. Prefer changing the variables over adding unrelated one-off overrides.

## How the stylesheet is organized

`Theme/ExquisiteFin.css` is organized into five sections:

1. **Settings and upstream theme variables** — imports, palette, layout values, and ElegantFin mappings.
2. **Home and library presentation** — library card geometry, hidden home heading, and status indicators.
3. **Card play and secondary actions** — primary play button, secondary controls, selected-state colours, and progress.
4. **Movie details** — backdrop positioning, centered synopsis/links, and the desktop Genres pill.
5. **General interactive states** — hover borders and keyboard focus.

All ExquisiteFin overrides are placed after the upstream imports so they can take precedence over the base theme where needed.

## Upstream dependencies

The theme currently imports these upstream stylesheets from jsDelivr:

- [ElegantFin](https://github.com/lscambo13/ElegantFin) — pinned to `v26.09.05`.
- ElegantFin Media Bar plugin support — pinned to `v26.09.05`.
- [ElegantFin Jellyfin 12 Modern companion](https://github.com/mihaif7/elegantfin-jf12) — pinned to `v26.10.07`.

Because these base styles are imported remotely, ExquisiteFin is **not yet fully self-contained**. The pinned upstream versions make the dependency points explicit; the project can gradually replace upstream-dependent pieces where doing so improves maintainability.

## Project structure

```text
ExquisiteFin/
├── Theme/
│   └── ExquisiteFin.css
├── docs/
│   └── design-notes.md
├── CHANGELOG.md
├── LICENSE
└── README.md
```

Temporary test stylesheets are kept out of the cleaned-up main branch once their confirmed changes have been promoted or discarded.

## Development approach

- Make one visible change at a time.
- Test against the actual Jellyfin 12 Modern markup instead of assuming legacy selectors still apply.
- Keep user-facing variables together and overrides grouped by purpose.
- Record merged changes in [CHANGELOG.md](CHANGELOG.md).
- Test desktop, mobile, and TV layouts separately when a change is intended to affect more than one of them.
- Avoid modifying upstream ElegantFin repositories; ExquisiteFin-specific work stays in this repository.

## Credits and licensing

ElegantFin is maintained by **lscambo13**. The Jellyfin 12 Modern companion is maintained by **mihaif7**. ExquisiteFin is an independent project and is not an official ElegantFin or Jellyfin project.

ExquisiteFin is distributed under **GPL-2.0**, consistent with its ElegantFin starting point. See [LICENSE](LICENSE).
