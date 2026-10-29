# COLLAB FIELD / 协作光场

By **一只黄学长** · 2026

A data-driven, single-page "agent ops" visual built on canvas. Twelve independent
pages share one rendering engine; each page carries a different c0 / hi / fil
palette. The `PAL` button switches between them. The right rail replays a
synthetic task ledger in real time.

![COLLAB FIELD hero](screenshots/hero-1920.webp)

![12 palettes](screenshots/all-12.webp)

[Ultrawide 3440×1440 preview](screenshots/hero-3440.webp) ·
[palette index screenshot](screenshots/palettes.png)

## Quick start

No build step is needed to view the pages. From the repository root:

```bash
python3 -m http.server 8000
# open http://localhost:8000/
```

Opening `index.html` directly also works, but some browsers block local audio
and remote fonts on `file://`.

- `index.html` — main entry, same as 09 综合总览 (gold)
- `palettes.html` — palette index, links to all 12
- `collab-01.html` … `collab-12.html` — individual palettes

Designed for 3440×1440 and 1920×1080. At ≥21:10 the bottom panels move to the
right vertical rail; below that they stay under the stage.

## Controls

| Control | Action |
|---|---|
| `PAL` | Open the 6×2 palette panel; each cell opens that palette page |
| BGM / `M` | Play or pause the background loop; the slider sets volume |
| `C` | Toggle the console overlay |
| `F` / double-click | Fullscreen |

## Data

All ledger content is synthetic. The demo contains 128 tasks across 12
workstreams and 24 fictional tool codenames, with 9 open gaps and 6 of 24
proofs verified.

- `data/demo-network.json` — the ledger consumed by the pages
- `src/make_demo.py` — deterministic generator (seed `20261028`); stdlib only
- No real people, organizations, projects, email addresses, phone numbers, file
  paths, or machine identifiers are included.

The right rail's `THOUGHT / CODE / RESULT` logs, the task feed, the dispatch
panel, and the counters all read from that JSON. Edit the JSON and rebuild to
change the story.

## Build

```bash
python3 src/build.py          # collab-01..12.html + index.html
python3 src/build_palettes.py # palettes.html
```

Python 3.9+ and the standard library are enough. The builder reads:

- `src/haloflux-lab.html` — upstream HALOFLUX source, with its copyright header
  intact; the build only performs palette mapping and data injection
- `src/sidebar.tpl` — live-rail template
- `data/palettes.json` — 12 c0 / hi / fil palettes and shared neutrals
- `data/demo-network.json` — the synthetic ledger

## Audio

`audio/bgm.m4a` is a 48-second original ambient loop generated for this
repository and released under CC0 1.0. It is optional. Replace it with a track
you have rights to, or delete it; if the file is missing, the player hides itself
after the load error. Do not commit music you do not own: `.gitignore` excludes
`audio/*.mp3` and `audio/*.wav` so a personal track is not accidentally pushed.

## License

Copyright (c) 2026 一只黄学长.

**PolyForm Noncommercial License 1.0.0 — source-available, not OSI open source.
Noncommercial use only; commercial use is strictly prohibited.** See
[`LICENSE`](LICENSE). The build scripts, generated pages, and synthetic ledger in
this repository are released under the same license.

This is a derivative work. Required notices and upstream credits are in
[`NOTICE`](NOTICE):

- **HALOFLUX** — Copyright (c) 2026 Ryder191 (RYDER CODE / Ms MAIKEBAIs CAT),
  <https://github.com/Ryder191/haloflux>. PolyForm Noncommercial 1.0.0.
- **ION 离子回路 / agent-display v8.0 theme 08** — Copyright (c) 2026 赛博老爸,
  <https://github.com/cyberdaddyleo/agent-display>. PolyForm Noncommercial 1.0.0.
  The 12 palette values are a re-named reference to that theme.
- **JetBrains Mono** — SIL Open Font License 1.1, loaded from Google Fonts.
- **audio/bgm.m4a** — original, CC0 1.0.

No commercial license is offered for HALOFLUX or the ION palette source. If you
need a permissive or commercial license, replace the rendering engine and the
palette source with works you have rights to use; changing this repository's
license alone is not enough.

## Privacy

The pages make no analytics or tracking requests. Everything except Google Fonts
and the local audio file is self-contained. For a fully offline build, remove the
Google Fonts `<link>` from `src/haloflux-lab.html`; the CSS falls back to system
monospace.

## Credits

- Visual engine, composition, and motion: **HALOFLUX by Ryder191**
- Palette reference: **ION 离子回路 / agent-display theme 08 by 赛博老爸**
- Typeface: **JetBrains Mono** (OFL)
- Author / build / synthetic ledger / 12-palette adaptation: **一只黄学长**

## Deploying

The repository root is already a static site. For GitHub Pages: push the
repository, then **Settings → Pages → Deploy from a branch → `main` / root**.
No server-side code is required.
