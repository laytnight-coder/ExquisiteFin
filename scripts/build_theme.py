#!/usr/bin/env python3
"""Build ExquisiteFin's self-contained CSS bundle and optional Media Bar adapter.

Sources are kept in Theme/source/ with their upstream attribution intact.
The distributable Theme/ExquisiteFin.css bundles the required core and
Jellyfin 12 Modern compatibility rules. Plugin-only Modern sections are omitted
from the core and the Media Bar section is moved to a separate optional file.

Run from any working directory:
    python scripts/build_theme.py
Check without writing:
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
VERSION = "0.6.0"
OMIT_MODERN_SECTIONS = {12, 14, 18}


def read_css(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def modern_section_ranges(css: str) -> tuple[list[str], list[dict[str, int]]]:
    """Find numbered Modern companion sections and their separator comments."""
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
        raise ValueError("Could not identify numbered sections in the Modern companion.")
    return lines, sections


def trim_base(css: str) -> tuple[str, str]:
    """Return the base theme without optional plugin rules, and its font import."""
    font_pattern = re.compile(
        r'^\s*@import url\("https://fonts\.googleapis\.com/css2\?family=Inter:[^;]+;\s*',
        re.MULTILINE,
    )
    font_match = font_pattern.search(css)
    if not font_match:
        raise ValueError("Expected upstream Inter font import was not found.")
    font_import = font_match.group(0).strip()
    css = css[: font_match.start()] + css[font_match.end() :]

    # Remove inactive, commented-out add-on import examples from the bundle.
    css = re.sub(
        r"/\* Add-ons: Uncomment to enable \*/\s*"
        r"/\* @import url\(\./assets/add-ons/media-bar-plugin-support-nightly\.css\); \*/\s*"
        r'/\* @import url\("https://cdn\.jsdelivr\.net/gh/lscambo13/ElegantFin@main/Theme/assets/add-ons/custom-media-covers-latest-min\.css"\); \*/\s*',
        "",
        css,
    )
    # Remove a long, commented full icon-font request URL; the @font-face
    # declarations immediately below provide the actual font sources.
    css = re.sub(
        r"/\* Material Symbols Rounded - Minimal \*/\s*"
        r"/\* https://fonts\.googleapis\.com/css2\?family=Material\+Symbols\+Rounded:[\s\S]*?\*/\s*",
        "",
        css,
    )

    # Media Bar styles live in the optional ExquisiteFin-MediaBar.css adapter.
    css = re.sub(
        r"/\* basic styling for the Media Bar Plugin - start[\s\S]*?"
        r"/\* basic styling for the Media Bar Plugin - end \*/\s*",
        "",
        css,
    )

    # Exclude only integrations that explicitly style optional plugins.
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
    css = re.sub(
        r"\.collectionItems,\s*\.programGuideSection,\s*"
        r"/\* Support \.series-episodes-section for KefinTweaks "
        r"\(https://github\.com/ranaldsgift/KefinTweaks\) \*/\s*"
        r"\.series-episodes-section,\s*"
        r"\.series-episodes-section ~ #listChildrenCollapsible\s*\{[^}]*\}\s*"
        r"\.series-episodes-section\s*\{\s*order:\s*4;\s*\}",
        ".collectionItems,\n.programGuideSection {\n    grid-column: 1 / -1;\n}",
        css,
    )

    # Drop disabled low-end-TV experiments, but retain the active TV fixes.
    css = re.sub(r"/\* \.layout-tv \*,[\s\S]*?\*/\s*", "", css)
    css = re.sub(r"/\* \.layout-tv \.show-focus:not\(\.card\):focus,[\s\S]*?\*/\s*", "", css)
    css = re.sub(r"/\* \.layout-tv \.blurhash-canvas \{[\s\S]*?\*/\s*", "", css)
    css = re.sub(
        r"/\* \.layout-tv \.emby-checkbox:focus \+ span \+ \.checkboxOutline \{[\s\S]*?\*/\s*",
        "",
        css,
    )

    css = css.replace(
        '--elegantFinFooterText: "ElegantFin v26.09.05";',
        f'--elegantFinFooterText: "ExquisiteFin v{VERSION}";',
    )
    return css.strip(), font_import


def trim_modern(css: str) -> tuple[str, str]:
    """Return core Modern rules and the extracted Media Bar section."""
    lines, sections = modern_section_ranges(css)
    media = next((section for section in sections if section["number"] == 12), None)
    if media is None:
        raise ValueError("Modern companion Media Bar section 12 was not found.")

    core_parts: list[str] = []
    cursor = 0
    for section in sections:
        if cursor < section["start"]:
            core_parts.append("\n".join(lines[cursor : section["start"]]))
        if section["number"] not in OMIT_MODERN_SECTIONS:
            core_parts.append("\n".join(lines[section["start"] : section["end"]]))
        cursor = section["end"]
    if cursor < len(lines):
        core_parts.append("\n".join(lines[cursor:]))
    core = "\n".join(core_parts).strip() + "\n"

    media_section = "\n".join(lines[media["start"] : media["end"]]).strip()
    core = core.replace(
        '/*! ElegantFin for Jellyfin 12 "Modern" layout | v26.10.07 | GPL-2.0\n'
        " *  https://github.com/mihaif7/elegantfin-jf12\n"
        " *  Load AFTER upstream ElegantFin. See the README for install. */",
        '/*! ElegantFin for Jellyfin 12 "Modern" layout | v26.10.07 | GPL-2.0\n'
        " *  https://github.com/mihaif7/elegantfin-jf12\n"
        f" *  Vendored into ExquisiteFin v{VERSION}; see Theme/source/ for attributed sources. */",
    )
    return core, media_section


def braces_balanced(css: str) -> bool:
    """Check braces while ignoring comments and quoted strings."""
    depth = 0
    quote: str | None = None
    in_comment = False
    index = 0
    while index < len(css):
        char = css[index]
        next_char = css[index + 1] if index + 1 < len(css) else ""
        if in_comment:
            if char == "*" and next_char == "/":
                in_comment = False
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
            in_comment = True
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
    return depth == 0 and quote is None and not in_comment


def without_comments(css: str) -> str:
    """Strip comments before checking active @import declarations."""
    return re.sub(r"/\*[\s\S]*?\*/", "", css)


def build() -> tuple[str, str]:
    base, font_import = trim_base(read_css(BASE_FILE))
    modern, modern_media = trim_modern(read_css(MODERN_FILE))
    media_support = read_css(MEDIA_FILE).strip()
    overrides = read_css(OVERRIDES_FILE).strip()

    header = (
        "/*!\\n"
        f" * ExquisiteFin v{VERSION} — self-contained theme bundle\\n"
        " *\\n"
        " * Includes selectively trimmed and adapted GPL-2.0 code from:\\n"
        " * - ElegantFin v26.09.05 by lscambo13\\n"
        " * - ElegantFin Jellyfin 12 Modern v26.10.07 by mihaif7\\n"
        " * Original upstream attribution is preserved in the bundled sections\\n"
        " * and source copies. No upstream theme stylesheet imports are required.\\n"
        " */\\n"
    )
    bundle = f"{header}{font_import}\\n\\n{base}\\n\\n{modern.strip()}\\n\\n{overrides}\\n"

    media_header = (
        "/*!\\n"
        f" * ExquisiteFin Media Bar Adapter v{VERSION} — optional plugin stylesheet\\n"
        " * Derived from ElegantFin Media Bar support v26.09.05 (lscambo13) and\\n"
        " * Modern companion v26.10.07 (mihaif7). Both are GPL-2.0.\\n"
        " * Load after Theme/ExquisiteFin.css. Omit this adapter without Media Bar.\\n"
        " */\\n"
    )
    media_adapter = f"{media_header}\\n{media_support}\\n\\n{modern_media}\\n"

    if not braces_balanced(bundle):
        raise ValueError("Generated theme bundle failed CSS brace/string validation.")
    if not braces_balanced(media_adapter):
        raise ValueError("Generated Media Bar adapter failed CSS brace/string validation.")

    active_imports = re.findall(r"@import\\s+[^;]+;", without_comments(bundle))
    if len(active_imports) != 1 or "fonts.googleapis.com" not in active_imports[0]:
        raise ValueError(f"Unexpected imports in the core bundle: {active_imports!r}")
    if "basic styling for the Media Bar Plugin - start" in base:
        raise ValueError("Media Bar base rules were not removed from the core.")
    if ".series-episodes-section" in base:
        raise ValueError("KefinTweaks selectors remain in the core base.")
    if any(token in modern for token in ("#slides-container:has(.slide-content)", "[data-jf-ieg-root", "Jellyfin Enhanced")):
        # A generic mention of Jellyfin Enhanced is only allowed in attribution
        # comments; plugin selectors should not remain in the Modern core.
        raise ValueError("Optional plugin sections remain in the core Modern layer.")
    return bundle, media_adapter


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate and report output sizes without writing files",
    )
    args = parser.parse_args()
    bundle, adapter = build()
    if args.check:
        print(f"Core bundle: {len(bundle):,} characters; CSS structure OK")
        print(f"Media Bar adapter: {len(adapter):,} characters; CSS structure OK")
        print("No upstream theme stylesheet imports in the core bundle.")
        return 0
    BUNDLE_FILE.write_text(bundle, encoding="utf-8")
    MEDIA_ADAPTER_FILE.write_text(adapter, encoding="utf-8")
    print(f"Wrote {BUNDLE_FILE.relative_to(ROOT)} ({len(bundle):,} characters)")
    print(f"Wrote {MEDIA_ADAPTER_FILE.relative_to(ROOT)} ({len(adapter):,} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
