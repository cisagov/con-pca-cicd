import { Component, OnInit } from '@angular/core';
import { ChartsService } from 'src/app/services/charts.service';

@Component({
  selector: 'app-sub-dashboard',
  templateUrl: './sub-dashboard.component.html'
})
export class SubDashboardComponent implements OnInit {

  chart: any = {};
  chartSentPercent: any = {};

  // average time to first click
  avgTTFC = '3 minutes';

  // average time to first report
  avgTTFR = '17 minutes';

  schemeLowMedHigh = {
    domain: ['#064875', '#fcbf10', '#007bc1' ]
  };

  /**
   * 
   */
  constructor(
    public chartsSvc: ChartsService
  ) { }

  /**
   * 
   */
  ngOnInit(): void {
    this.drawGraphs();
  }

  /**
   * 
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

    //this.chart.showLegend = true;
    //this.chart.legendPosition = 'right';

    this.chart.colorScheme = this.schemeLowMedHigh;

    // get content
    this.chart.chartResults = this.chartsSvc.getGraphs();


    this.chartSentPercent.showXAxis = true;
    this.chartSentPercent.showYAxis = true;
    this.chartSentPercent.showXAxisLabel = true;
    this.chartSentPercent.xAxisLabel = '';
    this.chartSentPercent.showYAxisLabel = true;
    this.chartSentPercent.yAxisLabel = '';
    this.chartSentPercent.showDataLabel = true;
    this.chartSentPercent.colorScheme = {
      domain: ['#336600', '#eeeeee']
    };
    this.chartSentPercent.view = [500, 100];
    this.chartSentPercent.chartResults = this.chartsSvc.getSentPercent();
  }
}
