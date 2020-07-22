var pdf = require('./generate_pdf')

class ReportRequest {
	subscription_uuid;
	start_date;
	report_type;
	constructor(u, s, r) {
		this.report_type = r;
		this.start_date = s;
		this.subscription_uuid = u;
	}
};


module.exports = function (app) {
	app.get('/api/:type/:subscriptionUUID/:cycle/pdf/', function (req, res) {
		pdf.PdfReportUrl(req, res);
	});

	// application -------------------------------------------------------------
	app.get('*', function (req, res) {
		res.sendfile('./public/index.html'); // load the single view file (angular will handle the page changes on the front-end)
	});
};
