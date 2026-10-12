// Captures chaque section de la maquette (mobile 390 px) pour les PDF.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [src, outDir] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const fontCss = fs.readFileSync(path.join(__dirname, 'fonts-abs.css'), 'utf8');
  const frag = fs.readFileSync(src, 'utf8').replace(/<link[^>]+fonts\.g[^>]+>/g, '');
  const tmp = path.join(path.dirname(path.resolve(src)), '.tmp-sec.html');
  fs.writeFileSync(tmp, `<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>${fontCss}</style><style>body{margin:0}[hidden]{display:none!important}.meta{display:none!important}.cta.pulse{animation:none}.sticky{display:none!important}</style></head><body>${frag}</body></html>`);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  await page.goto('file://' + tmp); await page.waitForTimeout(500);
  await page.screenshot({ path: `${outDir}/f-fold.png` });
  const secs = await page.$$('body > div.bar, header.top, main > section, main > div.numbers, footer');
  const names = ['s00','s01','s02','s03','s04','s05','s06','s07','s08','s09','s10','s11','s12','s13','s14','s15'];
  for (let i = 0; i < secs.length; i++) await secs[i].screenshot({ path: `${outDir}/${names[i]}.png` });
  await (await page.$('#idees')).screenshot({ path: `${outDir}/f-ideas.png` });
  await (await page.$('#offre')).screenshot({ path: `${outDir}/f-offer.png` });
  const hero = await page.$('main > section.hero'); await hero.screenshot({ path: `${outDir}/f-hero.png` });
  // barre fixe
  await page.addStyleTag({content:'.sticky{display:block!important}'});
  await page.evaluate(() => { window.scrollTo(0, 2600); document.querySelector('#sticky').classList.add('on'); }); await page.waitForTimeout(500);
  await page.waitForTimeout(400);
  const bb = await (await page.$('#sticky')).boundingBox();
  await page.screenshot({ path: `${outDir}/s16.png`, clip: { x: 0, y: bb.y, width: 390, height: bb.height } });
  // tiroir panier
  await page.click('#stickyBtn'); await page.waitForTimeout(500); await page.click('#upBtn'); await page.waitForTimeout(200);
  await page.screenshot({ path: `${outDir}/s17.png` });
  // annotations
  await page.evaluate(() => { document.querySelector('#dClose').click(); });
  await page.evaluate(() => { const m = document.querySelector('.meta'); m.style.cssText='display:flex!important'; document.querySelector('#annotBtn').click(); window.scrollTo(0,0); });
  await page.waitForTimeout(300);
  await page.screenshot({ path: `${outDir}/f-annot.png` });
  console.log('sections', secs.length);
  await browser.close(); fs.unlinkSync(tmp);
})();
