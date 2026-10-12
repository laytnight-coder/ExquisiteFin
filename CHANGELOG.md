# Changelog

All notable ExquisiteFin changes are documented here.

## [0.6.4] - 2026-10-12

### Changed

- Promoted the accepted Jellyfin 12 Modern header navigation styling into the main `Theme/ExquisiteFin.css` bundle.
- Restored the complete main CSS bundle after the temporary `PLACEHOLDER` file was identified on `main`.
- Kept the optional Media Bar support in the separate `Theme/ExquisiteFin-MediaBar.css` adapter.
- Removed the temporary header-navigation test stylesheet.
- Removed the vendored source tree and build script now that the maintained distributable CSS bundles are the repository outputs.
- Removed the GitHub Actions theme-build workflow because there is no longer a generated build step.
- Updated the README and design notes to reflect the simplified distributable layout.

### Notes

- No experimental library-toolbar negative-margin rule is included.
- The browser library spacing remains untouched because it was already correct.
- A live Jellyfin visual smoke test is recommended after updating the CDN import.

## [0.6.3] - 2026-10-12

### Changed

- Restyled the header's library navigation as flat text-and-icon links, closer to Jellyfin's default appearance.
- Removed the pill background, rounded corners, and button shadow from header library tabs.
- Kept inactive links light and highlighted the active page with the ExquisiteFin teal accent.
- Made hover/focus states remain flat instead of restoring pill backgrounds.

## [0.6.2] - 2026-10-12

### Changed

- Increased the desktop card-indicator left inset from `0.225em` to `0.5em`, matching ElegantFin's existing top inset.
- Added a mobile-specific `0.45em` left inset to match ElegantFin's smaller mobile top inset.
- Kept the indicator group left-aligned and preserved the existing colours, size, and indicator appearance.

## [0.6.1] - 2026-10-12

### Changed

- Moved the Modern companion's TV-specific Media Bar slideshow backdrop rule from the core bundle into the optional `Theme/ExquisiteFin-MediaBar.css` adapter.
- Removed ElegantFin's default lower-corner positioning rule for the primary card play button from the generated core bundle; ExquisiteFin's own centered positioning remains authoritative.
- Updated the build script so both optimizations are reproducible from the preserved, attributed source files.

### Notes

- The core bundle is 326 characters smaller than v0.6.0; this is a correctness/maintenance cleanup rather than a meaningful runtime performance change.
- The InPlayerEpisodePreview progress rule remains in core until plugin use is confirmed, since the rule is small and safe to leave available.
- CSS structure and active imports were checked. A live Jellyfin visual smoke test is still recommended after updating.
