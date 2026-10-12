# ExquisiteFin

**ExquisiteFin** is a custom CSS theme for Jellyfin 12's Modern interface. It uses adapted, locally bundled CSS from ElegantFin and its Jellyfin 12 Modern companion, with ExquisiteFin's own teal-accented styling layered on top.

> **Current version:** v0.6.0  
> **Target UI:** Jellyfin 12 Modern  
> **Status:** Active development. The bundled CSS has been structurally validated; a fresh live Jellyfin smoke test is still recommended after upgrading.

## Features

### Theme identity
- Teal/emerald accent built around `#00c79f`.
- Centralized ExquisiteFin colour, surface, focus, and layout variables.
- Teal hover borders and visible keyboard focus styling.

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
- On desktop-sized layouts (901px and wider), Genres appears as a compact rounded dark pill below the main hero action buttons.
- The Genres relocation is scoped to desktop-sized layouts; mobile and TV layouts retain their normal flow.

## Install

In Jellyfin, open **Dashboard → General → Custom CSS** and add this single import:

```css
@import url("https://cdn.jsdelivr.net/gh/laytnight-coder/ExquisiteFin@main/Theme/ExquisiteFin.css");
```

For a reproducible v0.6.0 install pinned to the current bundle commit:

```css
@import url("https://cdn.jsdelivr.net/gh/laytnight-coder/ExquisiteFin@d1e52ce886dba8abf5d0ac0276ed686a7de99ba8/Theme/ExquisiteFin.css");
```

Save the Custom CSS and refresh Jellyfin. ExquisiteFin now bundles the required ElegantFin base rules, Jellyfin 12 Modern compatibility rules, and ExquisiteFin overrides into **one stylesheet**. It no longer imports ElegantFin or the Modern companion as separate CSS files.

### Optional: Media Bar plugin

If you use Media Bar or Media Bar Enhanced, add the adapter as a second import, **after** the main theme:

```css
@import url("https://cdn.jsdelivr.net/gh/laytnight-coder/ExquisiteFin@main/Theme/ExquisiteFin.css");
@import url("https://cdn.jsdelivr.net/gh/laytnight-coder/ExquisiteFin@main/Theme/ExquisiteFin-MediaBar.css");
```

Pinned v0.6.0 URLs:

```css
@import url("https://cdn.jsdelivr.net/gh/laytnight-coder/ExquisiteFin@d1e52ce886dba8abf5d0ac0276ed686a7de99ba8/Theme/ExquisiteFin.css");
@import url("https://cdn.jsdelivr.net/gh/laytnight-coder/ExquisiteFin@383d64bff67a0ed99d9d1e52fceb8d550f8704e4/Theme/ExquisiteFin-MediaBar.css");
```

The Media Bar adapter is optional. Do not add it unless the plugin is installed.

## Independence and remaining external assets

The main stylesheet no longer depends on CSS files hosted by either upstream theme. The required theme and Modern compatibility rules are bundled in this repository and are loaded with one ExquisiteFin stylesheet import.

For font rendering, the bundle still requests Inter through Google Fonts and loads Material Symbols font files from Google's font CDN, matching the upstream appearance. These are **font assets**, not upstream theme CSS dependencies. The theme is independent of upstream stylesheet delivery, but it is not an entirely offline package.

The vendored rules are based on:

- [ElegantFin](https://github.com/lscambo13/ElegantFin), v26.09.05, by lscambo13.
- [ElegantFin Jellyfin 12 Modern companion](https://github.com/mihaif7/elegantfin-jf12), v26.10.07, by mihaif7.

Because the code is now vendored, upstream stylesheet updates will not flow in automatically. The source versions are intentionally explicit so future updates can be reviewed and tested rather than changing the UI unexpectedly.

To reduce plugin-only CSS in the main bundle, the Jellyfin Enhanced, Episodes Ratings Grid, and KefinTweaks-specific styling blocks have been omitted from the core. Media Bar support is separate by design.

## Settings

Frequently adjusted values are near the top of `Theme/source/ExquisiteFin-overrides.css` and are included in the generated bundle:

| Variable | Default | Purpose |
|---|---|---|
| `--exquisite-accent` | `#00c79f` | Main accent colour |
| `--exquisite-accent-border` | `#00c79f` | Accent borders |
| `--exquisite-library-card-padding` | `25%` | Height of targeted library-folder cards; 25% produces a 4:1 shape |
| `--resumeCardScale` | `1.20` | Continue Watching card scale |
| `--backdropTrimFromTop` | `0%` | Prevents trimming the top of movie backdrops |

Edit the source override file and rebuild to ensure your changes remain reproducible. Avoid editing the generated bundle directly unless you intend to replace the source build process.

## Source layout and rebuilding

```text
ExquisiteFin/
├── Theme/
│   ├── ExquisiteFin.css
│   ├── ExquisiteFin-MediaBar.css
│   └── source/
│       ├── ElegantFin.css
│       ├── Jellyfin12-Modern.css
│       ├── MediaBar-ElegantFin.css
│       └── ExquisiteFin-overrides.css
├── scripts/
│   └── build_theme.py
├── docs/
│   └── design-notes.md
├── CHANGELOG.md
├── LICENSE
└── README.md
```

The source files keep the upstream code and attribution available for maintenance. The build script trims optional plugin sections from the core, moves the Modern Media Bar section into the optional adapter, and writes both distributable stylesheets.

Run from the repository root:

```sh
python scripts/build_theme.py
```

Validate and report output sizes without rewriting files:

```sh
python scripts/build_theme.py --check
```

Core Modern compatibility includes the app bar, navigation, library toolbar, drawer, menus/dialogs, form controls, video player, icon buttons, in-player episode picker, and progress rules. Shared `:root` selectors between the base and Modern companion are intentional: the Modern layer bridges ElegantFin's palette variables to Jellyfin's MUI palette rather than duplicating identical declarations.

## Development approach

- Make one visible change at a time and test it in Jellyfin.
- Inspect current Modern UI markup before introducing selectors.
- Keep configuration variables together and feature rules grouped by purpose.
- Review upstream changes deliberately before refreshing vendored sources.
- Test desktop, mobile, and TV layouts separately whenever a change should affect more than one form factor.

All ExquisiteFin-specific changes stay in this repository; the upstream projects are not modified.

## Credits and licensing

ElegantFin is maintained by **lscambo13**. The Jellyfin 12 Modern companion is maintained by **mihaif7**. ExquisiteFin is an independent project and is not an official ElegantFin or Jellyfin project.

ExquisiteFin is distributed under **GPL-2.0**, consistent with the upstream theme. See [LICENSE](LICENSE). Original upstream attribution headers and source copies are retained.
