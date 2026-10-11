# Changelog

All notable ExquisiteFin changes are documented here.

## [0.3.2] - 2026-10-11

### Fixed

- Restored the card play button as a centered, larger circular control rather than a filled teal disc.
- Made the primary card play button transparent inside with a teal border and white play glyph.
- Added a restrained teal glow while preserving Jellyfin/ElegantFin's existing overlay placement.
- Kept non-primary card actions at their normal size so the play-button treatment does not affect other controls.

### Design decision

The v0.3.1 generic mini-play accent made the play control appear as a solid teal circle in Jellyfin 12 Modern. v0.3.2 narrows the styling to the actual primary card overlay button and uses the previous ExquisiteFin visual direction as the reference: central, larger, teal-outlined, transparent, and easy to read over poster artwork.

## [0.3.1] - 2026-10-11

### Added

- Added a controlled interactive-control pass for card action buttons and other raised/icon controls.
- Added teal accent borders and restrained hover/focus glow to card action buttons.
- Added a consistent teal play-button accent.
- Added a visible keyboard focus outline without changing control layout.

### Design decision

v0.3.1 keeps the existing layout and sizing intact. The goal is to make interaction states feel native to ExquisiteFin without repeating the larger visual changes from the old custom CSS. Interactive styling is centralized through ExquisiteFin variables so it can be tuned without scattering color values through selectors.

## [0.3.0] - 2026-10-11

### Added

- Introduced the first ExquisiteFin-owned accent system.
- Added a teal/emerald accent palette centered on `#00c79f`.
- Added ExquisiteFin surface and selector variables so the visual identity can be tuned from one settings block.
- Applied the accent to active UI elements, mini-play buttons, checked controls, status indicators, and played-state icons.

### Design decision

The first visual pass keeps ElegantFin's dark blue-gray surfaces while giving ExquisiteFin its own restrained teal accent. The colors are exposed as ExquisiteFin variables rather than scattered through individual selectors, making future palette changes a single-point edit.

## [0.2.3] - 2026-10-11

### Fixed

- Corrected the library-card geometry override to target the actual `.cardPadder-overflowBackdrop` element used by Jellyfin 12 Modern.
- Matched the working Branding CSS test with a 25% `padding-bottom`, producing the intended 4:1 library-card ratio.
- Removed the previous `.cardScalable` geometry experiment from ExquisiteFin.

### Changed

- Replaced the `--exquisite-library-card-ratio` setting with `--exquisite-library-card-padding`, which directly represents the CSS value controlling the card height.
- Restricted the override to folder cards carrying `CollectionFolder` or `UserView` data on the `.card` wrapper.

### Design decision

The working Branding CSS test confirmed that Jellyfin's card height is controlled by `.cardPadder-overflowBackdrop` padding in this layout. ExquisiteFin now uses that same mechanism instead of trying to impose an independent height or aspect ratio on `.cardScalable`.

## [0.2.2] - 2026-10-11

### Changed

- Moved the library-card geometry override from `.cardPadder-overflowBackdrop` to `.cardScalable`.
- Added an explicit `--exquisite-library-card-ratio` setting.
- Removed the padder's percentage height for the targeted library cards so it cannot compete with the ExquisiteFin ratio.

### Design decision

The screenshot showed the cards remaining at exactly the ElegantFin 2:1 geometry despite the previous override. Jellyfin's card source establishes the padder ratio, but the Modern layout can also participate in the card geometry. v0.2.2 therefore makes `.cardScalable` the explicit source of truth for the ExquisiteFin test.

## [0.2.1] - 2026-10-11

### Fixed

- Updated the library-card selector for Jellyfin 12 Modern, where the item `data-type` is carried by the `.card` wrapper.
- Kept the original `.overflowBackdropCard` selector as a compatibility fallback.

### Design decision

The Jellyfin 12 `Card/useCard.ts` source builds the wrapper class from the card shape, while the item data attributes are attached to the wrapper. ExquisiteFin therefore targets `.card[data-type="CollectionFolder"]` / `.card[data-type="UserView"]` directly instead of assuming the legacy shape class is present.

## [0.2.0] - 2026-10-11

### Added

- ExquisiteFin-owned `--exquisite-library-card-height` setting.
- Library card height override targeting the actual `cardPadder-overflowBackdrop` geometry used by ElegantFin.
- Clear separation between upstream compatibility layers, user-facing settings, and ExquisiteFin overrides.

### Design decision

The first visual customization targets library card geometry rather than `.cardScalable`, because the upstream ElegantFin source establishes the CollectionFolder/UserView card ratio through `.cardPadder-overflowBackdrop` padding.

## [0.1.0] - 2026-10-11

### Added

- Initial ExquisiteFin project structure.
- Jellyfin 12 Modern compatibility baseline based on ElegantFin.
- Pinned ElegantFin and ElegantFin-JF12 companion imports.
- Optional ElegantFin Media Bar support import.
- Dedicated ExquisiteFin settings and override sections.

### Design decision

v0.1.0 intentionally makes no visual changes of its own. The first milestone is reproducible compatibility. Visual changes are introduced as isolated, maintainable ExquisiteFin overrides in later releases.
