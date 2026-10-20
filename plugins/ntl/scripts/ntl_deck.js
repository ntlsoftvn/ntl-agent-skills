// NTL deck library for pptxgenjs: NTL cover/content layouts and the components of NTL proposal decks.
// Canvas 13.333" x 7.5" (1280x720 px at 96 px/in). Colours are hex values from references/brand.md, so the deck
// needs no theme post-processing. Needs pptxgenjs (and react, react-dom, react-icons, sharp for icons) on NODE_PATH:
// run scripts/setup_node.sh once, then NODE_PATH=<cache>/node_modules node build.js
//
//   const ntl = require("<PLUGIN>/scripts/ntl_deck.js");
//   const d = ntl.createDeck({ project: "RoadVision VN Distribution", docType: "Proposal", version: "2.0", date: "10/2026", total: 11 });
//   d.cover({ title: "RoadVision VN Distribution", subtitle: "From AWS to VN Cloud: challenges, solution, roadmap and cost" });
//   const s = d.content("Intro", "Agenda"); ...
//   await d.save("RoadVision_VN_Distribution_Proposal_v2.0.pptx");
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const H = {
  navy: "14264A", navy2: "1F396D", navy3: "3B5690", orange: "F16D22", orangeText: "C9520F",
  bg: "F1F4FA", border: "D5DBE7", text: "1E2637", muted: "667085", orangeTint: "FDE7D9", noteBg: "E9EEF7",
  white: "FFFFFF", coverText: "C9D3E6", coverSub: "DCE3F0", grid: "B8C2D6", gridMinor: "E3E8F1",
};
const FONT = "Verdana"; // stand-in for DejaVu Sans (same Bitstream Vera design, ships with Office)
const W = 13.333, HT = 7.5;
const px = (v) => v / 96; // template px -> inches
const pt = (v) => v * 0.75; // template px -> points
const ASSETS = path.join(__dirname, "..", "assets");

function createDeck({ project, docType = "Proposal", version = "1.0", date = "", total, author = "NTL Software", footer } = {}) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.title = project || "NTL document";
  pres.author = author;
  pres.company = "NTL Software";
  pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
  const FOOTER = footer || `NTL Software  ·  ${project}  ·  ${docType}`;
  const X0 = px(80), XW = W - 2 * px(80), Y0 = 1.5; // content box
  let page = 0, section = null;

  pres.defineSlideMaster({
    title: "NTL_COVER",
    background: { color: H.navy },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: px(96), y: 2.15, w: px(960), h: 1.55, fontSize: pt(54), bold: true, color: H.white, fontFace: FONT, align: "left", valign: "bottom", margin: 0 }, text: "" } },
      { placeholder: { options: { name: "body", type: "body", x: px(96), y: 4.15, w: px(1060), h: 0.9, fontSize: pt(28), color: H.coverSub, fontFace: FONT, align: "left", valign: "top", margin: 0 }, text: "" } },
    ],
  });
  pres.defineSlideMaster({
    title: "NTL_CONTENT",
    background: { color: H.white },
    margin: [px(64), px(80), px(72), px(80)],
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: px(80), y: px(56), w: px(1120), h: 0.6, fontSize: pt(38), bold: true, color: H.navy2, fontFace: FONT, align: "left", valign: "bottom", margin: 0 }, text: "" } },
      { rect: { x: px(80), y: px(56) + 0.68, w: px(84), h: px(4), fill: { color: H.orange }, line: { color: H.orange } } },
      { text: { text: FOOTER, options: { x: px(80), y: HT - px(26) - 0.2, w: 8, h: 0.2, fontSize: pt(13), color: H.muted, fontFace: FONT, margin: 0 } } },
    ],
  });

  const d = { pres, H, FONT, W, HT, X0, XW, Y0, px, pt };

  d.txt = (s, text, o = {}) =>
    s.addText(text, Object.assign({ isTextBox: true, margin: 0, valign: "top", color: H.text, fontFace: FONT, fontSize: 14 }, o));

  // Card: light background, 1px border, 6px top bar (navy, or orange for emphasis), radius 12px
  d.card = (s, x, y, w, h, name, top = H.navy2, bg = H.bg) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: px(12), fill: { color: bg }, line: { color: H.border, width: 0.75 }, objectName: name });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: px(14), rectRadius: px(6), fill: { color: top }, line: { color: top }, objectName: name + "-top" });
    s.addShape(pres.shapes.RECTANGLE, { x, y: y + px(6), w, h: px(8), fill: { color: bg }, line: { color: bg }, objectName: name + "-mask" });
  };

  // Note (blue) / callout (orange): tinted box with a 6px left bar. Pass text to fill it.
  d.box = (s, x, y, w, h, kind, name, text, o = {}) => {
    const bg = kind === "callout" ? H.orangeTint : H.noteBg, bar = kind === "callout" ? H.orange : H.navy2;
    s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: bg }, line: { color: bg }, objectName: name });
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: px(6), h, fill: { color: bar }, line: { color: bar }, objectName: name + "-bar" });
    if (text !== undefined) d.txt(s, text, Object.assign({ x: x + 0.25, y, w: w - 0.4, h, fontSize: pt(19), valign: "middle" }, o));
  };

  // [label, rest] -> bold coloured label + normal text, for callout lines: d.lead("Reference cost: ", "public price lists…")
  d.lead = (label, rest, color = H.orangeText) => [{ text: label, options: { bold: true, color } }, { text: rest }];

  d.bullets = (items) => items.map((t, i) => ({ text: t, options: { bullet: { code: "25CF" }, breakLine: i < items.length - 1 } }));

  d.pageNo = (s, n) =>
    d.txt(s, `${n} / ${total}`, { x: W - px(80) - 1.0, y: HT - px(24) - 0.22, w: 1.0, h: 0.22, fontSize: pt(15), bold: true, color: H.orange, align: "right" });

  d.section = (title) => { pres.addSection({ title }); section = title; };

  d.content = (sec, title) => {
    if (sec && sec !== section) d.section(sec);
    const s = pres.addSlide({ masterName: "NTL_CONTENT", sectionTitle: section || undefined });
    s.addText(title, { placeholder: "title" });
    page += 1;
    d.pageNo(s, page + 1);
    return s;
  };

  d.cover = ({ title, subtitle, kicker = `NTL SOFTWARE  ·  ${docType.toUpperCase()}`, versionLabel = "Version", logo = false, sectionTitle = "Intro" } = {}) => {
    d.section(sectionTitle);
    const s = pres.addSlide({ masterName: "NTL_COVER", sectionTitle });
    s.addShape(pres.shapes.RIGHT_TRIANGLE, { x: W - px(360), y: 0, w: px(360), h: px(360), rotate: 180, fill: { color: H.orange }, line: { color: H.orange }, objectName: "tri-orange" });
    s.addShape(pres.shapes.RIGHT_TRIANGLE, { x: W - px(260), y: HT - px(260), w: px(260), h: px(260), flipH: true, fill: { color: H.navy3 }, line: { color: H.navy3 }, objectName: "tri-navy" });
    if (logo) s.addImage({ path: path.join(ASSETS, "logo-white.png"), x: px(96), y: 0.55, w: 1.4, h: 1.4 * 474 / 738, objectName: "logo" });
    d.txt(s, kicker, { x: px(96), y: 1.7, w: 8, h: 0.3, fontSize: pt(16), color: H.coverText, charSpacing: 4 });
    s.addText(title || project, { placeholder: "title" });
    s.addShape(pres.shapes.RECTANGLE, { x: px(96), y: 3.85, w: px(110), h: px(4), fill: { color: H.orange }, line: { color: H.orange }, objectName: "cover-rule" });
    if (subtitle) s.addText(subtitle, { placeholder: "body" });
    s.addText([{ text: `${versionLabel} ${version}`, options: { bold: true, color: H.white } }, ...(date ? [{ text: `  ·  ${date}`, options: { color: H.coverText } }] : [])],
      { isTextBox: true, x: px(96), y: HT - px(56) - 0.25, w: 6, h: 0.25, fontSize: pt(16), fontFace: FONT, margin: 0 });
    return s;
  };

  // Agenda: [[title, page], ...]
  d.agenda = (items, title = "Agenda", sec = "Intro") => {
    const s = d.content(sec, title);
    items.forEach(([t, p], i) => {
      const y = Y0 + 0.1 + i * 0.68;
      d.txt(s, String(i + 1).padStart(2, "0"), { x: X0, y, w: 0.9, h: 0.55, fontSize: pt(34), bold: true, color: H.orange, valign: "middle" });
      d.txt(s, t, { x: X0 + 1.0, y, w: 8.0, h: 0.55, fontSize: pt(26), bold: true, color: H.navy2, valign: "middle" });
      d.txt(s, "p. " + p, { x: 10.9, y, w: 1.6, h: 0.55, fontSize: pt(20), color: H.muted, align: "right", valign: "middle" });
      if (i < items.length - 1) s.addShape(pres.shapes.LINE, { x: X0, y: y + 0.62, w: XW, h: 0, line: { color: H.border, width: 0.75 }, objectName: "agenda-line-" + i });
    });
    return s;
  };

  // Numbered points beside a diagram: [[title, text], ...]
  d.numbered = (s, items, { x = 9.35, y = Y0, w = 3.0, step = 1.27, color = H.navy2, titleSize = pt(19), textSize = pt(17) } = {}) => {
    items.forEach(([t, body], i) => {
      const yy = y + i * step;
      s.addShape(pres.shapes.OVAL, { x, y: yy + 0.05, w: 0.38, h: 0.38, fill: { color }, line: { color }, objectName: "num-" + i });
      d.txt(s, String(i + 1), { x, y: yy + 0.05, w: 0.38, h: 0.38, fontSize: 12, bold: true, color: H.white, align: "center", valign: "middle" });
      d.txt(s, t, { x: x + 0.52, y: yy, w, h: 0.45, fontSize: titleSize, bold: true, color: H.navy2, valign: "middle" });
      d.txt(s, body, { x: x + 0.52, y: yy + 0.48, w, h: step - 0.52, fontSize: textSize });
    });
  };

  // Image, or a labelled placeholder box when the file is missing (so the example deck builds anywhere)
  d.image = (s, file, { x = X0, y = Y0, w = 8.2, h = 5.06, name = "image" } = {}) => {
    if (file && fs.existsSync(file)) return s.addImage({ path: file, x, y, w, h, objectName: name });
    s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: H.bg }, line: { color: H.border, width: 1, dashType: "dash" }, objectName: name + "-placeholder" });
    d.txt(s, `Diagram: ${file ? path.basename(file) : name}`, { x, y, w, h, align: "center", valign: "middle", color: H.muted, fontSize: 14 });
  };

  // Table with a navy header row and thin row rules: header [..], rows [[..]], first column bold navy
  d.table = (s, header, rows, { x = X0, y = Y0, w = XW, colW, rowH = 0.72, headH = 0.5, fontSize = pt(19), name = "table" } = {}) => {
    const th = (t) => ({ text: t, options: { bold: true, color: H.white, fill: { color: H.navy2 }, fontSize: pt(20) } });
    const body = rows.map((r) => r.map((c, i) => ({ text: c, options: { bold: i === 0, color: i === 0 ? H.navy2 : H.text, fontSize } })));
    s.addTable([header.map(th)].concat(body), {
      x, y, w, colW, rowH: [headH].concat(rows.map(() => rowH)), valign: "middle", fontFace: FONT,
      border: [{ type: "none" }, { type: "none" }, { type: "solid", pt: 0.75, color: H.border }, { type: "none" }],
      margin: [0.08, 0.15, 0.08, 0.15], objectName: name,
    });
  };

  // Big stats: [[value, label], ...] in equal columns
  d.stats = (s, items, { y = 4.85, x = X0, w = XW, gap = px(24) } = {}) => {
    const cw = (w - (items.length - 1) * gap) / items.length;
    items.forEach(([v, label], i) => {
      const xx = x + i * (cw + gap);
      d.txt(s, v, { x: xx, y, w: cw, h: 0.85, fontSize: pt(48), bold: true, color: H.orange, valign: "bottom" });
      d.txt(s, label, { x: xx, y: y + 0.9, w: cw, h: 0.4, fontSize: pt(20), color: H.navy3 });
    });
  };

  // Roadmap Gantt: phases [[name, team, fromWeek, toWeek, md, color?, optional?]]; vertical week grid,
  // strong line every `block` weeks (labelled W1, W5, ...), MD column on the right.
  d.gantt = (s, { weeks = 20, block = 4, phases = [], x = X0, y = Y0, tx = 6.6, tw = 5.0, rowH = 0.56 } = {}) => {
    const wk = tw / weeks;
    d.txt(s, "Phase", { x, y, w: 2.9, h: 0.3, fontSize: 11, bold: true, color: H.muted });
    d.txt(s, "Proposed team", { x: 3.85, y, w: 2.7, h: 0.3, fontSize: 11, bold: true, color: H.muted });
    d.txt(s, "MD", { x: 11.75, y, w: 0.75, h: 0.3, fontSize: 11, bold: true, color: H.muted, align: "right" });
    for (let w = 1; w <= weeks; w += block) d.txt(s, "W" + w, { x: tx + (w - 1) * wk, y, w: 0.5, h: 0.3, fontSize: 10, color: H.muted });
    const top = y + 0.32, bottom = y + 0.4 + phases.length * rowH - 0.04;
    for (let w = 0; w <= weeks; w++) {
      const major = w % block === 0;
      s.addShape(pres.shapes.LINE, { x: tx + w * wk, y: top, w: 0, h: bottom - top,
        line: { color: major ? H.grid : H.gridMinor, width: major ? 0.75 : 0.5, dashType: major ? "solid" : "dash" }, objectName: "week-grid-" + w });
    }
    phases.forEach(([name, team, a, b, md, color, optional], i) => {
      const yy = y + 0.4 + i * rowH, c = color || (optional ? "F7B48A" : H.navy2);
      s.addShape(pres.shapes.LINE, { x, y: yy + rowH - 0.04, w: XW, h: 0, line: { color: H.border, width: 0.75 }, objectName: "row-line-" + i });
      d.txt(s, name, { x, y: yy, w: 3.0, h: 0.5, fontSize: pt(18), bold: !optional, valign: "middle", color: optional ? H.muted : H.navy2 });
      d.txt(s, team, { x: 3.85, y: yy, w: 2.7, h: 0.5, fontSize: pt(17), valign: "middle" });
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: tx + (a - 1) * wk, y: yy + 0.11, w: (b - a + 1) * wk, h: 0.28, rectRadius: 0.05, fill: { color: c }, line: { color: c }, objectName: "bar-" + i });
      d.txt(s, String(md), { x: 11.75, y: yy, w: 0.75, h: 0.5, fontSize: pt(18), bold: true, align: "right", valign: "middle", color: optional ? H.muted : H.navy2 });
    });
    return y + 0.4 + phases.length * rowH; // y below the last row
  };

  // Horizontal bar chart (native, single series): labels [..], values [..]
  d.barChart = (s, { labels, values, title, x = 7.15, y = Y0, w = 5.35, h = 5.05, format = "0.0", name = "chart" }) => {
    s.addChart(pres.charts.BAR, [{ name: title || "values", labels, values }], {
      x, y, w, h, barDir: "bar", chartColors: [H.navy2], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: format,
      dataLabelColor: H.text, dataLabelFontFace: FONT, dataLabelFontSize: 11, catAxisLabelColor: H.text, catAxisLabelFontFace: FONT,
      catAxisLabelFontSize: 11, catAxisOrientation: "maxMin", valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" },
      showLegend: false, showTitle: !!title, title, titleFontFace: FONT, titleFontSize: 13, titleColor: H.navy2, objectName: name,
    });
  };

  d.pageCount = () => page + 1;

  d.save = async (out) => {
    if (total && d.pageCount() !== total) console.warn(`⚠ total is ${total} but the deck has ${d.pageCount()} slides: fix "N / total"`);
    await pres.writeFile({ fileName: out });
    console.log("written", out);
  };

  // Icon in a filled circle (react-icons component), e.g. d.iconCircle(s, require("react-icons/fa").FaBullseye, x, y, 0.5)
  d.iconCircle = async (s, Comp, x, y, dia, fill = H.navy2, fg = H.white, name = "icon") => {
    const React = require("react"), ReactDOMServer = require("react-dom/server"), sharp = require("sharp");
    const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + fg, size: "256" }));
    const png = (await sharp(Buffer.from(svg)).png().toBuffer()).toString("base64");
    s.addShape(pres.shapes.OVAL, { x, y, w: dia, h: dia, fill: { color: fill }, line: { color: fill }, objectName: name + "-c" });
    const p = dia * 0.25;
    s.addImage({ data: "image/png;base64," + png, x: x + p, y: y + p, w: dia - 2 * p, h: dia - 2 * p, objectName: name + "-i" });
  };

  return d;
}

module.exports = { createDeck, H, FONT, px, pt };
