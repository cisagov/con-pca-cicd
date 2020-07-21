import { Component, OnInit, Input } from '@angular/core';
import { ChartsService } from 'src/app/services/charts.service';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { humanTiming } from 'src/app/helper/utilities';

@Component({
  selector: 'app-sub-dashboard',
  templateUrl: './sub-dashboard.component.html'
})
export class SubDashboardComponent implements OnInit {
  @Input()
  subscriptionUuid: string;
  dataAvailable = false;

  chart: any = {};
  chartSent: any = {};

  numberTemplatesInUse = 0;

  // average time to first click
  avgTTFC: string;

  // average time to first report
  avgTTFR: string;

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
    this.subscriptionSvc.subBehaviorSubject.subscribe(data => {
      if ('subscription_uuid' in data && !this.subscriptionUuid) {
        this.subscriptionUuid = data.subscription_uuid;
        this.dataAvailable = true;
        this.drawGraphs();
      }
    });
  }


  /**
   * Gathers statistics and renders information for two graphs,
   * chart and chartSent.  Chart shows the various statistics for
   * how the targets have responded to the phishing emails.
   * ChartSent indicates how many emails have been sent thus far.
   */
  drawGraphs() {
    // vertical bar chart groups for stats by template level
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

    // stacked horizontal bar chart for number of emails sent vs scheduled
    this.chartSent.showXAxis = true;
    this.chartSent.showYAxis = true;
    this.chartSent.showXAxisLabel = true;
    this.chartSent.xAxisLabel = '';
    this.chartSent.showYAxisLabel = true;
    this.chartSent.yAxisLabel = '';
    this.chartSent.showDataLabel = true;
    this.chartSent.view = [500, 100];
    this.chartSent.colorScheme = this.schemeSent;

    // get content
    this.chartsSvc.getStatisticsReport(this.subscriptionUuid)
      .subscribe((stats: any) => {
        this.chart.chartResults = this.chartsSvc.formatStatistics(stats);
        this.chartSent.chartResults = this.chartsSvc.getSentEmailNumbers(stats);

        for (const k in stats.templates) {
          if (stats.templates.hasOwnProperty(k)) {
            ++this.numberTemplatesInUse;
          }
        }

        this.avgTTFC = stats.metrics.avg_time_to_first_click;
        if (!this.avgTTFC) {
          this.avgTTFC = '(no emails clicked yet)';
        } else {
          this.avgTTFC = humanTiming(stats.metrics.avg_time_to_first_click);
        }

        this.avgTTFR = stats.metrics.avg_time_to_first_report;
        if (!this.avgTTFR) {
          this.avgTTFR = '(no emails reported yet)';
        }
      });
  }

  /**
   * Prevents decimal ticks from being displayed
   */
  axisFormat(val) {
    if (val % 1 === 0 || val === 0) {
      return val.toLocaleString();
    } else {
      return '';
    }
  }
}
