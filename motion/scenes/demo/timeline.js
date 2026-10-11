// Single source of truth for picture AND sound. Every cut sits on a bar line.
import { beatGrid, sequence } from '../../lib/motion.js';

export const BPM = 120; // 1 beat = 0.5s, 1 bar = 2s
export const grid = beatGrid(BPM);

export const seq = sequence([
  { name: 'title', dur: grid.bar(1) },
  { name: 'morph', dur: grid.bar(1) },
  { name: 'grid', dur: grid.bar(1) },
  { name: 'chart', dur: grid.bar(1) },
  { name: 'lockup', dur: grid.bar(1) },
]);

export const SCENE = { width: 1920, height: 1080, fps: 30, duration: seq.duration };

export const PALETTE = {
  paper: '#F3EFE6',
  ink: '#121212',
  accent: '#FF4D2E',
  blue: '#2D5BFF',
  mute: '#B9B2A3',
};
