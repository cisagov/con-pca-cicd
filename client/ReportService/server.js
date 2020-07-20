const express = require('express');
const puppeteer = require('puppeteer-core');
const { report } = require('process');

const app = express();

var port = process.env.PORT || 3030; 				// set the port
var morgan = require('morgan'); 		// log requests to the console (express4)
var bodyParser = require('body-parser'); 	// pull information from HTML POST (express4)
app.use(express.static(__dirname + '/public')); 				// set the static files location /public/img will be /img for users
app.use(morgan('dev')); 										// log every request to the console
app.use(bodyParser.urlencoded({ 'extended': 'true' })); 			// parse application/x-www-form-urlencoded
app.use(bodyParser.json()); 									// parse application/json
app.use(bodyParser.json({ type: 'application/vnd.api+json' })); // parse application/vnd.api+json as json


app.get('/api/pdf', async (req, res) => {
    // This was puppeteer.launch()
    const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://pca-browserless:3000' });
    const page = await browser.newPage();
    const reportUrl = "http://pca-web:4200/reports/monthly/0";
    await page.goto(reportUrl);
    await page.emulateMediaType('screen');
    const data = await page.screenshot();
    const pdfContent = await page.pdf({ format: 'Letter' });
    browser.close();

    return res.end(pdfContent, 'binary');
});

app.listen(port);
