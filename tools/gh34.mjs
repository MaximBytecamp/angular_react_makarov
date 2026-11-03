// Кадры GitHub для главы 3.4: Chrome с профилем ~/repo-shots-chrome на порту 9381 (вход в MaximBytecamp).
//   node tools/gh34.mjs <стадия> <номер кадра>
const { chromium } = (await import('/Users/makarovmn/python_presentations/tools/node_modules/playwright/index.js')).default;
const OUT = '/Users/makarovmn/angular_react_makarov/temy/34-github-actions/img/raw';
const R = 'MaximBytecamp/monitoring';
const [stage, n] = process.argv.slice(2);

const b = await chromium.connectOverCDP('http://127.0.0.1:9381');
const ctx = b.contexts()[0];

async function page(url, w = 1280, h = 800) {
  const p = await ctx.newPage();
  await p.setViewportSize({ width: w, height: h });
  await p.goto(url, { waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(3000);
  return p;
}

// Рамки с номерами в собственном popover: он показывается последним и лежит поверх всплывающих окон GitHub.
async function mark(p, loc, num, pad = 4) {
  await loc.first().scrollIntoViewIfNeeded().catch(() => {});
  const box = await loc.first().boundingBox();
  if (!box) throw new Error('нет элемента для метки ' + num);
  await p.evaluate(({ box, num, pad }) => {
    let layer = document.getElementById('shot-layer');
    if (!layer) {
      layer = document.createElement('div');
      layer.id = 'shot-layer';
      layer.popover = 'manual';
      Object.assign(layer.style, { position: 'fixed', inset: '0', width: '100vw', height: '100vh', margin: '0',
        padding: '0', border: '0', background: 'transparent', pointerEvents: 'none', overflow: 'visible' });
      document.body.append(layer);
    }
    const r = document.createElement('div');
    Object.assign(r.style, { position: 'fixed', left: box.x - pad + 'px', top: box.y - pad + 'px',
      width: box.width + pad * 2 + 'px', height: box.height + pad * 2 + 'px', border: '3px solid #D7263D',
      borderRadius: '6px', boxSizing: 'border-box' });
    const c = document.createElement('div');
    c.textContent = num;
    Object.assign(c.style, { position: 'fixed', left: box.x - pad - 14 + 'px', top: box.y - pad - 14 + 'px',
      width: '26px', height: '26px', borderRadius: '50%', background: '#D7263D', color: '#fff',
      font: '700 14px/26px Inter, Arial, sans-serif', textAlign: 'center', boxShadow: '0 0 0 2px #fff' });
    layer.append(r, c);
    if (layer.matches(':popover-open')) layer.hidePopover();
    layer.showPopover();
  }, { box, num, pad });
}

const unmark = (p) => p.evaluate(() => document.getElementById('shot-layer')?.remove());

async function shot(p, name, clip) {
  await p.screenshot({ path: `${OUT}/${name}.png`, clip, animations: 'disabled' });
  console.log('  ✓', name);
}

async function lastRun(workflow) {
  const p = await page(`https://github.com/${R}/actions/workflows/${workflow}`, 1280, 800);
  await p.locator('a[href*="/actions/runs/"]').first().click();
  await p.waitForTimeout(3500);
  return p;
}

const S = {
  // Ручной запуск ночной проверки кнопкой Run workflow.
  async dispatch() {
    const p = await page(`https://github.com/${R}/actions/workflows/check.yml`, 1280, 560);
    await mark(p, p.getByRole('link', { name: 'Ночная проверка сайтов' }).first(), 1);
    const open = p.getByRole('button', { name: 'Run workflow' }).first();
    await mark(p, open, 2);
    await shot(p, `${n}-run-workflow`);
    await unmark(p);
    await open.click();
    await p.waitForTimeout(1500);
    // В окне вторая кнопка Run workflow — та, что ниже на странице.
    const all = p.getByRole('button', { name: 'Run workflow' });
    let go = all.first();
    for (let i = 0, y = -1; i < await all.count(); i++) {
      const box = await all.nth(i).boundingBox();
      if (box && box.y > y) { y = box.y; go = all.nth(i); }
    }
    await mark(p, go, 3);
    await shot(p, `${n}a-run-workflow`, { x: 640, y: 100, width: 640, height: 260 });
    await unmark(p);
    await go.click();
    await p.waitForTimeout(3000);
    await p.close();
  },
  // Страница последнего запуска ночной проверки; при ошибке — журнал упавшего шага.
  async run() {
    const p = await lastRun('check.yml');
    await shot(p, `${n}-run`, { x: 0, y: 0, width: 1280, height: 700 });
    const failed = p.locator('a[href*="/job/"]').filter({ hasText: 'check' }).first();
    if (process.argv[4] === 'log') {
      await failed.click();
      await p.waitForTimeout(4000);
      // Упавший шаг раскрыт; строка с отказом в доступе — в его журнале.
      await p.setViewportSize({ width: 1280, height: 900 });
      const line = p.getByText(/denied to github-actions/).locator('visible=true').first();
      await line.waitFor({ timeout: 20000 });
      await line.evaluate((e) => e.scrollIntoView({ block: 'center' }));
      await p.waitForTimeout(1200);
      await shot(p, `${n}a-log`);
    }
    await p.close();
  },
  async commits() {
    const p = await page(`https://github.com/${R}/commits/main`, 1280, 700);
    await shot(p, `${n}-commits`);
    await p.close();
  },
  async list() {
    const p = await page(`https://github.com/${R}/actions`, 1280, 760);
    await shot(p, `${n}-actions`);
    await p.close();
  },
};

await S[stage]();
await b.close();
