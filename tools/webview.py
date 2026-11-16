"""Сырой CDP к webview Continue: поиск контекста выполнения с интерфейсом и вычисление JS в нём."""
import asyncio, json, urllib.request
import websockets

PORT = 9363

class Webview:
    async def __aenter__(self):
        t = next(x for x in json.load(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json')) if x['type'] == 'iframe' and 'vscode-webview' in x['url'])
        self.ws = await websockets.connect(t['webSocketDebuggerUrl'], max_size=50_000_000)
        self.n = 0; self.ctxs = []
        await self.send('Runtime.enable')
        await asyncio.sleep(1)
        self.ctx = None; best = -1
        for c in self.ctxs:
            r = await self.send('Runtime.evaluate', expression="document.querySelector('#root') ? document.body.innerText.length : -1", contextId=c)
            v = r.get('result', {}).get('value', -1)
            if isinstance(v, int) and v > best: best, self.ctx = v, c
        return self

    async def __aexit__(self, *a):
        await self.ws.close()

    async def send(self, method, **params):
        self.n += 1; my = self.n
        await self.ws.send(json.dumps({'id': my, 'method': method, 'params': params}))
        while True:
            m = json.loads(await self.ws.recv())
            if m.get('method') == 'Runtime.executionContextCreated':
                self.ctxs.append(m['params']['context']['id'])
            if m.get('id') == my:
                return m.get('result', m.get('error'))

    async def js(self, expr):
        r = await self.send('Runtime.evaluate', expression=expr, contextId=self.ctx, awaitPromise=True, returnByValue=True)
        return r.get('result', {}).get('value', r)
