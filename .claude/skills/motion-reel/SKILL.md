---
name: motion-reel
description: Create a code-rendered motion design video (showreel, product launch, explainer, loop) in the motion/ studio — seek(t) scene, springs, beat-synced synth audio, critique loop, MP4 in 16:9/1:1/9:16. Use when asked for a motion video, reel, launch video, animated ad or "/motion-reel for <URL or idea>".
---

# /motion-reel

Usage examples:
- `/motion-reel for https://myproduct.com, 20s, vertical`
- `/motion-reel 15-second showreel, reference ./motion/refs/frame.png`
- `/motion-reel loop of our onboarding UI morphing, 1:1`

Work inside `motion/`. Read `motion/CLAUDE.md` first and follow its rules.

## Steps

1. **Brief.** From the request extract: subject/product (fetch the URL and collect
   real copy, logo, colors, screenshots into `scenes/<name>/assets/`), duration,
   formats, reference, tone. Ask only if the subject is missing entirely.
2. **Reference.** If a frame/video/folder is given, look at it (extract frames from a
   video with `ffmpeg -i ref.mp4 -vf fps=2 refs/f%03d.png`) and write
   `scenes/<name>/style.md`: palette (hex), type, pacing, transitions, what NOT to copy.
   Without a reference, pick a named style and write it down anyway.
3. **Plan.** Copy `scenes/demo` to `scenes/<name>`. Rewrite `timeline.js`: BPM, a shot
   list on bar lines (hook in first 2 s, payoff every 3–5 s, last frame loops to the
   first when it makes sense), palette.
4. **Build.** Write one draw function per shot in `index.html`, against `layout()`
   units, using `spring` / `track` / `beatGrid` from `lib/motion.js`. One element that
   morphs through states beats many elements that fade.
5. **Sound.** Rewrite `audio.mjs` on the same grid (kick/hat/clap/pad/pluck/whoosh/
   impact), with whooshes into cuts and hits on reveals. If the user supplied music,
   measure it and set BPM/offset from it instead.
6. **Critique loop.** `node render.mjs scenes/<name> --sheet 12` and `--stills` at each
   shot's key moment. Look at the images, score each shot 1–10 (composition, type,
   motion clarity, beat sync, polish), fix the 3 worst problems, repeat until all 8+.
7. **Render.** Full MP4, then each requested format with `--size` (1080x1920,
   1080x1080). Check the vertical sheet too — reframe, don't crop.
8. **Deliver.** Report the output paths, duration, BPM and the final scores.
