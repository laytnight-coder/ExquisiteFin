# ExquisiteFin design notes

## Current baseline — v0.6.4

ExquisiteFin targets Jellyfin 12 Modern. The distributable core is the complete `Theme/ExquisiteFin.css` bundle: it combines the required ElegantFin v26.09.05 rules, Jellyfin 12 Modern compatibility from v26.10.07, and ExquisiteFin's accepted overrides.

The core no longer imports either upstream theme stylesheet. It still loads Inter and Material Symbols font assets from Google-hosted endpoints to preserve the current typography and icons, so "self-contained" means independent of upstream theme CSS delivery rather than fully offline.

The optional `Theme/ExquisiteFin-MediaBar.css` adapter keeps Media Bar plugin styles separate from the main theme. Import it after the main theme only when Media Bar or Media Bar Enhanced is installed.

## Visual direction

Card indicators use an inset that matches their top spacing: 0.5em on desktop and 0.45em on mobile. ExquisiteFin keeps their left alignment and does not alter indicator colour or size.

- Dark blue-gray surfaces with a restrained teal accent (`#00c79f`).
- Wide collection/library-folder cards and slightly enlarged Continue Watching cards.
- A prominent centered play control and clean icon-only secondary card actions.
- Persistent semantic colours for selected bookmark, Mark Played, and Favorite states.
- Centered movie synopsis and external rating links.
- A rounded Genres pill beneath hero actions on desktop-sized layouts.
- Clear keyboard focus and hover states.
- Flat header library navigation; the current section is highlighted in teal instead of a pill.

## Distribution

The repository now contains only the maintained distributable theme files plus documentation:

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

There is no source tree or build script in the distributable repository. `Theme/ExquisiteFin.css` is the maintained main bundle, and `Theme/ExquisiteFin-MediaBar.css` is the maintained optional plugin adapter.

The Media Bar adapter keeps plugin-specific rules out of the core, including the TV-specific slideshow adaptation. Jellyfin Enhanced, Episodes Ratings Grid, and KefinTweaks-only sections are not carried in the core bundle.

## Accepted layout decisions

- The primary card play control is centered and uses the ExquisiteFin teal outline treatment.
- Secondary card actions are icon-only and positioned together at the lower right.
- Collection and UserView cards use the intended wide 4:1 geometry.
- Continue Watching uses `--resumeCardScale: 1.20`.
- Movie backdrops use `--backdropTrimFromTop: 0%`.
- Movie Genres is displayed as a dark rounded pill beneath the hero actions on desktop-sized layouts.
- Jellyfin 12 Modern header navigation uses flat text links, with inactive links light and the active page in ExquisiteFin teal.
- The library toolbar spacing is not overridden. The browser layout is already correct, and the earlier negative-margin experiment is deliberately excluded.

## Development approach

- Change one visible component at a time and verify it in Jellyfin before committing.
- Inspect the current Modern UI markup before adding selectors.
- Keep user-facing variables together and group overrides by purpose.
- Test desktop, mobile, and TV layouts separately when a change should affect more than one layout.
- Keep optional plugin compatibility in the separate Media Bar adapter.
- Preserve upstream attribution and GPL-2.0 licensing notices in the distributed CSS.

## Upstream sources and licensing

The bundled CSS is adapted from:

- [ElegantFin](https://github.com/lscambo13/ElegantFin) by lscambo13, v26.09.05.
- [ElegantFin Jellyfin 12 Modern companion](https://github.com/mihaif7/elegantfin-jf12) by mihaif7, v26.10.07.

ExquisiteFin is an independent project; it does not modify upstream repositories and is not an official ElegantFin or Jellyfin project. See the repository's `LICENSE` for licensing information.
