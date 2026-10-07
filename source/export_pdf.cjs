// Captures each chapter of cec-brand-book.html as a 2x image for merge_pdf.py (one PDF page per chapter).
// Chrome's print layout reflows the book narrower than the screen, so we capture the screen layout instead.
// Uses the Playwright package from pesanest1 and the system Chrome. Run: node export_pdf.cjs && python merge_pdf.py
const path = require('path');
const fs = require('fs');
const { chromium } = require('C:/Users/Figbloom Digital/Desktop/mac_transfer/desktop/pesanest1/node_modules/playwright');

const ROOT = path.resolve(__dirname, '..');
const SRC = 'file:///' + path.join(ROOT, 'cec-brand-book.html').replace(/\\/g, '/');
const OUT = path.join(__dirname, 'pdf-parts');
const WIDTH = 1440;

(async () => {
  fs.rmSync(OUT, { recursive: true, force: true });
  fs.mkdirSync(OUT);
  const browser = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  const page = await browser.newPage({ viewport: { width: WIDTH, height: 900 }, deviceScaleFactor: 2, reducedMotion: 'reduce' });
  await page.goto(SRC, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.addStyleTag({ content: `
    .nav,.progress,.toc-overlay,.lightbox,.toast,.dl-meta a,.toggle{display:none!important}
    .rv,.xline .xs,.xline .xb,.xline .xt,.xline .xh{opacity:1!important;transform:none!important;transition:none!important}
    .isaiah .hl{color:#fff!important}.isaiah .w::after,.mani .last::before{transform:none!important;transition:none!important}
    .ph img{transition:none!important}` });
  await page.evaluate(() => document.querySelectorAll('.rv,[data-x],.hl').forEach(e => e.classList.add('in')));
  await page.evaluate(() => document.querySelector('#sEyebrow').dispatchEvent(new Event('input')));
  await page.waitForTimeout(800);

  const ids = await page.$$eval('section', ss => ss.map(s => s.id));
  for (const [i, id] of ids.entries()) {
    await page.locator('#' + id).screenshot({ path: path.join(OUT, String(i).padStart(2, '0') + '-' + id + '.png'), animations: 'disabled' });
    console.log(id);
  }
  await browser.close();
})();
