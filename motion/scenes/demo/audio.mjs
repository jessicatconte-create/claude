// Soundtrack synthesized on the same beat grid as the picture.
import { createMix, kick, hat, clap, pad, pluck, whoosh, impact, writeWav } from '../../lib/audio.mjs';
import { grid, seq } from './timeline.js';

export default function render(path) {
  const mix = createMix(seq.duration);
  const beats = Math.round(seq.duration / grid.spb);
  const chords = [[57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 65], [52, 55, 59, 64]];

  for (let b = 0; b < beats; b++) {
    const t = grid.beat(b);
    const last = b >= beats - 4; // let the lockup breathe
    if (!last || b === beats - 4) kick(mix, t, b % 4 === 0 ? 1 : 0.8);
    if (!last) hat(mix, t + grid.spb / 2);
    if (b % 4 === 2 && !last) clap(mix, t);
  }
  seq.shots.forEach((s, i) => {
    pad(mix, s.start, s.dur + 0.3, chords[i % chords.length]);
    if (i > 0) whoosh(mix, s.start, 0.45);
  });
  // Title letters land on 8th notes.
  [69, 72, 76, 79, 76, 72].forEach((m, i) => pluck(mix, 0.25 + i * 0.125, m, 0.16, (i - 2.5) / 4));
  // Chart bars.
  [64, 67, 69, 71, 72, 74, 76].forEach((m, i) => pluck(mix, seq.shots[3].start + 0.15 + i * 0.11, m, 0.13, (i - 3) / 5));
  impact(mix, seq.shots[4].start);
  writeWav(mix, path, { fadeOut: 0.6 });
}
