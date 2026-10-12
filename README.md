# ExquisiteFin

**ExquisiteFin** is a custom CSS theme for Jellyfin 12's Modern interface. It combines adapted ElegantFin/Jellyfin 12 Modern styling with ExquisiteFin's own teal-accented design.

> **Current version:** v0.6.4  
> **Target UI:** Jellyfin 12 Modern  
> **Status:** Active development.

## Features

### Theme identity
- Teal/emerald accent built around `#00c79f`.
- Centralized ExquisiteFin colour, surface, focus, and layout variables.
- Teal hover borders and visible keyboard focus styling.
- Flat header library navigation with no pill backgrounds; the current page uses ExquisiteFin teal.

### Home and library
- Wide 4:1 collection and library-folder cards.
- Larger Continue Watching cards using `--resumeCardScale: 1.20`.
- Hides the “My Media” heading above the home library shortcuts.
- Teal library/status indicators and top-left card indicators.

### Card actions
- Large centered play control with a teal outline.
- Clean white secondary icons without idle circles, borders, or glow.
- Hides the card three-dot menu.
- Persistent selected-action colours: bookmark blue, Mark Played green, Favorite red.
- Slightly raised playback progress strip.

### Movie details
- Movie backdrop artwork is anchored at the top.
- Synopsis and IMDb/TMDb links are centered.
- On desktop-sized layouts, Genres appears as a compact rounded dark pill below the main hero action buttons.
- Mobile and TV layouts retain their normal Genres flow.

## Install

In Jellyfin, open **Dashboard → General → Custom CSS** and add:

```css
@import url("https://cdn.jsdelivr.net/gh/laytnight-coder/ExquisiteFin@main/Theme/ExquisiteFin.css");
```

For a reproducible install, pin the import to a specific commit rather than `main`.

Save the Custom CSS and refresh Jellyfin. The main stylesheet is a complete ExquisiteFin bundle and does not import upstream theme CSS.

### Optional: Media Bar plugin

If you use Media Bar or Media Bar Enhanced, add the adapter **after** the main theme:

```css
@import url("https://cdn.jsdelivr.net/gh/laytnight-coder/ExquisiteFin@main/Theme/ExquisiteFin.css");
@import url("https://cdn.jsdelivr.net/gh/laytnight-coder/ExquisiteFin@main/Theme/ExquisiteFin-MediaBar.css");
```

The Media Bar adapter is optional. Do not add it unless the plugin is installed.

## Distribution

The repository intentionally keeps only the distributable CSS files:

```text
ExquisiteFin/
├── Theme/
│   ├── ExquisiteFin.css
│   └── ExquisiteFin-MediaBar.css
├── docs/
│   └── design-notes.md
├── CHANGELOG.md
├── LICENSE
└── README.md
```

`Theme/ExquisiteFin.css` is the main theme and contains the accepted ExquisiteFin styling, ElegantFin base rules, and Jellyfin 12 Modern compatibility rules in one stylesheet.

`Theme/ExquisiteFin-MediaBar.css` is the optional Media Bar adapter. It remains separate so users without the plugin do not need to load its plugin-specific CSS.

There is no build step or source tree in the distributable repository. The published CSS files are the maintained theme outputs.

## Independence and remaining external assets

The main stylesheet no longer depends on CSS files hosted by either upstream theme. The required theme and Modern compatibility rules are bundled in the ExquisiteFin stylesheet.

The bundle still requests Inter and Material Symbols font assets from Google-hosted endpoints to preserve typography and icons. These are font assets, not upstream theme CSS dependencies, so the theme is independent of upstream stylesheet delivery but is not a fully offline package.

The Media Bar adapter keeps its optional plugin-specific rules separate from the core, including the TV-specific slideshow adaptation.

## Settings

Frequently adjusted ExquisiteFin variables are kept near the beginning of the main stylesheet:

| Variable | Default | Purpose |
|---|---|---|
| `--exquisite-accent` | `#00c79f` | Main accent colour |
| `--exquisite-accent-border` | `#00c79f` | Accent borders |
| `--exquisite-library-card-padding` | `25%` | Height of targeted library-folder cards; 25% produces a 4:1 shape |
| `--resumeCardScale` | `1.20` | Continue Watching card scale |
| `--backdropTrimFromTop` | `0%` | Prevents trimming the top of movie backdrops |

Edit the published CSS directly when making a change, then test it in Jellyfin before committing.

## Development approach

- Make one visible change at a time and test it in Jellyfin.
- Inspect current Modern UI markup before introducing selectors.
- Keep configuration variables together and feature rules grouped by purpose.
- Test desktop, mobile, and TV layouts separately whenever a change should affect more than one form factor.
- Keep optional plugin compatibility in the separate Media Bar adapter.

The current desktop library spacing is intentionally left alone: the browser layout is already correct, and the earlier experimental negative-margin adjustment is not part of ExquisiteFin.

## Credits and licensing

ElegantFin is maintained by **lscambo13**. The Jellyfin 12 Modern companion is maintained by **mihaif7**. ExquisiteFin is an independent project and is not an official ElegantFin or Jellyfin project.

ExquisiteFin is distributed under **GPL-2.0**, consistent with the upstream theme. See [LICENSE](LICENSE).
