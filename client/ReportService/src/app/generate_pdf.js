const fs = require("fs");
const puppeteer = require('puppeteer-core');

let convertToPDf = async (reportUrl) => {
  const browser = await puppeteer.connect({ browserWSEndpoint: `ws://${process.env.BROWSERLESS_ENDPOINT}` });
  const page = await browser.newPage();
  await page.goto(reportUrl, { waitUntil: 'networkidle2' });
  await page.emulateMediaType('screen');
  const pdfContent = await page.pdf({
    format: 'Letter',
    printBackground: true
  });


  // res.on(, function(chunk) {
  //   data.push(chunk);
  // }).on('end', function() {
  //     //at this point data is an array of Buffers
  //     //so Buffer.concat() can make us a new Buffer
  //     //of all of them together
  //     var buffer = Buffer.concat(data);
  //     console.log(buffer.toString('base64'));
  // });
  await browser.close();
  return pdfContent;
};

module.exports = {
  PdfReportUrl: async function (req, res) {
    //GRR how do we deal with this api configuration. 
    //I'm not pleased with the idea of putting it in the .env.
    //this should not have to be configured it should be determined
    const uuid = req.params.subscriptionUUID
    const type = req.params.type
    const cycle = req.params.cycle

    const reportUrl = `http://${process.env.WEB_ENDPOINT}/reports/${type}/${uuid}/${cycle}`;

    const pdfContent = await convertToPDf(reportUrl);
    //res.contentType("application/pdf");
    res.setHeader("Content-Type", "application/pdf");
    res.send(pdfContent);
  }
}
