const fs = require("fs");
const puppeteer = require('puppeteer');

let convertHTMLToPDF = async (html, callback, options = null) => {
    if (typeof html !== 'string') {
        throw new Error(
            'Invalid Argument: HTML expected as type of string and received a value of a different type. Check your request body and request headers.'
        );
    }
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    page.on("error", (err) => {
      console.log(err);
    });
    page.on("pageerror", (err) => {
      console.log(err);
    });
    page.on("requestfailed", (err) => {
      console.log(err);
    });
    page.on("request", (request) => {
      console.log(request.url())
    })
    page.on("response", (response) => {
      console.log(response.status())
    })
    //await page.emulateMedia("print");

    if (!options) {
        options = { format: 'A4' };
    }
    // From https://github.com/GoogleChrome/puppeteer/issues/728#issuecomment-359047638
    // Using this method to preserve external resources while maximizing allowed size of pdf
    // Capture first request only
    await page.setRequestInterception(true);
    page.once('request', request => {
        // Fulfill request with HTML, and continue all subsequent requests
        request.respond({ body: html });
        page.on('request', request => request.continue());
    });
    await page.goto('localhost:3000').catch(function(e) { console.log(e) });

    await page.pdf(options).then(callback, function(error) {
        console.log(error);
    });
    await browser.close();
};

let callback = function(pdf) {
  fs.writeFile("/tmp/test.pdf", pdf, function(err) {
    if (err) {
      console.log("error writing file")
      console.log(err)
    }
    console.log("complete")
  })
}

function PdfReport(){
  const html = fs.readFileSync("./invoice-horizon.html").toString('utf-8')
  convertHTMLToPDF(html, callback, {printBackground: true});
}



