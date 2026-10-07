// Prints the four letterhead concepts from letterhead-concepts.html as A4 pages (vector text).
// Uses the Playwright package from pesanest1 and the system Chrome. Run: node export_concepts_pdf.cjs
const path = require('path');
const { chromium } = require('C:/Users/Figbloom Digital/Desktop/mac_transfer/desktop/pesanest1/node_modules/playwright');

(async () => {
  const src = 'file:///' + path.join(__dirname, 'letterhead-concepts.html').replace(/\\/g, '/');
  const browser = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  const page = await browser.newPage();
  await page.goto(src, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: path.join(__dirname, 'CEC Letterhead Concepts.pdf'), preferCSSPageSize: true, printBackground: true });
  await browser.close();
  console.log('done');
})();
