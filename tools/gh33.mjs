// Кадры GitHub для главы 3.3: Chrome с профилем ~/repo-shots-chrome на порту 9381 (вход в MaximBytecamp).
//   node tools/gh33.mjs <стадия>
const { chromium } = (await import('/Users/makarovmn/python_presentations/tools/node_modules/playwright/index.js')).default;
const OUT = '/Users/makarovmn/angular_react_makarov/temy/33-github-pages/img/raw';
const R = 'MaximBytecamp/monitoring';

const b = await chromium.connectOverCDP('http://127.0.0.1:9381');
const ctx = b.contexts()[0];

async function page(url, w = 1280, h = 800) {
  const p = await ctx.newPage();
  await p.setViewportSize({ width: w, height: h });
  await p.goto(url, { waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(2500);
  return p;
}

// Красная рамка с номером вокруг элемента — как в инструкции по репозиторию.
async function mark(p, loc, n, pad = 4) {
  await loc.first().scrollIntoViewIfNeeded().catch(() => {});
  const box = await loc.first().boundingBox();
  if (!box) throw new Error('нет элемента для метки ' + n);
  await p.evaluate(({ box, n, pad }) => {
    const r = document.createElement('div');
    r.className = 'shot-mark';
    Object.assign(r.style, { position: 'fixed', left: box.x - pad + 'px', top: box.y - pad + 'px',
      width: box.width + pad * 2 + 'px', height: box.height + pad * 2 + 'px', border: '3px solid #D7263D',
      borderRadius: '6px', zIndex: 2147483646, pointerEvents: 'none', boxSizing: 'border-box' });
    const c = document.createElement('div');
    c.className = 'shot-mark';
    c.textContent = n;
    Object.assign(c.style, { position: 'fixed', left: box.x - pad - 14 + 'px', top: box.y - pad - 14 + 'px',
      width: '26px', height: '26px', borderRadius: '50%', background: '#D7263D', color: '#fff',
      font: '700 14px/26px Inter, Arial, sans-serif', textAlign: 'center', zIndex: 2147483647,
      boxShadow: '0 0 0 2px #fff', pointerEvents: 'none' });
    document.body.append(r, c);
  }, { box, n, pad });
}

const unmark = (p) => p.evaluate(() => document.querySelectorAll('.shot-mark').forEach(e => e.remove()));

async function shot(p, name, clip) {
  await p.screenshot({ path: `${OUT}/${name}.png`, clip, animations: 'disabled' });
  console.log('  ✓', name);
}

const S = {
  async new() {
    const p = await page('https://github.com/new', 1280, 900);
    await p.locator('#repository-name-input').fill('monitoring');
    await p.waitForTimeout(1500);
    await mark(p, p.locator('#repository-name-input'), 1);
    await mark(p, p.locator('#visibility-anchor-button'), 2);
    await mark(p, p.getByRole('button', { name: 'Create repository' }), 3);
    await p.evaluate(() => window.scrollTo(0, 0));
    await shot(p, '12-gh-new', { x: 240, y: 70, width: 800, height: 830 });
    await unmark(p);
    await p.getByRole('button', { name: 'Create repository' }).click();
    await p.waitForURL(`https://github.com/${R}`, { timeout: 30000 });
    await p.waitForTimeout(2500);
    await shot(p, '13-gh-quick', { x: 0, y: 0, width: 1280, height: 800 });
    await p.close();
  },
  async quick() {
    const p = await page(`https://github.com/${R}`, 1280, 800);
    const h = p.getByText('…or push an existing repository from the command line');
    await h.scrollIntoViewIfNeeded();
    const box = await h.boundingBox();
    await shot(p, '13-gh-quick', { x: 0, y: Math.max(0, box.y - 330), width: 1280, height: 560 });
    await p.close();
  },
  async pages() {
    const p = await page(`https://github.com/${R}/settings/pages`, 1280, 760);
    await mark(p, p.getByRole('link', { name: 'Settings' }).first(), 1);
    await mark(p, p.getByRole('link', { name: 'Pages' }).first(), 2);
    const src = p.getByRole('button', { name: 'Deploy from a branch' });
    await mark(p, src, 3);
    await shot(p, '16-gh-pages', { x: 0, y: 0, width: 1280, height: 700 });
    await unmark(p);
    await src.click();
    await p.waitForTimeout(1000);
    const opt = p.getByRole('menuitemradio', { name: /GitHub Actions/ });
    await mark(p, opt, 4);
    await shot(p, '17-gh-pages-actions', { x: 300, y: 100, width: 980, height: 420 });
    await unmark(p);
    await opt.click();
    await p.waitForTimeout(2500);
    await shot(p, '18-gh-pages-vybrano', { x: 300, y: 100, width: 980, height: 520 });
    await p.close();
  },
  // Список запусков и страница последнего запуска; префикс номера кадра — из аргумента.
  async actions() {
    const n = process.argv[3];
    const p = await page(`https://github.com/${R}/actions`, 1280, 700);
    await shot(p, `${n}-gh-actions`, { x: 0, y: 0, width: 1280, height: 560 });
    await p.locator('a.Link--primary, a[href*="/actions/runs/"]').first().click();
    await p.waitForTimeout(3500);
    await shot(p, `${n}a-gh-run`, { x: 0, y: 0, width: 1280, height: 700 });
    await p.close();
  },
  async repo() {
    const p = await page(`https://github.com/${R}`, 1280, 800);
    await shot(p, process.argv[3] || '15-gh-repo');
    await p.close();
  },
};

await S[process.argv[2]]();
await b.close();
