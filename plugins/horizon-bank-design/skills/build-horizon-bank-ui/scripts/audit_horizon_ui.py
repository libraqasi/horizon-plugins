#!/usr/bin/env python3
"""Audit frontend source for Horizon palette drift and common UI hazards."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


APPROVED_HEX = {
    "#D71E28", "#B01B24", "#FFCD41", "#FFFFFF", "#141414", "#675F5F",
    "#787070", "#E2DEDE", "#F4F0ED", "#F9F7F6", "#5A469B", "#178757",
    "#A93E00", "#87190A", "#EB691E", "#D73F26", "#C83255", "#AA1E87",
    "#823291", "#352B6B", "#463782", "#9A89D9", "#BFB3F2",
}

SOURCE_SUFFIXES = {
    ".css", ".scss", ".sass", ".less", ".html", ".htm", ".jsx", ".tsx",
    ".js", ".ts", ".vue", ".svelte", ".json",
}

IGNORED_DIRS = {
    ".git", ".next", ".nuxt", "build", "coverage", "dist", "node_modules",
    "out", "vendor",
}

HEX_RE = re.compile(r"(?<![\w-])#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})(?![0-9a-fA-F])")
SINGLE_H_MARK_RE = re.compile(
    r'className=[{]?[\"\'][^\"\']*(?:brand|customer)[-_]mark[^\"\']*[\"\'][^>]*>\s*H\s*<',
    re.I,
)


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    line: int
    message: str


def normalize_hex(value: str) -> str:
    value = value.strip().upper()
    if not value.startswith("#"):
        value = f"#{value}"
    if len(value) == 4:
        value = "#" + "".join(character * 2 for character in value[1:])
    if not re.fullmatch(r"#[0-9A-F]{6}", value):
        raise ValueError(f"Invalid hex color: {value}")
    return value


def channel_to_linear(value: int) -> float:
    channel = value / 255
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def luminance(value: str) -> float:
    normalized = normalize_hex(value)
    red, green, blue = (
        int(normalized[index:index + 2], 16) for index in (1, 3, 5)
    )
    return (
        0.2126 * channel_to_linear(red)
        + 0.7152 * channel_to_linear(green)
        + 0.0722 * channel_to_linear(blue)
    )


def contrast_ratio(foreground: str, background: str) -> float:
    first, second = luminance(foreground), luminance(background)
    lighter, darker = max(first, second), min(first, second)
    return (lighter + 0.05) / (darker + 0.05)


def iter_source_files(targets: Iterable[Path]) -> Iterable[Path]:
    seen: set[Path] = set()
    for target in targets:
        if target.is_file():
            candidates = [target]
        elif target.is_dir():
            candidates = (
                path
                for path in target.rglob("*")
                if path.is_file()
                and not any(part in IGNORED_DIRS for part in path.parts)
            )
        else:
            print(f"warning: target not found: {target}", file=sys.stderr)
            continue
        for path in candidates:
            if path.suffix.lower() not in SOURCE_SUFFIXES:
                continue
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                yield path


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def scan_file(path: Path, allowed: set[str], forbidden: list[str]) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []

    findings: list[Finding] = []
    display_path = str(path)

    for match in HEX_RE.finditer(text):
        color = normalize_hex(match.group(0))
        if color not in allowed:
            findings.append(Finding(
                "warning",
                "HB001",
                display_path,
                line_number(text, match.start()),
                f"Undocumented color {color}; use a semantic Horizon token or pass --allow.",
            ))

    hazard_patterns = [
        (
            "error",
            "A11Y001",
            re.compile(r"\boutline\s*:\s*(?:none|0(?:px)?)\b", re.I),
            "Focus outline is removed. Provide a visible :focus-visible replacement.",
        ),
        (
            "error",
            "A11Y002",
            re.compile(r"<meta[^>]+name=[\"']viewport[\"'][^>]+user-scalable\s*=\s*no", re.I),
            "Viewport disables zoom. Allow users to magnify content.",
        ),
        (
            "warning",
            "A11Y003",
            re.compile(r"<(?:div|span)\b[^>]*\bonclick\s*=", re.I),
            "A non-semantic element has a click handler. Prefer a native button or link.",
        ),
        (
            "warning",
            "A11Y004",
            re.compile(r"\bautoplay\b", re.I),
            "Autoplay requires pause, sound, motion, and reduced-motion handling.",
        ),
        (
            "warning",
            "SEC001",
            re.compile(r"target=[\"']_blank[\"'](?![^>]*\brel=[\"'][^\"']*noopener)", re.I),
            "A new-window link may be missing rel=\"noopener\".",
        ),
        (
            "error",
            "HB002",
            SINGLE_H_MARK_RE,
            "Horizon identity uses a single H. Use the HB monogram or bundled logo.",
        ),
    ]

    for severity, code, pattern, message in hazard_patterns:
        for match in pattern.finditer(text):
            findings.append(Finding(
                severity,
                code,
                display_path,
                line_number(text, match.start()),
                message,
            ))

    for forbidden_term in forbidden:
        pattern = re.compile(re.escape(forbidden_term), re.I)
        for match in pattern.finditer(text):
            findings.append(Finding(
                "error",
                "HB003",
                display_path,
                line_number(text, match.start()),
                f"Cross-brand identity term found: {forbidden_term!r}. Replace it with Horizon identity.",
            ))

    for match in re.finditer(r"<img\b[^>]*>", text, re.I | re.S):
        tag = match.group(0)
        if not re.search(r"\balt\s*=", tag, re.I):
            findings.append(Finding(
                "error",
                "A11Y005",
                display_path,
                line_number(text, match.start()),
                "Image is missing an alt attribute. Add meaningful alt text or alt=\"\" when decorative.",
            ))

    return findings


def parse_allow(values: list[str]) -> set[str]:
    result = set(APPROVED_HEX)
    for raw in values:
        for value in raw.split(","):
            if value.strip():
                result.add(normalize_hex(value))
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit frontend files for Horizon palette drift, identity errors, and accessibility hazards."
    )
    parser.add_argument("targets", nargs="*", type=Path, help="Source files or directories to scan.")
    parser.add_argument(
        "--allow",
        action="append",
        default=[],
        metavar="#RRGGBB",
        help="Allow an additional documented color. Repeat or pass comma-separated values.",
    )
    parser.add_argument(
        "--forbid",
        action="append",
        default=[],
        metavar="TEXT",
        help="Flag a cross-brand name, prefix, or identity term. Repeat as needed.",
    )
    parser.add_argument("--strict", action="store_true", help="Fail on warnings as well as errors.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument(
        "--contrast",
        nargs=2,
        metavar=("FOREGROUND", "BACKGROUND"),
        help="Calculate a WCAG contrast ratio instead of scanning source.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.contrast:
        foreground, background = map(normalize_hex, args.contrast)
        ratio = contrast_ratio(foreground, background)
        result = {
            "foreground": foreground,
            "background": background,
            "ratio": round(ratio, 2),
            "aa_normal_text": ratio >= 4.5,
            "aa_large_text": ratio >= 3,
            "aa_non_text": ratio >= 3,
        }
        print(json.dumps(result, indent=2) if args.json else (
            f"{foreground} on {background}: {ratio:.2f}:1 | "
            f"AA normal {'PASS' if ratio >= 4.5 else 'FAIL'} | "
            f"AA large/non-text {'PASS' if ratio >= 3 else 'FAIL'}"
        ))
        return 0

    if not args.targets:
        print("error: provide at least one source target or --contrast", file=sys.stderr)
        return 2

    allowed = parse_allow(args.allow)
    findings: list[Finding] = []
    files = list(iter_source_files(args.targets))
    for path in files:
        findings.extend(scan_file(path, allowed, args.forbid))
    findings.sort(key=lambda item: (item.path, item.line, item.code))

    if args.json:
        print(json.dumps({
            "files_scanned": len(files),
            "findings": [asdict(item) for item in findings],
        }, indent=2))
    else:
        for item in findings:
            print(
                f"{item.path}:{item.line}: {item.severity.upper()} "
                f"{item.code} {item.message}"
            )
        errors = sum(item.severity == "error" for item in findings)
        warnings = sum(item.severity == "warning" for item in findings)
        print(f"Scanned {len(files)} file(s): {errors} error(s), {warnings} warning(s).")

    has_error = any(item.severity == "error" for item in findings)
    has_warning = any(item.severity == "warning" for item in findings)
    return 1 if has_error or (args.strict and has_warning) else 0


if __name__ == "__main__":
    raise SystemExit(main())
