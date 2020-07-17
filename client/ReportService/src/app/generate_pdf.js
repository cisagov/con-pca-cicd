const fs = require("fs");
const puppeteer = require('puppeteer');

let convertToPDf = async (reportUrl) => {
    const browser = await puppeteer.launch({
        headless: true,
        executablePath: process.env.CHROME_BIN,
        args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
    });
    const page = await browser.newPage();
    await page.goto(reportUrl, { waitUntil: 'networkidle2' });    
    await page.emulateMediaType('screen');
    const pdfContent = await page.pdf({ format: 'A4' });


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
  PdfReport : function (){
    const html = fs.readFileSync("./public/test.html").toString('utf-8')
    convertHTMLToPDF(html, callback, {printBackground: true});
  },
  PdfReportUrl : async function(req,res){
      //GRR how do we deal with this api configuration. 
      //I'm not pleased with the idea of putting it in the .env.
      //this should not have to be configured it should be determined
    
      const reportUrl = "http://localhost:4200/reports/monthly/"+req.params.subscription_uuid;
      const pdfContent = await convertToPDf(reportUrl);      
      //res.contentType("application/pdf");
      res.setHeader("Content-Type", "application/pdf");
      res.send(pdfContent);
  }
}



