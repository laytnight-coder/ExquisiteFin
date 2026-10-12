# ExquisiteFin design notes

## Current baseline — v0.6.3

ExquisiteFin targets Jellyfin 12 Modern. The distributable core is now a self-contained theme bundle at `Theme/ExquisiteFin.css`: it combines the required ElegantFin v26.09.05 rules, Jellyfin 12 Modern compatibility from v26.10.07, and ExquisiteFin's overrides.

The core no longer imports either upstream theme stylesheet. It still loads Inter and Material Symbols font assets from Google-hosted endpoints to preserve the current typography and icons, so "self-contained" here means independent of upstream theme CSS delivery rather than fully offline.

The optional `Theme/ExquisiteFin-MediaBar.css` adapter keeps the Media Bar plugin styles separate from the main theme. Import it after the main theme only when Media Bar or Media Bar Enhanced is installed.

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

## Source and distribution

Files in `Theme/source/` are the attributed upstream inputs plus ExquisiteFin-owned overrides:

- `ElegantFin.css` — ElegantFin v26.09.05 readable base.
- `Jellyfin12-Modern.css` — Modern companion v26.10.07.
- `MediaBar-ElegantFin.css` — ElegantFin's optional Media Bar support.
- `ExquisiteFin-overrides.css` — ExquisiteFin-owned settings and visual rules.

Run `python scripts/build_theme.py` to generate the distributable core and optional Media Bar adapter. Run `python scripts/build_theme.py --check` to validate the generated CSS structure and confirm that the core has no upstream theme stylesheet imports without rewriting files.

The build trims Media Bar from the core and writes its base and Modern-specific styles into the optional adapter, including the TV-specific slideshow backdrop rule. Jellyfin Enhanced, Episodes Ratings Grid, and KefinTweaks-only sections are not included in the core bundle to avoid carrying plugin-specific CSS by default. ElegantFin's generic lower-corner play-button positioning is also omitted from the generated bundle because ExquisiteFin's later override fully supplies the intended centered position; the upstream source remains unchanged. The small InPlayerEpisodePreview progress rule remains in core for now.

Some selectors appear in both the ElegantFin and Modern sources, notably `:root` and `:root[data-theme="light"]`. These are intentional cascade layers: the Modern companion maps theme colours into Jellyfin's MUI palette and should not be treated as duplicate blocks without checking each property.

## Development approach

- Change one visible component at a time and verify it in Jellyfin before merging.
- Inspect the current Modern UI markup before adding selectors.
- Keep user-facing variables together and group overrides by purpose.
- Review source updates deliberately; vendored upstream code will not refresh automatically.
- Test desktop, mobile, and TV layouts separately when a change should affect more than one layout.
- Keep optional plugin compatibility in separate adapters where practical.
- Preserve upstream attribution and GPL-2.0 licensing notices.

## Upstream sources and licensing

- [ElegantFin](https://github.com/lscambo13/ElegantFin) by lscambo13, v26.09.05.
- [ElegantFin Jellyfin 12 Modern companion](https://github.com/mihaif7/elegantfin-jf12) by mihaif7, v26.10.07.

ExquisiteFin is an independent project; it does not modify upstream repositories and is not an official ElegantFin or Jellyfin project. See the repository's `LICENSE` for licensing information.
