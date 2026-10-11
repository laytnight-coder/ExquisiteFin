# Changelog

All notable ExquisiteFin changes are documented here.

## [0.5.0] - 2026-10-11

### Changed

- Increased the size of Continue Watching / resume cards to make the homepage row more visually prominent.
- Set ElegantFin's `--resumeCardScale` to `1.20`, adding variation to the homepage without changing library card geometry.

## [0.4.6] - 2026-10-11

### Fixed

- Fixed selected secondary card-action colours reverting to white when the pointer leaves the icon.
- Increased the specificity of the selected bookmark, Mark Played, and Favorite selectors so Jellyfin 12 Modern's generic white-icon rule cannot override the selected colour when the action is no longer hovered.
- Kept the selected semantic colours persistent: bookmark blue, Mark Played green, and Favorite red.

## [0.4.5] - 2026-10-11

### Fixed

- Corrected selected secondary card-action colours so Jellyfin 12 Modern's generic icon rules cannot override them.
- Selected bookmark icons are blue.
- Selected Mark Played check icons are green.
- Selected Favorite heart icons are red.
- Kept the semantic colours stable while hovering selected actions.
- Used Jellyfin's existing `playstatebutton-icon-played` and `ratingbutton-icon-withrating` state classes, with Modern-layout-specific selectors for the enlarged icon controls.

## [0.4.4] - 2026-10-11

### Changed

- Increased the clean secondary card action icons to approximately twice their previous visual size.
- Increased the clickable icon area to keep the larger controls comfortable to use.
- Kept the simple white icon-only treatment with no circles, borders, glass, or idle glow.
- Kept the three-dot/menu action explicitly hidden.

## [0.4.3] - 2026-10-11

### Changed

- Reworked the secondary card actions from the glass/circular treatment to a clean icon-only style inspired by the reference design.
- Removed secondary-button borders, backgrounds, blur, and idle glow.
- Kept the secondary icons white with a subtle shadow for readability over poster artwork.
- Added restrained teal hover and active states without turning the controls into glowing discs.
- Explicitly hides the card menu/three-dot action so it cannot reappear through the Modern layout.
- Kept the primary centered play button unchanged.

### Design decision

The primary play button remains the visual hero. Secondary actions are now intentionally lightweight: simple white icons with spacing and only subtle interaction feedback.

## [0.4.2] - 2026-10-11

### Changed

- Redesigned the secondary card actions into a compact bottom-right control group.
- Reduced the secondary buttons to a smaller, consistent circular size so they no longer compete visually with the primary play control.
- Added a dark translucent glass-style background with subtle blur for better icon contrast across poster artwork.
- Added consistent spacing and inset positioning for the action group.
- Removed idle glow from secondary actions and reserved the teal glow for hover/interaction states.
- Added teal active-state icon styling for supported pressed/active controls.

### Design decision

The large centered play button remains the hero interaction. Secondary actions now use a quieter glass-and-outline treatment so the card has a clearer visual hierarchy while retaining ExquisiteFin's teal identity.

## [0.3.7] - 2026-10-11

### Changed

- Increased the centered primary play ring from `5.5em` to `6em`.
- Increased the play symbol from `2.2em` to `3em` for a substantially larger play control.
- Replaced the previous radial/frosted center with a mostly transparent `20%` grey-tinted surface.
- Reduced the backdrop blur to `1px` so the poster remains clearly visible through the control.

## [0.3.6] - 2026-10-11

### Changed

- Increased the centered primary card play ring from `5em` to `5.5em`.
- Increased the play symbol substantially to `2.2em` so it is much more prominent inside the larger control.
- Added a subtle frosted-glass blur and radial gradient to the transparent center of the play control.
- Added a slightly stronger teal glow while keeping the center translucent rather than solid.

## [0.3.5] - 2026-10-11

### Changed

- Increased the centered primary card play button from `4em` to `5em`.
- Increased the play symbol substantially so it reads clearly inside the larger control.
- Increased the outline and glow slightly to keep the larger button visually defined.

## [0.3.4] - 2026-10-11

### Changed

- Increased the centered primary card play button from `3em` to `4em` for a more prominent control on poster cards.
- Slightly increased the play icon size and restrained the hover scale so the larger control remains balanced.

## [0.3.3] - 2026-10-11

### Fixed

- Corrected the primary card play button positioning so the enlarged teal-outlined control remains centered on the card.
- Explicitly restored the Jellyfin card overlay's center positioning, preventing the button from inheriting the bottom action-button position in the Jellyfin 12 Modern layout.

### Design decision

The primary play button is now targeted through `.cardOverlayContainer > .cardOverlayFab-primary`, matching Jellyfin's own centered play-button geometry while ExquisiteFin controls only the visual treatment.

## [0.3.2] - 2026-10-11

### Fixed

- Changed the primary card play button from a filled accent control to a transparent button with a teal outline and white play icon.
- Kept the play button visually centered and circular while preserving the existing card action controls.

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
