# ExquisiteFin design notes

## Current baseline

ExquisiteFin is a custom CSS theme for Jellyfin 12 Modern built on ElegantFin and the ElegantFin Jellyfin Modern companion. The active stylesheet is `Theme/ExquisiteFin.css`; it contains all ExquisiteFin-owned overrides and imports the upstream layers first.

The current visual direction is:

- Dark blue-gray surfaces with a restrained teal accent (`#00c79f`).
- Wide collection/library-folder cards and slightly enlarged Continue Watching cards.
- A prominent centered play control and clean, icon-only secondary card actions.
- Persistent semantic colours for selected bookmark, Mark Played, and Favorite states.
- Centered movie synopsis and external rating links.
- A rounded Genres pill beneath the movie hero actions on desktop-sized layouts.
- Clear keyboard focus and hover states.

## CSS structure

The main stylesheet is grouped by purpose:

1. Settings and upstream theme variables.
2. Home and library presentation.
3. Card play and secondary actions.
4. Movie details.
5. General interactive states.

ExquisiteFin-specific rules remain after the upstream imports. Frequently tuned settings are kept near the top of the file rather than scattered through selectors.

## Development approach

Visual changes should be isolated and tested **one at a time** before they are merged into the main stylesheet. When a temporary testing file is useful, it should be removed after its confirmed styling is promoted or discarded.

For layout issues, inspect the actual Jellyfin Modern DOM and the upstream rules before adding overrides. A selector that worked with a legacy layout may not target the same element in Modern.

Desktop, mobile, and TV layouts should be checked separately whenever a change is expected to work across those form factors. Avoid broad hero repositioning rules unless the change has been validated against the full details-page layout.

## Upstream dependencies and licensing

The stylesheet currently imports pinned versions of ElegantFin, its Media Bar plugin support, and the Jellyfin Modern companion. ExquisiteFin is therefore not fully self-contained yet. Gradually replace upstream-dependent pieces where that improves clarity or independence, without modifying the upstream repositories.

ElegantFin is maintained by lscambo13, and the Jellyfin Modern companion by mihaif7. ExquisiteFin is an independent project. See the repository's `LICENSE` file for licensing information.
