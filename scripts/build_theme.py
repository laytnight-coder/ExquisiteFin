#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEME = ROOT / "Theme"
SOURCE = THEME / "source"
BASE_FILE = SOURCE / "ElegantFin.css"
MODERN_FILE = SOURCE / "Jellyfin12-Modern.css"
MEDIA_FILE = SOURCE / "MediaBar-ElegantFin.css"
OVERRIDES_FILE = SOURCE / "ExquisiteFin-overrides.css"
HEADER_FILE = SOURCE / "ExquisiteFin-header.css"
BUNDLE_FILE = THEME / "ExquisiteFin.css"
MEDIA_BUNDLE_FILE = THEME / "ExquisiteFin-MediaBar.css"
VERSION = "0.6.3"


def read_css(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def trim_base(css: str) -> tuple[str, str]:
    imports = re.findall(r'@import\s+url\(([^)]+)\);', css)
    font_import = next((f'@import url({value});' for value in imports if "fonts.googleapis.com" in value), "")
    css = re.sub(r'@import\s+url\(([^)]+)\);\s*', '', css)
    return css.strip(), font_import


def trim_modern(css: str) -> tuple[str, str, str]:
    lines = css.splitlines()
    media_start = None
    media_end = None
    for index, line in enumerate(lines):
        if "basic styling for the Media Bar Plugin - start" in line:
            media_start = index
        if media_start is not None and "basic styling for the Media Bar Plugin - end" in line:
            media_end = index + 1
            break

    if media_start is None or media_end is None:
        raise ValueError("Could not locate the Modern Media Bar section.")

    core = "\n".join(lines[:media_start] + lines[media_end:]).strip()
    media = "\n".join(lines[media_start:media_end]).strip()

    # This TV-specific rule only targets the Media Bar slideshow. Move it into
    # the optional adapter rather than loading it for users without that plugin.
    tv_media_rule_pattern = re.compile(
        r":root\.layout-tv #slides-container \.backdrop-container\s*\{\s*"
        r"bottom: 0;\s*height: auto;\s*\}\s*"
    )
    tv_media_rule_match = tv_media_rule_pattern.search(core)
    if tv_media_rule_match is None:
        raise ValueError("Expected one TV Media Bar rule to move, found 0.")
    tv_media_rule = tv_media_rule_match.group(0)
    core, rule_count = tv_media_rule_pattern.subn("", core)
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
    header = read_css(HEADER_FILE).strip()

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
    bundle = f"{bundle_header}{font_import}\n\n{base}\n\n{modern.strip()}\n\n{overrides}\n\n{header}\n"

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
        raise ValueError("Third-party plugin selectors remain in the Modern core.")

    return bundle, adapter


def main() -> int:
    bundle, adapter = build()
    check_only = "--check" in __import__("sys").argv[1:]
    if check_only:
        print("Theme bundle validation passed.")
        return 0
    BUNDLE_FILE.write_text(bundle, encoding="utf-8")
    MEDIA_BUNDLE_FILE.write_text(adapter, encoding="utf-8")
    print(f"Wrote {BUNDLE_FILE}")
    print(f"Wrote {MEDIA_BUNDLE_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
