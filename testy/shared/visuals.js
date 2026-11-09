/* Переиспользуемые SVG-схемы для заданий. */
const QUIZ_VIS = (() => {
  const escSvg = value => String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const wrap = (text, max = 22) => {
    const lines = []; let line = '';
    String(text).split(/\s+/).forEach(word => {
      if (line && (line + ' ' + word).length > max) { lines.push(line); line = word; }
      else line += (line ? ' ' : '') + word;
    });
    if (line) lines.push(line);
    return lines.slice(0, 3);
  };
  const textLines = (text, x, y, max = 22, cls = 'v-text') => wrap(text, max)
    .map((line, i) => `<text x="${x}" y="${y + i * 19}" class="${cls}">${escSvg(line)}</text>`).join('');
  const base = body => `<svg viewBox="0 0 760 250" role="img" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><style>
    .v-bg{fill:#f2f1e9}.v-box{fill:#fff;stroke:#020835;stroke-width:3}.v-dark{fill:#020835}.v-blue{fill:#2d7fc1}.v-pink{fill:#c2185b}.v-mint{fill:#dff3e6}.v-warn{fill:#f7e2d4}.v-line{stroke:#020835;stroke-width:3;fill:none}.v-text{fill:#020835;font:600 15px Inter,Arial,sans-serif}.v-small{fill:#3b4467;font:500 12px 'Roboto Mono',monospace}.v-white{fill:#fff;font:700 14px Inter,Arial,sans-serif}.v-label{fill:#fff;font:700 11px 'Roboto Mono',monospace;letter-spacing:1px}.v-arrow{fill:#020835}
  </style><rect width="760" height="250" class="v-bg"/>${body}</svg>`;
  function flow(items, accents = []) {
    const n = items.length, gap = 34, boxW = Math.min(150, (700 - gap * (n - 1)) / n);
    const start = (760 - (boxW * n + gap * (n - 1))) / 2;
    let body = '';
    items.forEach((item, i) => {
      const x = start + i * (boxW + gap);
      const fill = accents[i] === 'blue' ? 'v-blue' : accents[i] === 'pink' ? 'v-pink' : accents[i] === 'mint' ? 'v-mint' : accents[i] === 'warn' ? 'v-warn' : 'v-box';
      body += `<rect x="${x}" y="78" width="${boxW}" height="94" rx="4" class="${fill}${fill === 'v-box' ? '' : ' v-box'}"/>`;
      body += textLines(item, x + 13, 112, Math.max(12, Math.floor(boxW / 7.5)), accents[i] === 'blue' || accents[i] === 'pink' ? 'v-white' : 'v-text');
      if (i < n - 1) { const ax = x + boxW + 7; body += `<line x1="${ax}" y1="125" x2="${ax + gap - 14}" y2="125" class="v-line"/><polygon points="${ax + gap - 14},119 ${ax + gap - 4},125 ${ax + gap - 14},131" class="v-arrow"/>`; }
    });
    return base(body);
  }
  function compare(leftTitle, leftItems, rightTitle, rightItems) {
    const column = (x, title, items, color) => `<rect x="${x}" y="34" width="320" height="182" rx="4" class="v-box"/><rect x="${x}" y="34" width="320" height="40" class="${color}"/><text x="${x + 16}" y="60" class="v-label">${escSvg(title)}</text>${items.map((it, i) => `<circle cx="${x + 22}" cy="${101 + i * 34}" r="5" class="${color}"/>${textLines(it, x + 38, 106 + i * 34, 35, 'v-text')}`).join('')}`;
    return base(column(42, leftTitle, leftItems, 'v-blue') + column(398, rightTitle, rightItems, 'v-pink'));
  }
  function browser(path, title, lines = []) {
    return base(`<rect x="70" y="25" width="620" height="200" rx="6" class="v-box"/><rect x="70" y="25" width="620" height="48" class="v-dark"/><circle cx="96" cy="49" r="7" fill="#f06d6d"/><circle cx="119" cy="49" r="7" fill="#f0c66d"/><circle cx="142" cy="49" r="7" fill="#6fd39a"/><rect x="175" y="37" width="485" height="25" rx="4" fill="#fff"/><text x="190" y="55" class="v-small">${escSvg(path)}</text><text x="100" y="111" class="v-text">${escSvg(title)}</text>${lines.map((line, i) => `<rect x="100" y="${130 + i * 28}" width="${Math.min(500, 155 + String(line).length * 7)}" height="20" fill="${i % 2 ? '#dff3e6' : '#e3f1fa'}"/><text x="110" y="${145 + i * 28}" class="v-small">${escSvg(line)}</text>`).join('')}`);
  }
  function tree(root, children) {
    const n = children.length, boxW = Math.min(180, 650 / n - 20), gap = (650 - boxW * n) / Math.max(1, n - 1), start = 55;
    let body = `<rect x="290" y="25" width="180" height="55" rx="4" class="v-blue v-box"/>${textLines(root, 310, 58, 18, 'v-white')}`;
    children.forEach((child, i) => { const x = start + i * (boxW + gap), cx = x + boxW / 2; body += `<path d="M380 80 V115 H${cx} V145" class="v-line"/><rect x="${x}" y="145" width="${boxW}" height="70" rx="4" class="v-box"/>${textLines(child, x + 12, 177, Math.max(14, Math.floor(boxW / 7.5)), 'v-text')}`; });
    return base(body);
  }
  function timeline(items, active = []) {
    const step = 620 / Math.max(1, items.length - 1); let body = `<line x1="70" y1="105" x2="690" y2="105" class="v-line"/>`;
    items.forEach((item, i) => { const x = 70 + step * i; body += `<circle cx="${x}" cy="105" r="14" class="${active.includes(i) ? 'v-pink' : 'v-blue'}"/><text x="${x}" y="110" text-anchor="middle" class="v-label">${i + 1}</text>${textLines(item, Math.max(8, x - 55), 148, 16, 'v-small')}`; });
    return base(body);
  }
  return { flow, compare, browser, tree, timeline };
})();
