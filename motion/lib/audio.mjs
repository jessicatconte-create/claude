// Tiny dependency-free synth. Renders a soundtrack on the same timeline as the
// picture and writes a 16-bit stereo WAV.
import { writeFileSync } from 'node:fs';
import { rng } from './motion.js';

export const SR = 48000;

export function createMix(duration) {
  const n = Math.ceil(duration * SR);
  return { L: new Float32Array(n), R: new Float32Array(n), duration };
}

function add(mix, start, len, fn, pan = 0, gain = 1) {
  const s0 = Math.max(0, Math.round(start * SR));
  const n = Math.min(Math.round(len * SR), mix.L.length - s0);
  const gl = gain * Math.cos(((pan + 1) * Math.PI) / 4);
  const gr = gain * Math.sin(((pan + 1) * Math.PI) / 4);
  for (let i = 0; i < n; i++) {
    const v = fn(i / SR, i);
    mix.L[s0 + i] += v * gl;
    mix.R[s0 + i] += v * gr;
  }
}

export const midi = (m) => 440 * Math.pow(2, (m - 69) / 12);

export function kick(mix, t, gain = 0.9) {
  add(mix, t, 0.45, (x) => {
    // Pitch sweeps 155 Hz -> 45 Hz; phase is the integral of that sweep.
    const phase = 2 * Math.PI * (45 * x + (110 / 30) * (1 - Math.exp(-x * 30)));
    return Math.sin(phase) * Math.exp(-x * 7);
  }, 0, gain);
}

export function hat(mix, t, gain = 0.18, seed = 7) {
  const r = rng(seed + Math.round(t * 1000));
  let prev = 0;
  add(mix, t, 0.08, (x) => {
    const w = r() * 2 - 1;
    const hp = w - prev; // crude high-pass
    prev = w;
    return hp * Math.exp(-x * 60);
  }, 0.3, gain);
}

export function clap(mix, t, gain = 0.35, seed = 3) {
  const r = rng(seed + Math.round(t * 1000));
  add(mix, t, 0.25, (x) => {
    const env = Math.exp(-x * 18) * (x < 0.02 ? 0.6 + 0.4 * Math.sin(x * 900) : 1);
    return (r() * 2 - 1) * env;
  }, -0.2, gain);
}

// Soft detuned saw pad with a slow attack.
export function pad(mix, t, dur, notes, gain = 0.06) {
  for (const [k, m] of notes.entries()) {
    const f = midi(m);
    add(mix, t, dur, (x) => {
      const env = Math.min(1, x / 0.4) * Math.min(1, (dur - x) / 0.6);
      let v = 0;
      for (const d of [-0.12, 0, 0.12]) {
        const ph = (x * f * Math.pow(2, d / 12)) % 1;
        v += (2 * ph - 1) * 0.33;
      }
      return v * env;
    }, k % 2 ? 0.4 : -0.4, gain);
  }
}

export function pluck(mix, t, m, gain = 0.2, pan = 0) {
  const f = midi(m);
  add(mix, t, 0.6, (x) => {
    const ph = 2 * Math.PI * f * x;
    return (Math.sin(ph) + 0.4 * Math.sin(2 * ph) + 0.15 * Math.sin(3 * ph)) * Math.exp(-x * 9);
  }, pan, gain);
}

// Rising filtered-noise whoosh that ends exactly at `t` (put it before a cut).
export function whoosh(mix, t, len = 0.5, gain = 0.25, seed = 11) {
  const r = rng(seed + Math.round(t * 1000));
  let lp = 0;
  add(mix, t - len, len + 0.1, (x) => {
    const p = Math.min(1, x / len);
    const a = 0.02 + 0.5 * p * p;
    lp += a * (r() * 2 - 1 - lp);
    return lp * (x < len ? p * p : Math.exp(-(x - len) * 40));
  }, 0, gain);
}

// Short sine "impact" for logo hits.
export function impact(mix, t, gain = 0.6) {
  add(mix, t, 1.2, (x) => Math.sin(2 * Math.PI * 55 * x) * Math.exp(-x * 3) + Math.sin(2 * Math.PI * 110 * x) * 0.3 * Math.exp(-x * 6), 0, gain);
}

export function writeWav(mix, path, { fadeOut = 0.3 } = {}) {
  const n = mix.L.length;
  let peak = 0;
  for (let i = 0; i < n; i++) peak = Math.max(peak, Math.abs(mix.L[i]), Math.abs(mix.R[i]));
  const g = peak > 0 ? 0.89 / peak : 1;
  const buf = Buffer.alloc(44 + n * 4);
  buf.write('RIFF', 0);
  buf.writeUInt32LE(36 + n * 4, 4);
  buf.write('WAVEfmt ', 8);
  buf.writeUInt32LE(16, 16);
  buf.writeUInt16LE(1, 20);
  buf.writeUInt16LE(2, 22);
  buf.writeUInt32LE(SR, 24);
  buf.writeUInt32LE(SR * 4, 28);
  buf.writeUInt16LE(4, 32);
  buf.writeUInt16LE(16, 34);
  buf.write('data', 36);
  buf.writeUInt32LE(n * 4, 40);
  const fo = Math.round(fadeOut * SR);
  for (let i = 0; i < n; i++) {
    const f = i > n - fo ? (n - i) / fo : 1;
    const s = (v) => Math.max(-32768, Math.min(32767, Math.round(Math.tanh(v * g) * f * 32767)));
    buf.writeInt16LE(s(mix.L[i]), 44 + i * 4);
    buf.writeInt16LE(s(mix.R[i]), 46 + i * 4);
  }
  writeFileSync(path, buf);
}
