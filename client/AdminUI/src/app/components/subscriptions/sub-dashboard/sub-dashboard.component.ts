import { Component, OnInit, Input } from '@angular/core';
import { ChartsService } from 'src/app/services/charts.service';
import { SubscriptionService } from 'src/app/services/subscription.service';

@Component({
  selector: 'app-sub-dashboard',
  templateUrl: './sub-dashboard.component.html'
})
export class SubDashboardComponent implements OnInit {
  @Input()
  subscriptionUuid: string;

  chart: any = {};
  chartSent: any = {};

  // average time to first click
  avgTTFC = '3 minutes';

  // average time to first report
  avgTTFR = '17 minutes';

  schemeLowMedHigh = {
    domain: ['#064875', '#fcbf10', '#007bc1']
  };

  schemeSent = {
    domain: ['#336600', '#eeeeee']
  };

  /**
   *
   */
  constructor(
    public chartsSvc: ChartsService,
    private subscriptionSvc: SubscriptionService
  ) { }

  /**
   *
   */
  ngOnInit(): void {
    this.subscriptionUuid = this.subscriptionSvc.subscription.subscription_uuid;
    this.drawGraphs();
  }

  /**
   * Gathers statistics and renders information for two graphs,
   * chart and chartSent.  Chart shows the various statistics for
   * how the targets have responded to the phishing emails.
   * ChartSent indicates how many emails have been sent thus far.
   */
  drawGraphs() {
    // set display options
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

    // get content
    this.chartsSvc.getStatisticsReport(this.subscriptionUuid)
      .subscribe((stats: any) => {
        // series of vertical bar charts
        this.chart.chartResults = this.chartsSvc.formatStatistics(stats);

        // stacked horizontal bar chart for number of emails sent vs scheduled
        this.chartSent.showXAxis = true;
        this.chartSent.showYAxis = true;
        this.chartSent.showXAxisLabel = true;
        this.chartSent.xAxisLabel = '';
        this.chartSent.showYAxisLabel = true;
        this.chartSent.yAxisLabel = '';
        this.chartSent.showDataLabel = true;
        this.chartSent.colorScheme = this.schemeSent;
        this.chartSent.view = [500, 100];
        this.chartSent.chartResults = this.chartsSvc.getSentEmailNumbers(stats);
      });
  }

  /**
   * Prevents decimal ticks from being displayed
   */
  axisFormat(val) {
    if (val % 1 === 0) {
      return val.toLocaleString();
    } else {
      return '';
    }
  }
}
