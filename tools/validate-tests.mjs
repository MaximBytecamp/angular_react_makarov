const CDP = 'http://127.0.0.1:9223';
const SITE = 'http://127.0.0.1:8765';
import { readFileSync, writeFileSync } from 'node:fs';

function answerKeys(module) {
  const source = readFileSync(new URL(`../testy/modul-${module}/quiz-data.js`, import.meta.url), 'utf8');
  const salt = source.match(/"salt": "([^"]+)"/)[1];
  const encoded = source.match(/const SECRET = "([^"]+)"/)[1];
  const bytes = Buffer.from(encoded, 'base64');
  const plain = Buffer.from(bytes.map((byte, i) => byte ^ salt.charCodeAt(i % salt.length)));
  return JSON.parse(plain.toString('utf8'));
}

async function target(url) {
  const response = await fetch(`${CDP}/json/new?${encodeURIComponent(url)}`, { method: 'PUT' });
  if (!response.ok) throw new Error(`CDP target: ${response.status}`);
  return response.json();
}

async function inspectModule(module) {
  const keys = answerKeys(module);
  const page = await target(`${SITE}/testy/modul-${module}/`);
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  const pending = new Map();
  const exceptions = [];
  let id = 0;
  const call = (method, params = {}) => new Promise((resolve, reject) => {
    const callId = ++id;
    pending.set(callId, { resolve, reject });
    ws.send(JSON.stringify({ id: callId, method, params }));
  });
  ws.onmessage = event => {
    const message = JSON.parse(event.data);
    if (message.id && pending.has(message.id)) {
      const job = pending.get(message.id); pending.delete(message.id);
      if (message.error) job.reject(new Error(message.error.message)); else job.resolve(message.result);
    }
    if (message.method === 'Runtime.exceptionThrown') exceptions.push(message.params.exceptionDetails.text);
  };
  await new Promise((resolve, reject) => { ws.onopen = resolve; ws.onerror = reject; });
  await call('Runtime.enable');
  await call('Page.enable');
  await new Promise(resolve => setTimeout(resolve, 700));
  const expression = `(async () => {
    localStorage.clear();
    document.querySelector('#in-name').value = 'Тестов Тест';
    document.querySelector('#in-group').value = 'ПРОВЕРКА';
    window.confirm = () => true;
    document.querySelector('#btn-start').click();
    await new Promise(r => setTimeout(r, 800));
    for (const img of document.querySelectorAll('.q-img img')) {
      img.loading = 'eager';
      img.scrollIntoView({ block: 'center' });
      await new Promise(r => setTimeout(r, 120));
    }
    window.scrollTo(0, 0);
    const before = {
      questions: document.querySelectorAll('.q').length,
      svg: document.querySelectorAll('.q-img svg').length,
      images: document.querySelectorAll('.q-img img').length,
      situations: document.querySelectorAll('.q-situation').length,
      brokenImages: [...document.querySelectorAll('.q-img img')].filter(img => !img.complete || !img.naturalWidth).length,
      codeLabels: [...document.querySelectorAll('.q-code figcaption')].map(x => x.textContent).join(' | ')
    };
    const secret = ${JSON.stringify(keys)};
    for (const q of QUIZ.questions) {
      const key = secret[q.id].key;
      state.answers[q.id] = q.type === 'number' ? String(key[0]) : [...key];
    }
    save(KEY_STATE, state);
    await finish(false);
    await new Promise(r => setTimeout(r, 300));
    return { ...before, score: document.querySelector('#score-line').textContent, review: document.querySelectorAll('.rv').length };
  })()`;
  const result = await call('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  await call('Runtime.evaluate', { expression: `document.querySelector('#rv-q01').scrollIntoView({block:'start'}); window.scrollBy(0,-80)` });
  await new Promise(resolve => setTimeout(resolve, 250));
  await call('Emulation.setDeviceMetricsOverride', { width: 1280, height: 900, deviceScaleFactor: 1, mobile: false });
  const desktop = await call('Page.captureScreenshot', { format: 'png', fromSurface: true });
  writeFileSync(`/private/tmp/angular-react-test-m${module}-1280.png`, Buffer.from(desktop.data, 'base64'));
  await call('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
  await call('Runtime.evaluate', { expression: `document.querySelector('#rv-q01').scrollIntoView({block:'start'}); window.scrollBy(0,-65)` });
  await new Promise(resolve => setTimeout(resolve, 200));
  const mobile = await call('Page.captureScreenshot', { format: 'png', fromSurface: true });
  writeFileSync(`/private/tmp/angular-react-test-m${module}-390.png`, Buffer.from(mobile.data, 'base64'));
  ws.close();
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.text);
  return { module, ...result.result.value, exceptions };
}

const results = [];
for (const module of [1, 2, 3]) results.push(await inspectModule(module));
console.log(JSON.stringify(results, null, 2));
if (results.some(r => r.questions !== 15 || r.review !== 15 || r.score !== '15 из 15 · отлично' || r.brokenImages || r.exceptions.length)) process.exit(1);
