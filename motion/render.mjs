#!/usr/bin/env node
// Route A renderer: a page exposes seek(t); we walk time, screenshot every
// frame in headless Chromium and pipe the frames into ffmpeg.
//
//   node render.mjs scenes/demo                       # full MP4 (+ audio if the scene has audio.mjs)
//   node render.mjs scenes/demo --size 1080x1920      # same timeline, vertical
//   node render.mjs scenes/demo --stills 0.5,3,7.2    # PNG stills for critique
//   node render.mjs scenes/demo --sheet 12            # contact sheet of 12 evenly spaced frames
//   node render.mjs scenes/demo --draft               # half resolution, half fps, fast preview
//   node render.mjs scenes/demo --from 2 --to 4       # render only a time range
import { createServer } from 'node:http';
import { spawn } from 'node:child_process';
import { readFileSync, existsSync, mkdirSync, rmSync, statSync } from 'node:fs';
import { join, resolve, extname, basename, dirname, relative } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = dirname(fileURLToPath(import.meta.url));

// ------------------------------------------------------------------ args
const argv = process.argv.slice(2);
if (!argv[0] || argv[0].startsWith('--')) {
  console.error('usage: node render.mjs <sceneDir> [--out f.mp4] [--size WxH] [--fps n] [--from s] [--to s] [--stills t,t] [--sheet n] [--draft] [--no-audio]');
  process.exit(1);
}
const opt = { scene: resolve(argv[0]) };
for (let i = 1; i < argv.length; i++) {
  const k = argv[i].replace(/^--/, '');
  const next = argv[i + 1];
  if (next !== undefined && !next.startsWith('--')) { opt[k] = next; i++; } else opt[k] = true;
}
const sceneName = basename(opt.scene);
if (!existsSync(join(opt.scene, 'index.html'))) throw new Error(`${opt.scene}/index.html not found`);
if (relative(ROOT, opt.scene).startsWith('..')) throw new Error('scene must live inside motion/');

// --------------------------------------------------------- static server
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.otf': 'font/otf', '.css': 'text/css' };
const server = createServer((req, res) => {
  const p = join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!p.startsWith(ROOT) || !existsSync(p) || statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': TYPES[extname(p)] || 'application/octet-stream' });
  res.end(readFileSync(p));
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const base = `http://127.0.0.1:${server.address().port}`;

// --------------------------------------------------------------- browser
async function loadPlaywright() {
  try { return await import('playwright'); } catch {}
  for (const p of ['/opt/node22/lib/node_modules/playwright/index.mjs']) {
    if (existsSync(p)) return import(pathToFileURL(p).href);
  }
  throw new Error('playwright not found: run `npm install` in motion/');
}
const { chromium } = await loadPlaywright();
const launch = { args: ['--disable-gpu-vsync', '--font-render-hinting=none'] };
if (existsSync('/opt/pw-browsers/chromium')) launch.executablePath = '/opt/pw-browsers/chromium';
let browser;
try { browser = await chromium.launch(launch); } catch { delete launch.executablePath; browser = await chromium.launch(launch); }

// Probe the scene for its defaults, then open it at the requested size.
async function openScene(w, h) {
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => { console.error('scene error:', e.message); process.exitCode = 1; });
  page.on('console', (m) => m.type() === 'error' && console.error('scene console:', m.text()));
  const rel = relative(ROOT, opt.scene).split('\\').join('/');
  await page.goto(`${base}/${rel}/index.html?w=${w}&h=${h}`);
  await page.waitForFunction(() => window.SCENE && typeof window.seek === 'function', null, { timeout: 15000 });
  await page.evaluate(async () => { await document.fonts.ready; if (window.ready) await window.ready; });
  return page;
}

const probe = await openScene(1920, 1080);
const S = await probe.evaluate(() => ({ ...window.SCENE }));
await probe.close();

let [W, H] = opt.size ? opt.size.split('x').map(Number) : [S.width, S.height];
let fps = Number(opt.fps || S.fps || 30);
if (opt.draft) { W = Math.round(W / 4) * 2; H = Math.round(H / 4) * 2; fps = Math.max(12, Math.round(fps / 2)); }
const page = await openScene(W, H);
const T0 = Number(opt.from || 0);
const T1 = Math.min(Number(opt.to || S.duration), S.duration);

const outDir = join(ROOT, 'out', sceneName);
mkdirSync(outDir, { recursive: true });
const shot = async (t, path, type = 'png') => {
  await page.evaluate((t) => window.seek(t), t);
  return page.screenshot({ path, type, ...(type === 'jpeg' ? { quality: 92 } : {}) });
};
const ff = (args) => new Promise((ok, fail) => {
  const p = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', ...args], { stdio: ['pipe', 'inherit', 'inherit'] });
  p.on('close', (c) => (c === 0 ? ok() : fail(new Error(`ffmpeg exited ${c}`))));
  ff.proc = p;
});

const tag = `${W}x${H}`;
try {
  if (opt.stills) {
    // ---------------------------------------------------------- stills
    const times = String(opt.stills).split(',').map(Number);
    for (const t of times) {
      const f = join(outDir, `still_${tag}_${t.toFixed(2)}s.png`);
      await shot(t, f);
      console.log(relative(process.cwd(), f));
    }
  } else if (opt.sheet) {
    // --------------------------------------------------- contact sheet
    const n = Number(opt.sheet === true ? 12 : opt.sheet);
    const cols = Math.ceil(Math.sqrt(n * (H / W) * 1.6)) || 4;
    const tmp = join(outDir, '.sheet');
    rmSync(tmp, { recursive: true, force: true });
    mkdirSync(tmp, { recursive: true });
    for (let i = 0; i < n; i++) {
      const t = T0 + ((T1 - T0) * (i + 0.5)) / n;
      await page.evaluate((t) => window.seek(t), t);
      await page.evaluate((label) => {
        const d = document.createElement('div');
        d.id = '__ts';
        d.textContent = label;
        d.style.cssText = 'position:fixed;left:8px;top:8px;font:bold 22px monospace;color:#fff;background:#000c;padding:2px 8px;z-index:99999';
        document.body.appendChild(d);
      }, `${t.toFixed(2)}s`);
      await page.screenshot({ path: join(tmp, `f${String(i).padStart(3, '0')}.png`) });
      await page.evaluate(() => document.getElementById('__ts').remove());
    }
    const f = join(outDir, `sheet_${tag}.png`);
    const cellW = Math.min(480, W);
    await ff(['-framerate', '1', '-i', join(tmp, 'f%03d.png'), '-vf', `scale=${cellW}:-2,tile=${cols}x${Math.ceil(n / cols)}:padding=6:color=0x222222`, '-frames:v', '1', f]);
    rmSync(tmp, { recursive: true, force: true });
    console.log(relative(process.cwd(), f));
  } else {
    // ----------------------------------------------------------- video
    let audio = null;
    const audioSrc = join(opt.scene, 'audio.mjs');
    if (!opt['no-audio'] && existsSync(audioSrc)) {
      audio = join(outDir, 'audio.wav');
      const mod = await import(pathToFileURL(audioSrc).href);
      await mod.default(audio, S);
      console.log('audio  ', relative(process.cwd(), audio));
    }
    const out = opt.out ? resolve(opt.out) : join(outDir, `${sceneName}_${tag}${opt.draft ? '_draft' : ''}.mp4`);
    const frames = Math.round((T1 - T0) * fps);
    const type = opt.draft ? 'jpeg' : 'png';
    const args = ['-f', 'image2pipe', '-framerate', String(fps), '-i', '-'];
    if (audio) args.push('-ss', String(T0), '-t', String(T1 - T0), '-i', audio);
    args.push('-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', opt.draft ? '26' : '16', '-preset', opt.draft ? 'veryfast' : 'slow', '-movflags', '+faststart');
    if (audio) args.push('-c:a', 'aac', '-b:a', '192k', '-shortest');
    args.push(out);
    const done = ff(args);
    const started = Date.now();
    for (let i = 0; i < frames; i++) {
      const buf = await shot(T0 + i / fps, undefined, type);
      if (!ff.proc.stdin.write(buf)) await new Promise((r) => ff.proc.stdin.once('drain', r));
      if (i % fps === 0 || i === frames - 1) {
        const pct = (((i + 1) / frames) * 100).toFixed(0);
        process.stdout.write(`\rframe ${i + 1}/${frames} (${pct}%)  ${((Date.now() - started) / 1000).toFixed(0)}s`);
      }
    }
    ff.proc.stdin.end();
    await done;
    console.log(`\nvideo   ${relative(process.cwd(), out)}`);
  }
} finally {
  await browser.close();
  server.close();
}
