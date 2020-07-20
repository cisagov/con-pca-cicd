const express = require('express');
const puppeteer = require('puppeteer-core');
const { report } = require('process');

const app = express();

app.get('/api/pdf', async (req, res) => {
    // This was puppeteer.launch()
    const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://pca-browserless:3000' });
    const page = await browser.newPage();
    const reportUrl = "https://google.com/";
    await page.goto(reportUrl);
    const data = await page.screenshot();
    browser.close();

    return res.end(data, 'binary');
});

app.listen(3030);
