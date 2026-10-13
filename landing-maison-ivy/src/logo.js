// Mesure le « ı » dans Fredoka et écrit les SVG du logo Maison Ivy.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const css = fs.readFileSync(path.join(__dirname, 'fonts-abs.css'), 'utf8');
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage();
  await p.setContent(`<style>${css}</style><span id="t" style="font:700 80px Fredoka;letter-spacing:-1.6px;white-space:pre">maison <span id="i">ı</span>vy</span>`);
  await p.waitForTimeout(300);
  const m = await p.evaluate(() => { const t = document.getElementById('t').getBoundingClientRect(), i = document.getElementById('i').getBoundingClientRect(); return { w: t.width, ix: i.left - t.left, iw: i.width }; });
  await b.close();
  const fs80 = 80, bs = fs80 * 0.42, k = bs / 40;
  const bx = 6 + m.ix + m.iw / 2 - bs * 0.42, by = 78 - fs80 * 0.76;
  const O = id => `<g transform="translate(${bx.toFixed(1)} ${by.toFixed(1)}) scale(${k.toFixed(3)})"><defs><mask id="m${id}"><rect x="-5" y="-5" width="50" height="50" fill="#fff"/><path d="M15 1 L38 24 L50 24 L50 -10 L15 -10 Z" fill="#000"/></mask></defs><g mask="url(#m${id})" fill="#FF5A36"><circle cx="20" cy="19" r="16"/><path d="M8.5 27 L4 38.5 L17.5 33.5 Z"/></g><path d="M17.24 3.24 Q16.88 22.12 35.76 21.76 Z" fill="#FFE1D6" stroke="#E8431F" stroke-width="1.2" stroke-linejoin="round"/></g>`;
  const W = Math.ceil(m.w + 12);
  const svg = (col, id) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} 106" width="${W * 2}" height="212"><text x="6" y="78" font-family="Fredoka, sans-serif" font-weight="700" font-size="80" letter-spacing="-1.6" fill="${col}" xml:space="preserve">maison ıvy</text>${O(id)}</svg>`;
  const out = path.join(__dirname, '../assets/logo');
  fs.writeFileSync(out + '/maison-ivy-logo.svg', svg('#1E1B2E', 'a'));
  fs.writeFileSync(out + '/maison-ivy-logo-inverse.svg', svg('#FFF6EC', 'b'));
  fs.writeFileSync(out + '/maison-ivy-icone.svg', `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40" width="512" height="512">${O('c').replace(/translate\([^)]*\) scale\([^)]*\)/, 'translate(0 0) scale(1)')}</svg>`);
  console.log(m);
})();
