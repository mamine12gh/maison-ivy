const { chromium } = require('playwright');
(async () => {
  const [src, out] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage();
  await p.goto('file://' + require('path').resolve(src)); await p.waitForTimeout(400);
  await p.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
  await b.close();
})();
