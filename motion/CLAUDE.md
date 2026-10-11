# Motion studio — house rules

Every video here is a program. A scene is an `index.html` that exposes
`window.SCENE` and a synchronous `window.seek(t)`; `render.mjs` walks time in
headless Chromium and pipes frames into ffmpeg.

## Scene contract
- `scenes/<name>/index.html` sets `window.SCENE = { width, height, fps, duration }`,
  `window.seek(t)` and optionally `window.ready` (a promise for fonts/images).
- `seek(t)` repaints the WHOLE frame from scratch and depends only on `t`.
  Never use `Date.now`, `performance.now`, `requestAnimationFrame`, CSS
  transitions, `Math.random` or state carried between frames (use `rng(seed)`).
- Read the stage size from `?w=&h=` and draw against `layout(w, h)` (`u` = 1% of
  the short side). Never hard-code pixels, so one timeline renders 16:9, 1:1, 9:16.
- Put BPM, shot list and palette in `timeline.js`; both `index.html` and
  `audio.mjs` import it, so cuts land on the beat.
- No network at render time: local fonts/assets only, inside `motion/`.

## Motion
- Use closed-form springs from `lib/motion.js`, not fixed easing curves:
  `snappy` for UI, `default` for containers/camera, `heavy` (no overshoot) for big
  type and logos, `playful` for mascots.
- A value with more than one target uses `track()` (one spring per change),
  never a restarted spring.
- Payoff every 3–5 s, hook in the first 2 s. Cut on bar lines; land hits on beats.
- Avoid the default look: centered text on a gradient with everything fading in.
  If there's a reference (frame, video, folder), match its palette, type and pacing.

## Sound
- If the scene has `audio.mjs` (default export `(path, SCENE) => void`), it's
  synthesized with `lib/audio.mjs` on the same beat grid and muxed automatically.
- Supplied track: measure its BPM/onsets first and put them in `timeline.js`.
- API keys (e.g. ElevenLabs) live in `.env`; refer to them by variable name, never paste values.

## Workflow gates (don't skip)
plan (shot list in timeline.js) → stills → contact sheet → draft → full render → formats.

```bash
node render.mjs scenes/<name> --stills 0.5,2,4.5   # look at key frames
node render.mjs scenes/<name> --sheet 12           # whole film at a glance
node render.mjs scenes/<name> --draft              # fast low-res MP4
node render.mjs scenes/<name>                      # final MP4 (+audio)
node render.mjs scenes/<name> --size 1080x1920     # vertical from the same timeline
```

## Critique loop
After every stills/sheet render, open the PNGs and score each shot 1–10 on:
composition, typography, motion clarity, timing/beat sync, polish. Write the 3
worst problems, fix them, re-render the affected stills. Repeat until every shot
scores 8+. Only then render the full MP4. Output goes to `out/` (gitignored).
