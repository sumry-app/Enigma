"""Generate Enigma's README visuals as plain SVG.

Run from the repository root:

    python3 assets/src/build_assets.py

Output is deterministic (seeded) and has no dependencies beyond the Python
standard library. Every mark in the images is drawn here; no third-party
imagery is used. The data shown in the concept image comes from the
synthetic example in examples/example_output.json (result P-1).
"""

from __future__ import annotations

import random
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]

# Palette. Color is reserved for meaning: ember marks conflict, haze marks
# insufficient or unresolved evidence. Everything else is ink and bone.
INK = "#0C0C0E"
PANEL = "#141417"
LINE = "#34332F"
DIM = "#8E8A81"
BONE = "#ECE8E1"
EMBER = "#E4502E"
HAZE = "#7FA0CF"

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', 'DejaVu Sans Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, 'Liberation Sans', 'DejaVu Sans', sans-serif"


def f(x: float) -> str:
    """Compact number formatting to keep files small."""
    s = f"{x:.1f}"
    return s[:-2] if s.endswith(".0") else s


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=13, fill=DIM, family=MONO, weight="400", anchor="start", spacing=0.0, extra=""):
    ls = f' letter-spacing="{f(spacing)}"' if spacing else ""
    return (
        f'<text x="{f(x)}" y="{f(y)}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{ls}{extra}>{esc(s)}</text>'
    )


def grain_defs(fid="grain"):
    return (
        f'<filter id="{fid}" x="0" y="0" width="100%" height="100%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7" stitchTiles="stitch"/>'
        '<feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.55 0"/>'
        "</filter>"
    )


# ---------------------------------------------------------------------------
# State textures. Each evidence state has one visual signature.
# ---------------------------------------------------------------------------

def dots(points, fill, opacity=None):
    """Draw dots compactly: one round-capped path per radius bin."""
    op = f' stroke-opacity="{opacity}"' if opacity is not None else ""
    bins: dict[float, list[str]] = {}
    for x, y, r in points:
        if r <= 0.15:
            continue
        key = round(r * 5) / 5
        bins.setdefault(key, []).append(f"M{f(x)} {f(y)}h.01")
    body = "".join(
        f'<path stroke-width="{f(2 * r)}" d="{"".join(segs)}"/>' for r, segs in sorted(bins.items())
    )
    return f'<g fill="none" stroke="{fill}" stroke-linecap="round"{op}>{body}</g>'


def grid(x, y, w, h, step):
    cols = int(w // step)
    rows = int(h // step)
    ox = x + (w - (cols - 1) * step) / 2
    oy = y + (h - (rows - 1) * step) / 2
    for j in range(rows):
        for i in range(cols):
            yield ox + i * step, oy + j * step, (i / max(cols - 1, 1))


def tex_supported(x, y, w, h):
    # Dense, regular halftone: adequate, direct, uncontested.
    pts = [(px, py, 2.5 * min(1.0, 0.35 + t * 3)) for px, py, t in grid(x, y, w, h, 6.5)]
    return dots(pts, BONE)


def tex_no_relationship(x, y, w, h):
    # Regular rings: an affirmative, established absence of effect.
    body = "".join(
        f'<circle cx="{f(px)}" cy="{f(py)}" r="2.3"/>' for px, py, _ in grid(x, y, w, h, 8)
    )
    return f'<g fill="none" stroke="{BONE}" stroke-width="1">{body}</g>'


def tex_contradictory(x, y, w, h):
    # Two opposing halftones, both kept. Neither side is averaged away.
    left, right = [], []
    for px, py, t in grid(x, y, w, h, 6.5):
        if t < 0.47:
            left.append((px, py, 2.6 * (1 - t / 0.47) + 0.5))
        elif t > 0.53:
            right.append((px, py, 2.6 * ((t - 0.53) / 0.47) + 0.5))
    return dots(left, BONE) + dots(right, EMBER)


def tex_missing(x, y, w, h):
    # Evidence that thins out before the declared obligation is met.
    pts = [(px, py, 2.2 * max(0.0, 1 - t / 0.45)) for px, py, t in grid(x, y, w, h, 6.5)]
    outline = (
        f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="none" '
        f'stroke="{HAZE}" stroke-width="1" stroke-dasharray="3 3" stroke-opacity="0.8"/>'
    )
    return dots(pts, HAZE) + outline


def tex_unknown(x, y, w, h, seed=11):
    # Irregular grain: investigated, but nothing more specific can be said.
    rnd = random.Random(seed)
    n = int(w * h / 32)
    pts = [(x + rnd.random() * w, y + rnd.random() * h, 0.6 + rnd.random() * 0.9) for _ in range(n)]
    return dots(pts, HAZE, opacity="0.75")


def tex_unexplored(x, y, w, h):
    # Nothing inside: a registered question nobody has looked into.
    return (
        f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="none" '
        f'stroke="{DIM}" stroke-width="1" stroke-dasharray="3 3"/>'
    )


def stipple_band(x, y, w, h, density, rnd):
    n = int(w * h * density)
    pts = []
    for _ in range(n):
        # Denser toward the centre line of the band.
        py = y + h / 2 + (rnd.random() - rnd.random()) * h / 2
        pts.append((x + rnd.random() * w, py, 0.45 + rnd.random() * 0.6))
    return pts


# ---------------------------------------------------------------------------
# Mark
# ---------------------------------------------------------------------------

def build_mark():
    size, n, step = 64, 7, 7.6
    o = (size - (n - 1) * step) / 2
    c = (n - 1) / 2
    pts = []
    for j in range(n):
        for i in range(n):
            d = ((i - c) ** 2 + (j - c) ** 2) ** 0.5
            r = max(0.0, min(2.5, (d - 1.5) * 1.1))
            pts.append((o + i * step, o + j * step, r))
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
        'role="img" aria-label="Enigma mark: a halftone grid with an empty centre">'
        f'<rect width="{size}" height="{size}" rx="13" fill="{INK}"/>'
        + dots(pts, BONE)
        + "</svg>\n"
    )
    (OUT / "enigma-mark.svg").write_text(svg)


# ---------------------------------------------------------------------------
# Hero: sources -> structured evidence -> ordered rules -> evidence states
# ---------------------------------------------------------------------------

def curve(x1, y1, x2, y2, stroke, width=1.0, opacity=1.0):
    mx = (x1 + x2) / 2
    return (
        f'<path d="M{f(x1)} {f(y1)} C{f(mx)} {f(y1)} {f(mx)} {f(y2)} {f(x2)} {f(y2)}" fill="none" '
        f'stroke="{stroke}" stroke-width="{f(width)}" stroke-opacity="{opacity}"/>'
    )


def build_hero():
    W, H = 1040, 520
    rnd = random.Random(2026)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        'role="img" aria-label="Enigma concept: sources feed ordered rules that resolve into six evidence states">',
        f"<defs>{grain_defs()}</defs>",
        f'<rect width="{W}" height="{H}" rx="14" fill="{INK}"/>',
    ]

    top, pitch = 118, 38
    # Column headings
    parts.append(text(40, 72, "SOURCES", 12, DIM, spacing=2))
    parts.append(text(410, 72, "ENIGMA", 12, BONE, weight="700", spacing=2))
    parts.append(text(484, 72, "ORDERED RULES", 12, DIM, spacing=2))
    parts.append(text(680, 72, "EVIDENCE STATE", 12, DIM, spacing=2))
    parts.append(f'<line x1="40" y1="88" x2="{W - 40}" y2="88" stroke="{LINE}" stroke-width="1"/>')

    # Rule panel
    rules = [
        ("1", "investigation"),
        ("2", "supersession"),
        ("3", "explicit conflict"),
        ("4", "adequacy"),
        ("5", "affirmative negative"),
        ("6", "scoped support"),
        ("·", "else: fail closed"),
    ]
    px, pw = 410, 200
    ptop = top - 22
    pbot = top + pitch * (len(rules) - 1) + 22
    parts.append(
        f'<rect x="{px}" y="{ptop}" width="{pw}" height="{pbot - ptop}" rx="6" fill="{PANEL}" stroke="{LINE}"/>'
    )
    rule_y = [top + k * pitch for k in range(len(rules))]
    for (num, name), ry in zip(rules, rule_y):
        hot = num == "3"
        parts.append(text(px + 16, ry + 4.5, num, 13, EMBER if hot else DIM, weight="700" if hot else "400"))
        parts.append(text(px + 36, ry + 4.5, name, 13, BONE if hot else "#C9C5BD"))
    parts.append(text(px + 16, rule_y[1] + 19, "removes superseded paths", 10, DIM))

    # Sources: eight stipple bands, one per synthetic report
    src_top, src_pitch, band_h = top - 12, 37.5, 22
    src_y = [src_top + i * src_pitch for i in range(8)]
    densities = [0.13, 0.19, 0.10, 0.17, 0.12, 0.07, 0.09, 0.15]
    for i, (sy, dens) in enumerate(zip(src_y, densities)):
        label = f"S-0{i + 1}"
        hot = label in ("S-02", "S-04")
        color = EMBER if label == "S-04" else BONE
        parts.append(text(40, sy + band_h / 2 + 4.5, label, 12, BONE if hot else DIM, weight="700" if hot else "400"))
        pts = stipple_band(92, sy, 150, band_h, dens, rnd)
        parts.append(dots(pts, color, opacity="1" if hot else "0.55"))

    # Structured evidence: every source converges on the rule panel
    entry = (px, (ptop + pbot) / 2)
    for i, sy in enumerate(src_y):
        parts.append(curve(248, sy + band_h / 2, entry[0], entry[1], BONE, 0.8, 0.22))
    parts.append(text(92, src_y[-1] + band_h + 30, "structured evidence: typed facts + provenance", 11, DIM))
    # One highlighted trace: a supporting and a contradicting source, through rule 3
    for label_idx, color in ((1, BONE), (3, EMBER)):
        sy = src_y[label_idx] + band_h / 2
        parts.append(curve(248, sy, px, rule_y[2], color, 1.4, 0.95))

    # States
    states = [
        (0, "UNEXPLORED", tex_unexplored),
        (2, "CONTRADICTORY", tex_contradictory),
        (3, "MISSING EVIDENCE", tex_missing),
        (4, "NO RELATIONSHIP", tex_no_relationship),
        (5, "SUPPORTED", tex_supported),
        (6, "UNKNOWN", tex_unknown),
    ]
    sw_x, sw_w, sw_h = 842, 158, 22
    s_top = top - 6
    s_pitch = (rule_y[-1] + 6 - s_top) / (len(states) - 1)
    for k, (rule_idx, name, tex) in enumerate(states):
        sy = s_top + k * s_pitch
        hot = name == "CONTRADICTORY"
        parts.append(
            curve(px + pw, rule_y[rule_idx], 672, sy, EMBER if hot else DIM, 1.4 if hot else 0.9, 0.95 if hot else 0.6)
        )
        parts.append(text(680, sy + 4.5, name, 14, BONE, weight="700" if hot else "400"))
        parts.append(tex(sw_x, sy - sw_h / 2, sw_w, sw_h))

    # Caption
    parts.append(f'<line x1="40" y1="{H - 62}" x2="{W - 40}" y2="{H - 62}" stroke="{LINE}" stroke-width="1"/>')
    parts.append(
        text(40, H - 34, "Every state traces back through the rule that decided it to the sources behind it.", 13, "#C9C5BD")
    )
    parts.append(text(W - 40, H - 34, "illustrative · synthetic sources", 11, DIM, anchor="end"))

    parts.append(f'<rect width="{W}" height="{H}" rx="14" filter="url(#grain)" opacity="0.07"/>')
    parts.append("</svg>\n")
    (OUT / "enigma-hero.svg").write_text("".join(parts))


# ---------------------------------------------------------------------------
# Interface concept (design concept only; built from synthetic result P-1)
# ---------------------------------------------------------------------------

def card(x, y, w, h, accent):
    return (
        f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="6" fill="{PANEL}" stroke="{LINE}"/>'
        f'<rect x="{f(x)}" y="{f(y + 8)}" width="2.5" height="{f(h - 16)}" fill="{accent}"/>'
    )


def lines(x, y, rows, size=13, fill="#C9C5BD", family=SANS, lh=19):
    return "".join(text(x, y + i * lh, r, size, fill, family) for i, r in enumerate(rows))


def build_concept():
    W, H = 1040, 780
    M = 32
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        'role="img" aria-label="Design concept, not current implementation: inspecting one Enigma result">',
        f"<defs>{grain_defs()}</defs>",
        f'<rect width="{W}" height="{H}" rx="14" fill="{INK}"/>',
    ]

    # Concept stamp: impossible to miss, and part of the image itself
    stamp = "DESIGN CONCEPT — NOT CURRENT IMPLEMENTATION"
    parts.append(f'<rect x="{M}" y="24" width="408" height="30" rx="4" fill="none" stroke="{EMBER}" stroke-width="1.5"/>')
    parts.append(text(M + 14, 44, stamp, 13, EMBER, weight="700", spacing=1))
    parts.append(text(W - M, 44, "synthetic data · examples/ · result P-1", 12, DIM, anchor="end"))

    # Question and resulting state
    qy = 76
    parts.append(f'<rect x="{M}" y="{qy}" width="{W - 2 * M}" height="104" rx="8" fill="{PANEL}" stroke="{LINE}"/>')
    parts.append(text(M + 20, qy + 28, "QUESTION", 11, DIM, spacing=2))
    parts.append(text(M + 20, qy + 58, "Does PRR improve oral reading fluency?", 22, BONE, SANS, weight="600"))
    parts.append(text(M + 20, qy + 84, "mild intellectual disability · grades 3–5 · small group · immediate posttest", 12, DIM))
    sx = 690
    parts.append(f'<line x1="{sx - 22}" y1="{qy + 16}" x2="{sx - 22}" y2="{qy + 88}" stroke="{LINE}"/>')
    parts.append(text(sx, qy + 28, "EVIDENCE STATE", 11, DIM, spacing=2))
    parts.append(text(sx, qy + 56, "CONTRADICTORY_EVIDENCE", 16, BONE, weight="700"))
    parts.append(tex_contradictory(sx, qy + 68, 286, 16))

    # Evidence columns
    cy, ch = 206, 238
    gap = 18
    cw = (W - 2 * M - 2 * gap) / 3
    cols = [
        ("SUPPORTING · current", BONE),
        ("CONTRADICTING · current", EMBER),
        ("QUALIFYING · not counted", DIM),
    ]
    xs = [M + i * (cw + gap) for i in range(3)]
    for (title, accent), x in zip(cols, xs):
        parts.append(text(x, cy + 4, title, 11, accent if accent != DIM else DIM, spacing=1.5))

    top = cy + 18
    # Supporting: S-02, with its duplicate report nested under it
    x = xs[0]
    parts.append(card(x, top, cw, 96, BONE))
    parts.append(text(x + 16, top + 26, "S-02", 13, BONE, weight="700"))
    parts.append(text(x + 58, top + 26, "Synthetic Study B (2018)", 13, BONE, SANS))
    parts.append(lines(x + 16, top + 50, ["single-case design · n = 4 · direct"]))
    parts.append(text(x + 16, top + 76, "S-02:results:figure-1", 11, DIM))
    t2 = top + 108
    parts.append(card(x + 18, t2, cw - 18, 76, LINE))
    parts.append(text(x + 34, t2 + 26, "S-03", 13, "#C9C5BD", weight="700"))
    parts.append(text(x + 76, t2 + 26, "same sample as S-02", 13, "#C9C5BD", SANS))
    parts.append(text(x + 34, t2 + 52, "study-B · counted once", 11, DIM))
    parts.append(f'<path d="M{f(x + 8)} {f(top + 96)} V{f(t2 + 38)} H{f(x + 18)}" fill="none" stroke="{LINE}"/>')

    # Contradicting: S-04
    x = xs[1]
    parts.append(card(x, top, cw, 96, EMBER))
    parts.append(text(x + 16, top + 26, "S-04", 13, EMBER, weight="700"))
    parts.append(text(x + 58, top + 26, "Synthetic Study C (2021)", 13, BONE, SANS))
    parts.append(lines(x + 16, top + 50, ["randomized · n = 58 · direct"]))
    parts.append(text(x + 16, top + 76, "S-04:results:table-3", 11, DIM))
    parts.append(lines(x + 16, top + 128, [
        "Independent of study-B. Reports an",
        "interval that excludes the S-02 effect.",
    ], 12, DIM))

    # Qualifying, not counted
    x = xs[2]
    parts.append(card(x, top, cw, 96, DIM))
    parts.append(text(x + 16, top + 26, "S-01", 13, "#C9C5BD", weight="700"))
    parts.append(text(x + 58, top + 26, "population mismatch", 13, "#C9C5BD", SANS))
    parts.append(lines(x + 16, top + 50, ["learning disability, not ID", "see P-4 for that scope"], 12, DIM))
    parts.append(card(x, top + 108, cw, 96, DIM))
    parts.append(text(x + 16, top + 134, "S-07", 13, "#C9C5BD", weight="700"))
    parts.append(text(x + 58, top + 134, "construct mismatch", 13, "#C9C5BD", SANS))
    parts.append(lines(x + 16, top + 158, ["measures teacher-rated engagement,", "not fluency"], 12, DIM))

    # Bottom row: trace, uncertainty, missing evidence
    by, bh = 478, 214
    bw1 = 400
    bw2 = (W - 2 * M - bw1 - 2 * gap) / 2
    bx = [M, M + bw1 + gap, M + bw1 + gap + bw2 + gap]
    for x, w in zip(bx, [bw1, bw2, bw2]):
        parts.append(f'<rect x="{f(x)}" y="{by}" width="{f(w)}" height="{bh}" rx="8" fill="{PANEL}" stroke="{LINE}"/>')

    x = bx[0]
    parts.append(text(x + 20, by + 28, "PRECEDENCE TRACE", 11, DIM, spacing=2))
    trace = [
        ("1", "investigation", "COMPLETE", False, True),
        ("2", "supersession", "none", False, True),
        ("3", "explicit conflict", "PRESENT", True, True),
        ("4", "adequacy", "not reached", False, False),
        ("5", "affirmative negative", "not reached", False, False),
        ("6", "scoped support", "not reached", False, False),
    ]
    for k, (n, name, val, hot, reached) in enumerate(trace):
        ty = by + 56 + k * 21
        col = EMBER if hot else ("#C9C5BD" if reached else "#5E5B55")
        parts.append(text(x + 20, ty, n, 12, col, weight="700" if hot else "400"))
        parts.append(text(x + 40, ty, name, 12, col))
        parts.append(text(x + 230, ty, val, 12, col, weight="700" if hot else "400"))
    parts.append(text(x + 20, by + bh - 14, "→ CONTRADICTORY_EVIDENCE", 12, EMBER, weight="700"))

    x = bx[1]
    parts.append(text(x + 20, by + 28, "UNCERTAINTY", 11, DIM, spacing=2))
    parts.append(text(x + 20, by + 56, "CONFLICTING_EVIDENCE", 12, EMBER, weight="700"))
    parts.append(lines(x + 20, by + 84, [
        "Independent direct studies",
        "disagree on the same outcome",
        "in the same population.",
    ], 13))

    x = bx[2]
    parts.append(text(x + 20, by + 28, "MISSING EVIDENCE", 11, DIM, spacing=2))
    parts.append(lines(x + 20, by + 58, [
        "An independent replication",
        "able to separate the S-02",
        "and S-04 explanations.",
    ], 13))
    parts.append(tex_missing(x + 20, by + 160, bw2 - 40, 22))

    # Provenance footer
    fy = H - 44
    parts.append(f'<line x1="{M}" y1="{fy - 22}" x2="{W - M}" y2="{fy - 22}" stroke="{LINE}"/>')
    parts.append(text(M, fy, "PROVENANCE", 11, DIM, spacing=2))
    parts.append(text(M + 112, fy, "demo-corpus@v1 · facts: human annotator · rules: deterministic · model use: none · corpus-only", 12, "#C9C5BD"))

    parts.append(f'<rect width="{W}" height="{H}" rx="14" filter="url(#grain)" opacity="0.06"/>')
    parts.append("</svg>\n")
    (OUT / "enigma-concept.svg").write_text("".join(parts))


if __name__ == "__main__":
    build_mark()
    build_hero()
    build_concept()
