// Figura "Balança de elasticidade": uma bancada com 15 pinos cujas alturas
// desenham a curva de demanda Q = Q0 · (P/P0)^ε. Um carro com relógio
// comparador corre sobre os pinos: a posição é o preço, o ponteiro é o volume.
// Uso: node build.mjs [saída.html]
import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as k from "../../.claude/skills/anatomy/kit/iso-kit.mjs";
import { kitScript } from "../../.claude/skills/anatomy/scripts/inline-kit.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = process.argv[2] || join(HERE, "balanca-elasticidade.html");

const WIDTH = 640;
const HEIGHT = 380;

// Modelo
const STEPS = Array.from({ length: 15 }, (_, i) => -30 + 5 * i); // variação de preço, %
const ZERO = STEPS.indexOf(0);
const E0 = -1.4;
const PIN_UNIT = 36; // altura do pino quando Q = Q0
const PER_TURN = 90; // uma volta do ponteiro = 90 de altura = 2,5 × Q0

// Mundo
const PLATE = { x: -140, y: -84, w: 280, d: 128, r: 8 };
const PLATE_H = 12;
const FOOT_H = 5;
const ROW_Y = -14;
const PIN_X0 = -100;
const PIN_STEP = 14;
const PIN_R = 3.2;
const CAP_R = 4.4;
const HOLDER = { x: PIN_X0 - 12, y: ROW_Y - 8, w: PIN_STEP * 14 + 24, d: 16, r: 2 };
const HOLDER_H = 10;
const pinX = (i) => PIN_X0 + PIN_STEP * i;
const height = (pct, e) => PIN_UNIT * Math.pow(1 + pct / 100, e);
const MAX_PIN = 92; // limite físico do pino
const pinH = (pct, e) => Math.min(MAX_PIN, height(pct, e));

const RAILS = [-78, -64];
const RAIL_FROM = PIN_X0 - 20;
const RAIL_TO = pinX(14) + 20;
const CAR = { x: -18, y: -82, w: 36, d: 26, r: 3 }; // relativo ao eixo x do carro
const CAR_Z = 3;
const CAR_TOP = 9;
const POST = [0, -71];
const ARM_Z = 112;
const ARM_H = 6;
const POST_TOP = ARM_Z + ARM_H + 10;
const DIAL_R = 21;
const DIAL_Z = ARM_Z + ARM_H;
const DIAL_H = 8;
const DIAL_TOP = DIAL_Z + DIAL_H;
const EPS_KNOB = [PLATE.x + 16, ROW_Y];

const P = k.fitProjection(
  [...k.boxCorners(PLATE, -PLATE_H - FOOT_H, 0), [pinX(14), POST[1], POST_TOP + 2], [pinX(0) - DIAL_R, ROW_Y, DIAL_TOP], [pinX(14) + DIAL_R, ROW_Y + DIAL_R, DIAL_TOP]],
  WIDTH,
  HEIGHT,
  { pad: 26, azimuth: 40 },
);

const at = (point) => k.iso(point, P);
const S = (paths, style) => k.solidSvg(paths, style);
const L = (d, style) => k.lineSvg(d, style);
const D = (points, style) => k.dotsSvg(points, style);
const byDepth = (points) => [...points].sort((a, b) => k.depthOf([a[0], a[1], 0], P) - k.depthOf([b[0], b[1], 0], P));

function plate() {
  const out = [`<path class="iso-halo" d="${k.haloOf(PLATE, -PLATE_H - FOOT_H, PLATE_H, P)}"/>`];
  for (const [x, y] of byDepth(k.corners(PLATE, 22))) {
    out.push(S(k.cylinder(x, y, 7, -PLATE_H - FOOT_H, 1.6, P, 28), { tone: "lo" }));
    out.push(S(k.cylinder(x, y, 5.4, -PLATE_H - FOOT_H + 1.6, FOOT_H - 1.6, P, 28), { tone: "mid" }));
  }
  out.push(S(k.slabOf(PLATE, -PLATE_H, PLATE_H, P, 8, 1.6), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(PLATE, 5), 0, P), { tone: "lo" }));
  const screws = k.corners(PLATE, 10);
  out.push(L(screws.map(([x, y]) => k.ring(x, y, 2.2, 0, P, 16)).join(""), { tone: "lo" }));
  out.push(D(screws.map(([x, y]) => at([x, y, 0])), { size: 0.5 }));

  // régua de preço: um traço por pino, maior a cada 10%, o 0% em destaque
  const strip = { x: pinX(0) - 8, y: 6, w: PIN_STEP * 14 + 16, d: 8, r: 1 };
  out.push(S(k.slabOf(strip, 0, 0.6, P, 3), { tone: "lo", crease: "none" }));
  const minor = [], major = [];
  STEPS.forEach((pct, i) => {
    const x = pinX(i);
    const len = pct === 0 ? 5.6 : pct % 10 === 0 ? 3.8 : 2.2;
    (pct % 10 === 0 ? major : minor).push(k.lineOnTop([x, strip.y + 0.8], [x, strip.y + 0.8 + len], 0.6, P));
    for (const off of [PIN_STEP / 2]) if (i < 14) minor.push(k.lineOnTop([x + off, strip.y + 0.8], [x + off, strip.y + 1.8], 0.6, P));
  });
  out.push(L(minor.join(""), { tone: "lo" }), L(major.join(""), { tone: "mid" }));
  out.push(L(k.lineOnTop([pinX(ZERO), strip.y + 0.8], [pinX(ZERO), strip.y + 6.4], 0.6, P), { tone: "hi" }));
  out.push(D([at([strip.x + 2.5, strip.y + 4, 0.6]), at([strip.x + strip.w - 2.5, strip.y + 4, 0.6])], { size: 0.45 }));

  // plaqueta de identificação com três linhas
  const tag = { x: PLATE.x + PLATE.w - 40, y: 18, w: 28, d: 16, r: 1.2 };
  out.push(S(k.slabOf(tag, 0, 0.8, P, 3, 0.3), { tone: "lo", crease: "none" }));
  for (const [i, y] of [tag.y + 4.5, tag.y + 8, tag.y + 11.5].entries()) {
    out.push(L(k.lineOnTop([tag.x + 4, y], [tag.x + (i === 1 ? 16 : 22), y], 0.8, P), { tone: "faint", free: true }));
  }
  out.push(D(k.corners(tag, 2).map(([x, y]) => at([x, y, 0.8])), { size: 0.4, tone: "lo" }));
  return out.join("");
}

function rails() {
  const out = [];
  for (const y of RAILS) {
    out.push(S(k.slabOf({ x: RAIL_FROM, y: y - 2, w: RAIL_TO - RAIL_FROM, d: 4, r: 1 }, 0, 3, P, 3, 0.4), { tone: "mid" }));
    out.push(D([RAIL_FROM + 8, (RAIL_FROM + RAIL_TO) / 2, RAIL_TO - 8].map((x) => at([x, y, 3])), { size: 0.4 }));
  }
  for (const x of [RAIL_FROM - 6, RAIL_TO]) {
    out.push(S(k.slabOf({ x, y: RAILS[0] - 6, w: 6, d: RAILS[1] - RAILS[0] + 12, r: 1.2 }, 0, 8, P, 3, 0.5), { tone: "mid" }));
    out.push(D([at([x + 3, RAILS[0] - 2, 8]), at([x + 3, RAILS[1] + 2, 8])], { size: 0.45 }));
  }
  return out.join("");
}

function holder() {
  const out = [];
  out.push(S(k.slabOf(HOLDER, 0, HOLDER_H, P, 3, 0.6), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(HOLDER, 2.4), HOLDER_H, P, 3), { tone: "faint" }));
  STEPS.forEach((_, i) => out.push(L(k.ring(pinX(i), ROW_Y, PIN_R + 1.2, HOLDER_H, P, 18), { tone: "lo" })));
  out.push(D([at([HOLDER.x + 4, ROW_Y, HOLDER_H]), at([HOLDER.x + HOLDER.w - 4, ROW_Y, HOLDER_H])], { size: 0.45 }));
  // botão do ε: parafuso de ajuste na ponta esquerda
  const [x, y] = EPS_KNOB;
  out.push(S(k.cylinder(x, y, 8, 0, 3, P, 32), { tone: "lo" }));
  out.push(S(k.cylinder(x, y, 6.4, 3, 9, P, 36), { tone: "mid" }));
  out.push(L(k.knurl(x, y, 6.4, 3.6, 11.4, 34, P), { tone: "lo" }));
  out.push(L(k.ring(x, y, 4.6, 12, P, 24), { tone: "faint" }));
  out.push(L(k.ring(x, y, 9.6, 0, P, 32), { tone: "faint" }));
  const ticks = k.radialTicks(x, y, 9.8, 12, 3, 0, [0.8, 1.6], P, -Math.PI * 0.75, Math.PI * 1.5);
  out.push(L(ticks.minor, { tone: "lo" }), L(ticks.major, { tone: "mid" }));
  out.push(`<path data-part="eps-mark" class="iso-line" data-tone="hi" data-free="end" d="${epsMark(E0)}" style="stroke-width:0.9"/>`);
  out.push(D([at([x, y, 12])], { size: 0.5, tone: "hi" }));
  return out.join("");
}

// ε de −0,2 a −3 vira um quarto de volta para cada lado
const epsAngle = (e) => -Math.PI * 0.75 + ((-e - 0.2) / 2.8) * Math.PI * 1.5;
function epsMark(e) {
  const [x, y] = EPS_KNOB, a = epsAngle(e);
  return k.lineOnTop([x, y], [x + Math.sin(a) * 4.4, y - Math.cos(a) * 4.4], 12, P);
}

function pin(i, h) {
  const x = pinX(i);
  return S(k.cylinder(x, ROW_Y, PIN_R, HOLDER_H, h - 1.6, P, 20), { tone: "hi", crease: "lo" }) +
    S(k.cylinder(x, ROW_Y, CAP_R, HOLDER_H + h - 1.6, 1.6, P, 24, 0.3), { tone: "hi", crease: "lo" });
}

function carriage() {
  const out = [`<path class="iso-halo" d="${k.haloOf(k.insetPlan(CAR, 3), CAR_Z, 0.1, P)}" style="filter:blur(4px)"/>`];
  for (const y of RAILS) out.push(S(k.slabOf({ x: CAR.x + 2, y: y - 3.4, w: CAR.w - 4, d: 6.8, r: 1 }, 1.4, CAR_Z - 1.4 + 0.2, P, 2), { tone: "lo", crease: "none" }));
  out.push(S(k.slabOf(CAR, CAR_Z, CAR_TOP - CAR_Z, P, 5, 0.6), { tone: "mid" }));
  out.push(D(k.corners(CAR, 3.2).map(([x, y]) => at([x, y, CAR_TOP])), { size: 0.4, tone: "lo" }));
  out.push(L(k.ring(POST[0], POST[1], 7.6, CAR_TOP, P, 28), { tone: "faint" }));
  // coluna, abraçadeira e braço
  out.push(S(k.cylinder(POST[0], POST[1], 6, CAR_TOP, 4, P, 28), { tone: "mid" }));
  out.push(S(k.cylinder(POST[0], POST[1], 3.4, CAR_TOP + 4, ARM_Z - 6 - CAR_TOP - 4, P, 24), { tone: "mid", crease: "none" }));
  out.push(L([40, 80].map((z) => k.sideArc(POST[0], POST[1], 3.4, z, P, 14)).join(""), { tone: "faint" }));
  const clamp = { x: POST[0] - 7, y: POST[1] - 7, w: 14, d: 14, r: 2.5 };
  out.push(S(k.slabOf(clamp, ARM_Z - 6, 18, P, 4, 0.6), { tone: "mid" }));
  out.push(L(k.sideSeam(clamp, ARM_Z + 3, P, 4), { tone: "faint" }));
  const thumb = [clamp.x + clamp.w + 3, POST[1]];
  out.push(S(k.slabOf({ x: clamp.x + clamp.w, y: thumb[1] - 1.4, w: 3, d: 2.8, r: 0.8 }, ARM_Z - 3, 4, P, 2), { tone: "mid", crease: "none" }));
  out.push(S(k.cylinder(thumb[0] + 1.4, thumb[1], 2.6, ARM_Z - 4, 6, P, 20), { tone: "mid" }));
  out.push(L(k.knurl(thumb[0] + 1.4, thumb[1], 2.6, ARM_Z - 4, ARM_Z + 2, 18, P), { tone: "lo" }));
  out.push(S(k.cylinder(POST[0], POST[1], 3.4, ARM_Z + 12, POST_TOP - ARM_Z - 12, P, 24), { tone: "mid", crease: "none" }));
  out.push(S(k.cylinder(POST[0], POST[1], 4, POST_TOP, 2, P, 24), { tone: "mid" }));
  const arm = { x: -3, y: clamp.y + clamp.d, w: 6, d: ROW_Y - (clamp.y + clamp.d) - 6, r: 1.5 };
  out.push(S(k.slabOf(arm, ARM_Z, ARM_H, P, 3, 0.5), { tone: "mid" }));
  out.push(D([at([0, arm.y + 4, ARM_Z + ARM_H]), at([0, arm.y + arm.d - 3, ARM_Z + ARM_H])], { size: 0.45 }));
  // bucha onde a haste do apalpador desliza
  out.push(S(k.cylinder(0, ROW_Y, 5, ARM_Z - 4, 4 + ARM_H, P, 24), { tone: "mid" }));
  out.push(L(k.sideArc(0, ROW_Y, 5, ARM_Z - 1, P, 16), { tone: "faint" }));
  return out.join("");
}

function dial() {
  const out = [];
  out.push(S(k.cylinder(0, ROW_Y, DIAL_R, DIAL_Z, DIAL_H, P, 64, 0.8), { tone: "hi", crease: "lo" }));
  out.push(L(k.knurl(0, ROW_Y, DIAL_R, DIAL_TOP - 3.2, DIAL_TOP, 80, P, 0.3), { tone: "lo" }));
  out.push(L(k.sideArc(0, ROW_Y, DIAL_R, DIAL_TOP - 3.2, P, 40), { tone: "faint" }));
  out.push(L(k.ring(0, ROW_Y, DIAL_R - 2.2, DIAL_TOP, P, 64), { tone: "lo" }));
  const ticks = k.radialTicks(0, ROW_Y, DIAL_R - 3, 50, 5, DIAL_TOP, [1.2, 2.6], P);
  out.push(L(ticks.minor, { tone: "lo" }), L(ticks.major, { tone: "mid" }));
  // marca do volume de partida (Q0 = 0,4 volta)
  const a0 = (PIN_UNIT / PER_TURN) * Math.PI * 2;
  out.push(L(k.lineOnTop([Math.sin(a0) * (DIAL_R - 6.4), ROW_Y - Math.cos(a0) * (DIAL_R - 6.4)], [Math.sin(a0) * (DIAL_R - 3), ROW_Y - Math.cos(a0) * (DIAL_R - 3)], DIAL_TOP, P), { tone: "hi" }));
  out.push(L(k.ring(0, ROW_Y, 1.5, DIAL_TOP, P, 16), { tone: "mid" }));
  out.push(k.faceTextSvg(k.topMatrix([0, ROW_Y + 8.6], DIAL_TOP, P, "x"), "un.", { size: 2.4, tone: "lo", anchor: "middle" }));
  return out.join("");
}

function needle(h) {
  const a = (h / PER_TURN) * Math.PI * 2;
  return k.lineOnTop([-Math.sin(a) * 3.2, ROW_Y + Math.cos(a) * 3.2], [Math.sin(a) * (DIAL_R - 4), ROW_Y - Math.cos(a) * (DIAL_R - 4)], DIAL_TOP + 0.2, P);
}

function plunger(h) {
  const z = HOLDER_H + h;
  return S(k.cylinder(0, ROW_Y, 2.6, z, 1.4, P, 18), { tone: "hi", lit: true }) +
    S(k.cylinder(0, ROW_Y, 1.3, z + 1.4, ARM_Z - 4 - z - 1.4, P, 14), { tone: "hi", crease: "none", lit: true });
}

const pins0 = STEPS.map((pct) => pinH(pct, E0));
const startX = pinX(ZERO + 2);

const svg = k.figureSvg({
  width: WIDTH,
  height: HEIGHT,
  label:
    "Uma bancada de medição com quinze pinos em fila. A altura de cada pino é o volume vendido naquele preço, de −30% a +40% em passos de 5%, então o topo dos pinos desenha a curva de demanda. Um carro corre num trilho atrás dos pinos e leva um braço com relógio comparador; o apalpador desce até o pino sob ele e o ponteiro mostra o volume. Um botão na ponta esquerda ajusta a elasticidade e muda a altura de todos os pinos.",
  body: [
    plate(),
    rails(),
    `<g data-part="carriage" transform="${k.translateAlong(P, [startX, 0, 0])}">${carriage()}</g>`,
    holder(),
    `<g data-part="row">${STEPS.map((_, i) => `<g data-pin="${i}">${pin(i, pins0[i])}</g>`).join("")}`,
    `<g data-part="top" transform="${k.translateAlong(P, [startX, 0, 0])}"><g data-part="plunger">${plunger(pins0[ZERO + 2])}</g>${dial()}<path data-part="needle" class="iso-line" data-tone="lit" data-free="start" d="${needle(pins0[ZERO + 2])}" style="stroke-width:1.1"/></g></g>`,
  ],
});

const live = `
const P = ${JSON.stringify(P)};
const STEPS = ${JSON.stringify(STEPS)};
const ZERO = ${ZERO}, PIN_UNIT = ${PIN_UNIT}, PER_TURN = ${PER_TURN}, MAX_PIN = ${MAX_PIN};
const PIN_X0 = ${PIN_X0}, PIN_STEP = ${PIN_STEP}, PIN_R = ${PIN_R}, CAP_R = ${CAP_R}, ROW_Y = ${ROW_Y}, HOLDER_H = ${HOLDER_H};
const ARM_Z = ${ARM_Z}, DIAL_R = ${DIAL_R}, DIAL_TOP = ${DIAL_TOP}, EPS_KNOB = ${JSON.stringify(EPS_KNOB)};
const S = (paths, style) => solidSvg(paths, style);
const pinX = ${pinX.toString()};
const epsAngle = ${epsAngle.toString()};
const epsMark = ${epsMark.toString().replace("k.lineOnTop", "lineOnTop")};
const pin = ${pin.toString().replace(/k\./g, "")};
const needle = ${needle.toString().replace(/k\./g, "")};
const plunger = ${plunger.toString().replace(/k\./g, "")};

const root = document.querySelector(".fig-root");
const stage = root.querySelector(".iso-stage");
const svg = stage.querySelector("svg");
const carriage = svg.querySelector('[data-part="carriage"]');
const top = svg.querySelector('[data-part="top"]');
const plungerG = svg.querySelector('[data-part="plunger"]');
const needleEl = svg.querySelector('[data-part="needle"]');
const epsEl = svg.querySelector('[data-part="eps-mark"]');
const row = svg.querySelector('[data-part="row"]');
const pinEls = [...row.querySelectorAll("[data-pin]")];
const readout = root.querySelector("[data-readout]");
const still = matchMedia("(prefers-reduced-motion: reduce)");
const $ = (id) => document.getElementById(id);
const brl = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });
const int = new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 0 });
const dec = (v, d = 1) => v.toLocaleString("pt-BR", { minimumFractionDigits: d, maximumFractionDigits: d });
const pct = (v) => (v > 0.05 ? "+" : v < -0.05 ? "−" : "") + dec(Math.abs(v)) + "%";
const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));

const base = { p0: 20, q0: 10000, c: 9 };
let eps = ${E0}, epsShown = eps;
let index = ${ZERO + 2}, target = pinX(index), x = target;
let heights = STEPS.map((p) => Math.min(MAX_PIN, PIN_UNIT * Math.pow(1 + p / 100, eps)));
let tip = { at: heights[index], rate: 0 };
let frame = 0, last = 0, clock = 0, touring = true, visible = false, idleTimer = 0, orderAt = -1;
const tour = [${ZERO + 2}, ${ZERO + 6}, ${ZERO - 4}, ${ZERO}];

const want = (p) => PIN_UNIT * Math.pow(1 + p / 100, eps);
const heightUnder = (cx) => {
  // o pé do apalpador (raio 2,6) apoia no pino mais alto que estiver embaixo
  let h = 0;
  STEPS.forEach((_, i) => { if (Math.abs(pinX(i) - cx) < CAP_R + 2.6) h = Math.max(h, heights[i]); });
  return h || heights[Math.round(clamp((cx - PIN_X0) / PIN_STEP, 0, STEPS.length - 1))];
};

function order() {
  // pinos atrás do apalpador primeiro, depois o apalpador, depois os da frente
  const cut = Math.floor((x - PIN_X0) / PIN_STEP + 0.5);
  if (cut === orderAt) return;
  orderAt = cut;
  pinEls.forEach((el, i) => { if (i <= cut) row.appendChild(el); });
  row.appendChild(top);
  pinEls.forEach((el, i) => { if (i > cut) row.appendChild(el); });
}

function numbers() {
  const p = STEPS[index], P1 = base.p0 * (1 + p / 100), Q1 = base.q0 * Math.pow(1 + p / 100, eps);
  const R0 = base.p0 * base.q0, M0 = (base.p0 - base.c) * base.q0, R1 = P1 * Q1, M1 = (P1 - base.c) * Q1;
  return { p, P1, Q1, dQ: (Q1 / base.q0 - 1) * 100, dR: (R1 / R0 - 1) * 100, dM: M0 > 0 ? (M1 / M0 - 1) * 100 : 0, R1, M1 };
}
function chip(id, v) {
  const n = $(id); n.textContent = (v > 0.05 ? "▲ " : v < -0.05 ? "▼ " : "") + pct(v);
  n.dataset.dir = Math.abs(v) < 0.05 ? "flat" : v > 0 ? "up" : "down";
}
let lastText = "";
function report() {
  const n = numbers();
  const text = pct(n.p) + " · " + int.format(n.Q1) + " un. · lucro " + pct(n.dM);
  if (text !== lastText) {
    lastText = text;
    readout.textContent = text;
    $("vP").textContent = brl.format(n.P1);
    $("vQ").textContent = int.format(n.Q1); chip("dQ", n.dQ);
    $("vR").textContent = "R$ " + dec(n.R1 / 1000) + " mil"; chip("dR", n.dR);
    $("vM").textContent = "R$ " + dec(n.M1 / 1000) + " mil"; chip("dM", n.dM);
    $("pOut").textContent = pct(n.p);
    $("pOutCtl").textContent = pct(n.p);
    $("eOut").textContent = "−" + dec(-eps, 2);
    $("p").value = index;
    stage.setAttribute("aria-valuenow", String(n.p));
    stage.setAttribute("aria-valuetext", "preço " + pct(n.p) + ", volume " + int.format(n.Q1) + " unidades, lucro bruto " + pct(n.dM));
  }
}

function draw(pinsChanged) {
  carriage.setAttribute("transform", translateAlong(P, [x, 0, 0]));
  top.setAttribute("transform", translateAlong(P, [x, 0, 0]));
  plungerG.innerHTML = plunger(tip.at);
  needleEl.setAttribute("d", needle(tip.at));
  if (pinsChanged) { pinEls.forEach((el, i) => { el.innerHTML = pin(i, heights[i]); }); epsEl.setAttribute("d", epsMark(epsShown)); }
  order();
  report();
}

function tick(now) {
  const dt = last ? Math.min((now - last) / 1000, 1 / 30) : 1 / 60;
  last = now;
  const calm = still.matches;
  if (touring) { clock += dt; const next = tour[Math.floor(clock / 2.6) % tour.length]; if (next !== index) { index = next; target = pinX(index); } }
  x = calm ? target : x + (target - x) * (1 - Math.exp(-dt / 0.3));
  if (Math.abs(target - x) < 0.01) x = target;
  let pinsChanged = false;
  const goal = STEPS.map((p) => Math.min(MAX_PIN, want(p)));
  heights = heights.map((h, i) => { const g = goal[i]; const n = calm ? g : h + (g - h) * (1 - Math.exp(-dt / 0.22)); if (Math.abs(n - h) > 0.001) pinsChanged = true; return Math.abs(g - n) < 0.01 ? g : n; });
  epsShown = calm ? eps : epsShown + (eps - epsShown) * (1 - Math.exp(-dt / 0.22));
  const h = heightUnder(x);
  const drag = calm ? 2 * Math.sqrt(420) : 26;
  for (let i = 0; i < 4; i++) { tip.rate += ((h - tip.at) * 420 - tip.rate * drag) * dt / 4; tip.at += tip.rate * dt / 4; }
  if (Math.abs(h - tip.at) < 0.005 && Math.abs(tip.rate) < 0.005) { tip.at = h; tip.rate = 0; }
  draw(pinsChanged);
  const settled = !touring && x === target && tip.rate === 0 && tip.at === h && !pinsChanged;
  frame = visible && !settled ? requestAnimationFrame(tick) : 0;
}
const run = () => { if (!frame && visible) { last = 0; frame = requestAnimationFrame(tick); } };
const hold = () => { touring = false; clearTimeout(idleTimer); idleTimer = setTimeout(() => { touring = !still.matches; clock = 0; run(); }, 5000); run(); };
const goTo = (i) => { index = clamp(i, 0, STEPS.length - 1); target = pinX(index); hold(); report(); };
const setEps = (e) => { eps = clamp(e, -3, -0.2); $("e").value = eps; hold(); report(); };

new IntersectionObserver((entries) => { visible = entries[entries.length - 1].isIntersecting; if (visible) run(); }, { rootMargin: "120px 0px" }).observe(stage);
if (still.matches) touring = false;
stage.addEventListener("pointermove", (event) => {
  const box = svg.getBoundingClientRect();
  const share = clamp(((event.clientX - box.left) / box.width - 0.2) / 0.62, 0, 1);
  const i = Math.round(share * (STEPS.length - 1));
  if (i !== index || touring) goTo(i);
});
stage.addEventListener("keydown", (event) => {
  let used = true;
  if (event.key === "ArrowRight") goTo(index + 1);
  else if (event.key === "ArrowLeft") goTo(index - 1);
  else if (event.key === "ArrowUp") setEps(eps + 0.1);
  else if (event.key === "ArrowDown") setEps(eps - 0.1);
  else if (event.key === "Home") goTo(0);
  else if (event.key === "End") goTo(STEPS.length - 1);
  else used = false;
  if (used) event.preventDefault();
});
$("p").addEventListener("input", (e) => goTo(+e.target.value));
$("e").addEventListener("input", (e) => setEps(+e.target.value));
root.querySelectorAll("[data-e]").forEach((b) => b.addEventListener("click", () => setEps(+b.dataset.e)));
["p0", "q0", "c"].forEach((id) => $(id).addEventListener("input", (e) => { const v = parseFloat(e.target.value); if (isFinite(v) && v >= (id === "c" ? 0 : 0.01)) { base[id] = v; lastText = ""; report(); } }));

// tema: segue o visualizador (atributo data-theme na raiz ou preferência do sistema)
const themeOf = () => { const t = document.documentElement.getAttribute("data-theme"); return t || (matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark"); };
const syncTheme = () => root.setAttribute("data-theme", themeOf());
syncTheme();
matchMedia("(prefers-color-scheme: light)").addEventListener("change", syncTheme);
new MutationObserver(syncTheme).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
draw(true);
`;

const plateBody = k.plateHtml({
  fig: "Fig 1",
  title: "Balança de elasticidade",
  hint: "Passe o mouse para mudar o preço",
  readout: "",
  keys: [
    { mark: "lit", label: "Apalpador e ponteiro: o volume no preço escolhido" },
    { mark: "raised", label: "Quinze pinos, um por preço, de −30% a +40%" },
  ],
  caption:
    "Cada pino tem a altura do volume vendido naquele preço, Q = Q₀ · (P/P₀)^ε, então o topo da fileira é a curva de demanda. O apalpador desce até o pino sob o carro, e uma volta do ponteiro equivale a 2,5 vezes o volume de partida; a marca clara no mostrador é o volume de hoje. Girar o botão da elasticidade, na ponta esquerda, sobe ou desce todos os pinos de uma vez.",
  body: `<div class="iso-stage" tabindex="0" role="slider" aria-label="Balança de elasticidade: setas para os lados mudam o preço, setas para cima e para baixo mudam a elasticidade" aria-valuemin="-30" aria-valuemax="40" aria-valuenow="10">${svg}</div>`,
});

const panel = `
<section class="fx-panel" aria-label="Controles e resultado">
  <div class="fx-stats">
    <div><span>Novo preço</span><b id="vP"></b><i class="fx-chip" data-dir="flat" id="pOut"></i></div>
    <div><span>Volume</span><b id="vQ"></b><i class="fx-chip" id="dQ"></i></div>
    <div><span>Receita</span><b id="vR"></b><i class="fx-chip" id="dR"></i></div>
    <div><span>Lucro bruto</span><b id="vM"></b><i class="fx-chip" id="dM"></i></div>
  </div>
  <div class="fx-controls">
    <label for="p">Variação de preço <output id="pOutCtl"></output></label>
    <input type="range" id="p" min="0" max="${STEPS.length - 1}" step="1" value="${ZERO + 2}">
    <label for="e">Elasticidade (ε) <output id="eOut"></output></label>
    <input type="range" id="e" min="-3" max="-0.2" step="0.05" value="${E0}">
    <div class="fx-presets" role="group" aria-label="Exemplos de elasticidade">
      <button type="button" data-e="-0.3">Uso contínuo −0,3</button>
      <button type="button" data-e="-0.8">Marca forte −0,8</button>
      <button type="button" data-e="-1.8">Com genéricos −1,8</button>
    </div>
    <div class="fx-nums">
      <label>Preço hoje (R$)<input type="number" id="p0" value="20" min="0.01" step="0.5"></label>
      <label>Volume hoje (un.)<input type="number" id="q0" value="10000" min="1" step="500"></label>
      <label>Custo (R$/un.)<input type="number" id="c" value="9" min="0" step="0.5"></label>
    </div>
    <p class="fx-note">Valores de exemplo. A figura mostra a forma da curva; os números em reais saem do mesmo modelo com os dados acima.</p>
  </div>
</section>`;

const css = `
:root{--fx-page:#f2f2ef}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--fx-page:#0b0b0b;color-scheme:dark}}
:root[data-theme="dark"]{--fx-page:#0b0b0b;color-scheme:dark}
body{background:var(--fx-page)}
.fig-root{background:var(--anatomy-page);color:var(--anatomy-text);font:14px/1.6 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;-webkit-font-smoothing:antialiased;min-height:100vh;padding-inline:16px;padding-block:40px 64px}
.fig-root *{box-sizing:border-box}
.fig-page{width:min(680px,100%);margin:0 auto;display:grid;gap:20px}
.iso-stage{outline:none}
.iso-stage:focus-visible{outline:1px solid var(--anatomy-mid);outline-offset:4px}
.fx-panel{display:grid;gap:16px;font-family:var(--anatomy-mono)}
.fx-stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--anatomy-mid);box-shadow:0 0 0 1px var(--anatomy-mid)}
@media (max-width:560px){.fx-stats{grid-template-columns:repeat(2,minmax(0,1fr))}}
.fx-stats>div{background:var(--anatomy-card);padding:10px 12px;display:grid;gap:2px}
.fx-stats span{font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--anatomy-muted)}
.fx-stats b{font-size:16px;font-weight:500;color:var(--anatomy-strong);font-variant-numeric:tabular-nums;white-space:nowrap}
.fx-chip{font-style:normal;font-size:11.5px;font-variant-numeric:tabular-nums;color:var(--anatomy-text)}
.fx-chip[data-dir="up"]{color:var(--anatomy-green)}
.fx-chip[data-dir="down"]{color:var(--anatomy-red)}
.fx-controls{display:grid;gap:8px;font-size:12px}
.fx-controls label{display:flex;justify-content:space-between;gap:8px;color:var(--anatomy-strong)}
.fx-controls output{color:var(--anatomy-text);font-variant-numeric:tabular-nums}
.fx-controls input[type=range]{width:100%;accent-color:var(--anatomy-strong);margin:0 0 6px}
.fx-presets{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:6px}
.fx-presets button{font:inherit;font-size:11.5px;color:var(--anatomy-text);background:var(--anatomy-card);border:1px solid var(--anatomy-mid);padding:4px 10px;cursor:pointer}
.fx-presets button:hover{color:var(--anatomy-strong)}
.fx-presets button:focus-visible,.fx-nums input:focus-visible{outline:1px solid var(--anatomy-strong);outline-offset:2px}
.fx-nums{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.fx-nums label{display:grid;gap:4px;color:var(--anatomy-muted);font-size:11px}
.fx-nums input{width:100%;font:inherit;font-size:13px;color:var(--anatomy-strong);background:var(--anatomy-card);border:1px solid var(--anatomy-mid);padding:6px 8px;font-variant-numeric:tabular-nums}
.fx-note{margin:0;color:var(--anatomy-muted);font-size:11.5px;line-height:1.5}
`;

const page = `<title>Balança de Elasticidade</title>
<style>${k.ISO_CSS}${css}</style>
<div class="iso fig-root" data-theme="dark"><main class="fig-page">${plateBody}${panel}</main></div>
<script type="module">${(kitScript() + live).replace(/<\/(script)/gi, "<\\/$1")}</script>
`;
writeFileSync(OUT, page);
console.log("wrote", OUT);
