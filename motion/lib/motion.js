// Motion primitives. Everything here is a pure function of time, so seek(t)
// can paint any frame without simulating the frames before it.
// Works in the browser (ES module) and in Node.

// ---------------------------------------------------------------- springs

// Presets: stiffness k, damping c (mass = 1). Damping ratio z = c / (2*sqrt(k)).
export const SPRINGS = {
  snappy: { stiffness: 400, damping: 30 }, // z≈0.75 tiny overshoot: buttons, toggles, leading edges
  default: { stiffness: 170, damping: 22 }, // z≈0.84 cards, containers, camera
  heavy: { stiffness: 120, damping: 24 }, // z≈1.10 no overshoot: big type, 3D, logo lockups
  playful: { stiffness: 180, damping: 10 }, // z≈0.37 visible bounce: mascots, stickers
};

const preset = (p) => (typeof p === 'string' ? SPRINGS[p] : p || SPRINGS.default);

// Closed-form step response of a damped spring going 0 -> 1 from rest.
export function spring(t, p = 'default') {
  if (t <= 0) return 0;
  const { stiffness: k, damping: c } = preset(p);
  const w = Math.sqrt(k);
  const z = c / (2 * w);
  if (z < 1) {
    const wd = w * Math.sqrt(1 - z * z);
    return 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + ((z * w) / wd) * Math.sin(wd * t));
  }
  if (z === 1) return 1 - Math.exp(-w * t) * (1 + w * t);
  const s = w * Math.sqrt(z * z - 1);
  const r1 = -z * w + s;
  const r2 = -z * w - s;
  return 1 - (r2 * Math.exp(r1 * t) - r1 * Math.exp(r2 * t)) / (r2 - r1);
}

// Animate a value from `from` to `to`, starting at time `start`.
export const springTo = (t, start, from, to, p) => from + (to - from) * spring(t - start, p);

// A value that changes target several times. Do NOT restart the spring on each
// change: add one spring per change, each starting at its own time. Motion stays
// continuous and frame N is still computed directly.
//   track(t, [[0, 100], [1.2, 300], [2.0, 180]], 'snappy')
export function track(t, keys, p) {
  let v = keys[0][1];
  for (let i = 1; i < keys.length; i++) {
    const [at, value] = keys[i];
    if (t < at) break;
    v += (value - keys[i - 1][1]) * spring(t - at, p);
  }
  return v;
}

// Same as track() for arrays of numbers (colors, points).
export const trackN = (t, keys, p) =>
  keys[0][1].map((_, j) => track(t, keys.map(([at, v]) => [at, v[j]]), p));

// ----------------------------------------------------------------- timing

export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a, b, x) => a + (b - a) * x;
// Progress 0..1 of t inside [a, b].
export const range = (t, a, b) => clamp((t - a) / (b - a));
export const easeInOut = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
export const easeOut = (x) => 1 - Math.pow(1 - x, 3);

// Beat grid. Picture and sound share it, so cuts land on the beat.
export function beatGrid(bpm, offset = 0, beatsPerBar = 4) {
  const spb = 60 / bpm;
  return {
    bpm,
    spb,
    beat: (n) => offset + n * spb,
    bar: (n) => offset + n * spb * beatsPerBar,
    // Which beat t is in, and how far into it (0..1).
    at: (t) => {
      const x = (t - offset) / spb;
      return { index: Math.floor(x), phase: x - Math.floor(x) };
    },
    // Decaying pulse 1 -> 0 after every beat, handy for "hit" accents.
    pulse: (t, decay = 8) => {
      const x = (t - offset) / spb;
      return x < 0 ? 0 : Math.exp(-decay * (x - Math.floor(x)) * spb);
    },
  };
}

// Shot list -> which shot is active at t, and local time inside it.
//   const shots = [{ name: 'title', dur: 2 }, ...]
export function sequence(shots) {
  let acc = 0;
  const timed = shots.map((s) => {
    const o = { ...s, start: acc, end: acc + s.dur };
    acc += s.dur;
    return o;
  });
  return {
    shots: timed,
    duration: acc,
    at(t) {
      const s = timed.find((s) => t < s.end) || timed[timed.length - 1];
      return { shot: s, local: t - s.start, progress: clamp((t - s.start) / s.dur) };
    },
  };
}

// Deterministic PRNG (never use Math.random in a scene).
export function rng(seed = 1) {
  let s = seed >>> 0;
  return () => {
    s = (s + 0x6d2b79f5) >>> 0;
    let x = s;
    x = Math.imul(x ^ (x >>> 15), x | 1);
    x ^= x + Math.imul(x ^ (x >>> 7), x | 61);
    return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
  };
}

// --------------------------------------------------------------- color

export const hex = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
export const rgb = ([r, g, b], a = 1) => `rgba(${r | 0},${g | 0},${b | 0},${a})`;
export const mix = (a, b, x) => a.map((v, i) => lerp(v, b[i], x));

// -------------------------------------------------------------- layout

// Scenes are written against a layout, not fixed pixels, so one timeline
// renders to 16:9, 1:1 and 9:16. `u` is 1% of the short side.
export function layout(width, height) {
  const short = Math.min(width, height);
  return {
    w: width,
    h: height,
    cx: width / 2,
    cy: height / 2,
    u: short / 100,
    portrait: height > width,
    square: width === height,
  };
}
