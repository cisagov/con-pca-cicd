import { Component, OnInit } from '@angular/core';
import { NullishCoalescePipe } from 'src/app/pipes/nullish-coalesce.pipe';
import { ReportsService } from 'src/app/services/reports.service';
import { AppSettings } from 'src/app/AppSettings';
import { ActivatedRoute } from '@angular/router';
import { ChartsService } from 'src/app/services/charts.service';

@Component({
  selector: 'app-cycle',
  templateUrl: './cycle.component.html',
  styleUrls: ['./cycle.component.scss']
})
export class CycleComponent implements OnInit {

  private routeSub: any;
  subscriptionUuid: string;

  detail: any;
  recommendations: any[] = [];

  dateFormat = AppSettings.DATE_FORMAT;

  chart: any = {};
  schemeLowMedHigh = {
    domain: ['#064875', '#fcbf10', '#007bc1']
  };

  /**
   *
   */
  constructor(
    public reportsSvc: ReportsService,
    public chartsSvc: ChartsService,
    private route: ActivatedRoute,
  ) { }

  /**
   *
   */
  ngOnInit(): void {
    this.routeSub = this.route.params.subscribe(params => {
      this.subscriptionUuid = params.id;
      this.reportsSvc.getCycleReport(this.subscriptionUuid, new Date()).subscribe(resp => {
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
    });
  }

  /**
   *
   */
  renderReport() {
  }
}
