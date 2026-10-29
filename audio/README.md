# Audio

`bgm.m4a` — a 48-second original ambient loop generated for this repository.
Released under CC0 1.0. You may keep, replace, or delete it.

The page expects `audio/bgm.m4a` (see `data-src` in the generated HTML and
`src/haloflux-lab.html`). If the file is missing, the BGM player hides itself
after the load error; the rest of the page works normally.

To use your own track:

1. Put a licensed file in this folder.
2. Update `data-src="audio/bgm.m4a"` in `src/haloflux-lab.html` (or keep the
   filename and overwrite `bgm.m4a`; the browser decides the codec, not the
   extension).
3. Rebuild with `python3 src/build.py`.

Do not add music you do not have rights to redistribute. `.gitignore` excludes
`audio/*.mp3` and `audio/*.wav` as a guard against accidentally committing a
personal track.
