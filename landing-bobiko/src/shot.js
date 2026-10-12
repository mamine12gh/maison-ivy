// Usage: node shot.js <fragment.html> <out-prefix> [widths...]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [src, out, ...ws] = process.argv.slice(2);
  const frag = fs.readFileSync(src, 'utf8');
  const fontCss = fs.readFileSync(path.join(__dirname, 'fonts-abs.css'), 'utf8');
  const doc = `<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>${fontCss}</style><style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>${frag.replace(/<link[^>]+fonts\.g[^>]+>/g,'')}</body></html>`;
  const tmp = path.join(path.dirname(path.resolve(src)), '.tmp-render.html');
  fs.writeFileSync(tmp, doc);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const w of (ws.length ? ws : ['390'])) {
    const page = await browser.newPage({ viewport: { width: +w, height: w < 600 ? 844 : 900 }, deviceScaleFactor: 2 });
    const errs = []; page.on('pageerror', e => errs.push(e.message)); page.on('console', m => { if (m.type()==='error') errs.push(m.text()) });
    await page.goto('file://' + tmp); await page.waitForTimeout(600);
    const ov = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    await page.screenshot({ path: `${out}-${w}-fold.png` });
    await page.screenshot({ path: `${out}-${w}-full.png`, fullPage: true });
    console.log(w, 'overflow', ov, 'errors', errs);
    await page.close();
  }
  await browser.close(); fs.unlinkSync(tmp);
})();
