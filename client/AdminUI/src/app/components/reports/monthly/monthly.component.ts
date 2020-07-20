import { Component, OnInit } from '@angular/core';
import { drawSvgCircle } from 'src/app/helper/svgHelpers';
import { DomSanitizer } from '@angular/platform-browser';
import { ReportsService } from 'src/app/services/reports.service';
import { ActivatedRoute } from '@angular/router';
import { ChartsService } from 'src/app/services/charts.service';

@Component({
  selector: 'app-monthly',
  templateUrl: './monthly.component.html',
  styleUrls: ['./monthly.component.scss']
})
export class MonthlyComponent implements OnInit {

  private routeSub: any;
  subscriptionUuid: string;
  reportStartDate: Date;
  detail: any;


  sentCircleSvg: any;
  openedCircleSvg: any;
  clickedCircleSvg: any;


  chart: any = {};
  schemeLowMedHigh = {
    domain: ['#064875', '#fcbf10', '#007bc1']
  };


  constructor(
    public sanitizer: DomSanitizer,
    public reportsSvc: ReportsService,
    public chartsSvc: ChartsService,
    private route: ActivatedRoute,
  ) { }

  ngOnInit(): void {

    this.routeSub = this.route.params.subscribe(params => {
      this.subscriptionUuid = params.id;
      let isDate = new Date(params.start_date)
      if(isDate.getTime()){
        this.reportStartDate = isDate
      } else {
        console.log("Invalid Date time provided, defaulting to now")
        this.reportStartDate = new Date()        
      }
      this.loadPage();
    });
  }

  loadPage() {

    // RKW -- When API is ready call this....
    this.reportsSvc.getMonthlyReport(this.subscriptionUuid, this.reportStartDate).subscribe(resp => {
      this.detail = resp;

      // build statistics by level chart
      this.chart.showXAxis = true;
      this.chart.showYAxis = true;
      this.chart.showXAxisLabel = true;
      this.chart.xAxisLabel = '';
      this.chart.showYAxisLabel = true;
      this.chart.yAxisLabel = '';
      this.chart.showDataLabel = true;
      this.chart.showLegend = true;
      this.chart.legendPosition = 'right';
      this.chart.colorScheme = this.schemeLowMedHigh;

      this.chart.chartResults = this.chartsSvc.formatReportStatsForChart(resp);

      this.renderReport();
    });
  }

  /**
   * 
   */
  renderReport() {
    // draw circles
    this.sentCircleSvg = drawSvgCircle(this.detail.metrics.number_of_email_sent_overall, this.detail.metrics.total_users_targeted);
    this.openedCircleSvg = drawSvgCircle(this.detail.metrics.number_of_opened_emails, this.detail.metrics.total_users_targeted);
    this.clickedCircleSvg = drawSvgCircle(this.detail.metrics.number_of_clicked_emails, this.detail.metrics.total_users_targeted);
  }
}
