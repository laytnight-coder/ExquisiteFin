# ExquisiteFin design notes

## v0.1 baseline

ExquisiteFin is being developed as an independent theme for Jellyfin 12's
Modern UI, using ElegantFin as its starting point.

The first release is deliberately conservative:

- ElegantFin remains the visual baseline.
- The Jellyfin 12 Modern companion is loaded after ElegantFin.
- ExquisiteFin-owned CSS is kept after all upstream imports.
- No one-off browser/DevTools edits are treated as part of the theme.
- Visual changes will be introduced one component at a time and recorded in
a versioned changelog.

## Planned development order

1. Verify the v0.1 baseline in Jellyfin 12 Modern.
2. Establish ExquisiteFin's variables/settings section.
3. Fix library-card sizing using the actual Modern UI DOM and ElegantFin rules.
4. Refine cards, buttons, borders, glow, spacing, navigation, and typography.
5. Review other Jellyfin themes for design ideas and selectively recreate useful
   features in ExquisiteFin.
6. Replace upstream-dependent pieces over time where independence is useful.

## Source/licensing

ElegantFin is GPL-2.0 licensed. ExquisiteFin is intended to remain compatible
with that licensing model while keeping ExquisiteFin-owned changes clearly
separated from upstream-origin material.
