#!/usr/bin/env python3
"""Build ExquisiteFin's local CSS bundle and optional Media Bar adapter.

Keep attributed upstream inputs and ExquisiteFin-owned overrides in
Theme/source/. The main output bundles the supported core plus Jellyfin 12
Modern rules. Media Bar-specific rules are generated as a separate adapter.

Run:
    python scripts/build_theme.py
Validate without writing:
    python scripts/build_theme.py --check
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Theme" / "source"
THEME = ROOT / "Theme"

BASE_FILE = SOURCE / "ElegantFin.css"
MODERN_FILE = SOURCE / "Jellyfin12-Modern.css"
MEDIA_FILE = SOURCE / "MediaBar-ElegantFin.css"
OVERRIDES_FILE = SOURCE / "ExquisiteFin-overrides.css"
BUNDLE_FILE = THEME / "ExquisiteFin.css"
MEDIA_ADAPTER_FILE = THEME / "ExquisiteFin-MediaBar.css"

VERSION = "0.6.3"
OMIT_MODERN_SECTIONS = {12, 14, 18}


def read_css(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def find_modern_sections(css: str) -> tuple[list[str], list[dict[str, int]]]:
    lines = css.splitlines()
    headings: list[dict[str, int]] = []
    for index, line in enumerate(lines):
        match = re.match(r"^\s*\*\s*(\d+)\.\s+", line)
        if not match:
            continue
        start = index
        while start > 0 and not re.match(r"^\s*/\*\s*═", lines[start]):
            start -= 1
        headings.append({"number": int(match.group(1)), "start": start, "heading": index})

    sections: list[dict[str, int]] = []
    for index, section in enumerate(headings):
        end = headings[index + 1]["start"] if index + 1 < len(headings) else len(lines)
        sections.append({**section, "end": end})
    if not sections or sections[0]["number"] != 1:
        raise ValueError("Could not identify numbered sections in the Modern source.")
    return lines, sections


def trim_base(css: str) -> tuple[str, str]:
    """Keep shared theme rules; remove optional plugins and disabled experiments."""
    lines = css.splitlines()
    font_import = next(
        (
            line.strip()
            for line in lines
            if line.lstrip().startswith(
                '@import url("https://fonts.googleapis.com/css2?family=Inter:'
            )
        ),
        None,
    )
    if not font_import:
        raise ValueError("Expected upstream Inter stylesheet import was not found.")

    cleaned_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped == font_import:
            continue
        if stripped in {
            "/* Add-ons: Uncomment to enable */",
            "/* @import url(./assets/add-ons/media-bar-plugin-support-nightly.css); */",
            '/* @import url("https://cdn.jsdelivr.net/gh/lscambo13/ElegantFin@main/Theme/assets/add-ons/custom-media-covers-latest-min.css"); */',
            "/* Material Symbols Rounded - Minimal */",
        }:
            continue
        if stripped.startswith("/* https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:"):
            continue
        cleaned_lines.append(line)
    css = "\n".join(cleaned_lines)

    # Media Bar styles are moved into Theme/ExquisiteFin-MediaBar.css.
    css = re.sub(
        r"/\* basic styling for the Media Bar Plugin - start[\s\S]*?"
        r"/\* basic styling for the Media Bar Plugin - end \*/\s*",
        "",
        css,
    )

    # Drop optional Jellyfin Enhanced-only external-link and review styling.
    css = re.sub(
        r"/\* Support for Jellyfin Enhanced "
        r"\(https://github\.com/n00bcodr/Jellyfin-Enhanced\) \*/[\s\S]*?(?=\.itemTags,)",
        "",
        css,
    )
    css = re.sub(
        r"/\* Support \.tmdb-review-swipe-container for Jellyfin Enhanced[\s\S]*?\*/\s*"
        r"\.tmdb-review-swipe-container\s*\{[^}]*\}\s*",
        "",
        css,
    )

    # Remove the optional KefinTweaks selector without disturbing the shared
    # collection/program-guide layout rule next to it.
    group_start = css.find(".collectionItems,\n.programGuideSection,")
    next_collection_rule = css.find(".collectionItems {", group_start + 1)
    if group_start >= 0 and next_collection_rule > group_start:
        replacement = (
            ".collectionItems,\n"
            ".programGuideSection {\n"
            "    grid-column: 1 / -1;\n"
            "}\n\n"
        )
        css = css[:group_start] + replacement + css[next_collection_rule:]
    css = re.sub(r"\.series-episodes-section\s*\{\s*order:\s*4;\s*\}\s*", "", css)

    # ElegantFin positions the primary card play button near a card corner.
    # ExquisiteFin explicitly supplies the complete centered positioning, so
    # keep the shared visual rule below but omit this redundant position block.
    css = re.sub(
        r"\.cardOverlayContainer > \.cardOverlayFab-primary\s*\{\s*"
        r"margin-left: unset;\s*margin-top: unset;\s*top: unset;\s*"
        r"left: calc\(var\(--overlayPlayButtonPosition\) - 1\.5em\);\s*"
        r"bottom: calc\(var\(--overlayPlayButtonPosition\) - 1\.5em\);\s*\}\s*",
        "",
        css,
    )

    # These commented-out performance experiments never ran in the upstream
    # theme. Keep the active low-end-TV fixes that follow them.
    for pattern in (
        r"/\* \.layout-tv \*,[\s\S]*?\*/\s*",
        r"/\* \.layout-tv \.show-focus:not\(\.card\):focus,[\s\S]*?\*/\s*",
        r"/\* \.layout-tv \.blurhash-canvas \{[\s\S]*?\*/\s*",
        r"/\* \.layout-tv \.emby-checkbox:focus \+ span \+ \.checkboxOutline \{[\s\S]*?\*/\s*",
    ):
        css = re.sub(pattern, "", css)

    css = css.replace(
        '--elegantFinFooterText: "ElegantFin v26.09.05";',
        f'--elegantFinFooterText: "ExquisiteFin v{VERSION}";',
    )
    if ".series-episodes-section" in css:
        raise ValueError("KefinTweaks selector cleanup failed.")
    if re.search(r"\.cardOverlayContainer > \.cardOverlayFab-primary\s*\{", css):
        raise ValueError("Redundant ElegantFin primary-play positioning remains.")
    return css.strip(), font_import


def trim_modern(css: str) -> tuple[str, str, str]:
    """Bundle core compatibility; return optional Media Bar rules separately."""
    lines, sections = find_modern_sections(css)
    media_section = next((s for s in sections if s["number"] == 12), None)
    if media_section is None:
        raise ValueError("Could not find Modern companion section 12 (Media Bar).")

    parts: list[str] = []
    cursor = 0
    for section in sections:
        if cursor < section["start"]:
            parts.append("\n".join(lines[cursor:section["start"]]))
        if section["number"] not in OMIT_MODERN_SECTIONS:
            parts.append("\n".join(lines[section["start"]:section["end"]]))
        cursor = section["end"]
    if cursor < len(lines):
        parts.append("\n".join(lines[cursor:]))
    core = "\n".join(parts).strip() + "\n"
    media = "\n".join(lines[media_section["start"]:media_section["end"]]).strip()

    # This TV-specific rule only targets the Media Bar slideshow. Move it into
    # the optional adapter rather than loading it for users without that plugin.
    tv_media_rule_pattern = re.compile(
        r":root\.layout-tv #slides-container \.backdrop-container\s*\{\s*"
        r"bottom: 0;\s*height: auto;\s*\}\s*"
    )
    tv_media_rule, rule_count = tv_media_rule_pattern.subn("", core)
    if rule_count != 1:
        raise ValueError(
            f"Expected one TV Media Bar rule to move, found {rule_count}."
        )

    core = core.replace(
        '/*! ElegantFin for Jellyfin 12 "Modern" layout | v26.10.07 | GPL-2.0\n'
        " *  https://github.com/mihaif7/elegantfin-jf12\n"
        " *  Load AFTER upstream ElegantFin. See the README for install. */",
        '/*! ElegantFin for Jellyfin 12 "Modern" layout | v26.10.07 | GPL-2.0\n'
        " *  https://github.com/mihaif7/elegantfin-jf12\n"
        f" *  Vendored into ExquisiteFin v{VERSION}; attributed sources are in Theme/source/. */",
    )
    core = core.strip() + "\n"
    return core, media, tv_media_rule.strip()


def balanced_css(css: str) -> bool:
    depth = 0
    quote: str | None = None
    comment = False
    index = 0
    while index < len(css):
        char = css[index]
        next_char = css[index + 1] if index + 1 < len(css) else ""
        if comment:
            if char == "*" and next_char == "/":
                comment = False
                index += 2
                continue
            index += 1
            continue
        if quote is not None:
            if char == "\\":
                index += 2
                continue
            if char == quote:
                quote = None
            index += 1
            continue
        if char == "/" and next_char == "*":
            comment = True
            index += 2
            continue
        if char in ("'", '"'):
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth < 0:
                return False
        index += 1
    return depth == 0 and quote is None and not comment


def strip_comments(css: str) -> str:
    return re.sub(r"/\*[\s\S]*?\*/", "", css)


def build() -> tuple[str, str]:
    base, font_import = trim_base(read_css(BASE_FILE))
    modern, media_modern, media_tv_rule = trim_modern(read_css(MODERN_FILE))
    media_legacy = read_css(MEDIA_FILE).strip()
    overrides = read_css(OVERRIDES_FILE).strip()

    bundle_header = (
        "/*!\n"
        f" * ExquisiteFin v{VERSION} — self-contained theme bundle\n"
        " *\n"
        " * Includes selectively trimmed and adapted GPL-2.0 code from:\n"
        " * - ElegantFin v26.09.05 by lscambo13\n"
        " * - ElegantFin Jellyfin 12 Modern v26.10.07 by mihaif7\n"
        " * Original upstream attribution is preserved in the bundled sections\n"
        " * and source copies. No upstream theme stylesheet imports are required.\n"
        " */\n"
    )
    bundle = f"{bundle_header}{font_import}\n\n{base}\n\n{modern.strip()}\n\n{overrides}\n"

    media_header = (
        "/*!\n"
        f" * ExquisiteFin Media Bar Adapter v{VERSION} — optional plugin stylesheet\n"
        " * Derived from ElegantFin Media Bar support v26.09.05 (lscambo13) and\n"
        " * Modern companion v26.10.07 (mihaif7). Both are GPL-2.0.\n"
        " * Load after Theme/ExquisiteFin.css. Omit this adapter without Media Bar.\n"
        " */\n"
    )
    adapter = (
        f"{media_header}\n{media_legacy}\n\n{media_modern}\n\n"
        f"/* Modern TV slideshow adaptation; only used with Media Bar. */\n"
        f"{media_tv_rule}\n"
    )

    if not balanced_css(bundle):
        raise ValueError("The built core bundle failed CSS structure validation.")
    if not balanced_css(adapter):
        raise ValueError("The Media Bar adapter failed CSS structure validation.")

    active_imports = re.findall(r"@import\s+[^;]+;", strip_comments(bundle))
    if len(active_imports) != 1 or "fonts.googleapis.com" not in active_imports[0]:
        raise ValueError(f"Unexpected active core imports: {active_imports!r}")
    if "basic styling for the Media Bar Plugin - start" in base:
        raise ValueError("Media Bar core rules were not removed.")
    if re.search(r"\.cardOverlayContainer > \.cardOverlayFab-primary\s*\{", base):
        raise ValueError("Redundant primary-play positioning remains in the core.")
    if ":root.layout-tv #slides-container .backdrop-container" in modern:
        raise ValueError("TV-specific Media Bar rule remains in the core.")
    if ":root.layout-tv #slides-container .backdrop-container" not in adapter:
        raise ValueError("TV-specific Media Bar rule is missing from the adapter.")
    if ".series-episodes-section" in base:
        raise ValueError("KefinTweaks selectors were not removed.")
    if any(
        token in modern
        for token in ("#slides-container:has(.slide-content)", "[data-jf-ieg-root", "Jellyfin Enhanced")
    ):
        raise ValueError("An optional plugin-only Modern section remains in the core.")
    return bundle, adapter


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate without writing output files")
    args = parser.parse_args()
    bundle, adapter = build()
    if args.check:
        print(f"Core bundle: {len(bundle):,} characters; structure OK")
        print(f"Media Bar adapter: {len(adapter):,} characters; structure OK")
        print("Core has no upstream theme stylesheet imports.")
        return 0
    BUNDLE_FILE.write_text(bundle, encoding="utf-8")
    MEDIA_ADAPTER_FILE.write_text(adapter, encoding="utf-8")
    print(f"Wrote {BUNDLE_FILE.relative_to(ROOT)} ({len(bundle):,} characters)")
    print(f"Wrote {MEDIA_ADAPTER_FILE.relative_to(ROOT)} ({len(adapter):,} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
