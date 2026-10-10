# Changelog

All notable ExquisiteFin changes are documented here.

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
