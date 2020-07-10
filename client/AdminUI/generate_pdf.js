const puppeteer = require('puppeteer-core');

(async () => {
    const browser = await puppeteer.launch({
        headless: true,
        executablePath: process.env.CHROME_BIN,
        args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
    });
    const page = await browser.newPage();
    await page.goto('https://cisa.gov', { waitUntil: 'networkidle2' });
    await page.pdf({ path: 'hn.pdf', format: 'A4' });

    await browser.close();
})();