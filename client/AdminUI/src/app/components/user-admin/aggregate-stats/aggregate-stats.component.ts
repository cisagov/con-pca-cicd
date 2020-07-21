import { Component, OnInit } from '@angular/core';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { SettingsService } from 'src/app/services/settings.service';
import { StatisticsService } from 'src/app/services/statistics.service';

@Component({
  selector: 'app-aggregate-stats',
  templateUrl: './aggregate-stats.component.html'
})
export class AggregateStatsComponent implements OnInit {

  detail: any;

  constructor(
    public layoutSvc: LayoutMainService,
    public settingsSvc: SettingsService,
    public statsSvc: StatisticsService
  ) {
    layoutSvc.setTitle('Aggregate Statistics');
  }

  ngOnInit(): void {
    this.statsSvc.getAggregateStats().subscribe(result => {
      this.detail = result;
    },
      error => {
        this.fake();
      });
  }

  /**
   * Drop in some dummy data until the API is ready
   */
  fake() {
    this.detail = {};
    this.detail.total_customers_enrolled = 42;
    this.detail.total_monthly_reports_sent = 211;
    this.detail.total_completed_cycle_reports_sent = 170;
    this.detail.total_yearly_reports_sent = 12;
    this.detail.total_federal = 22;
    this.detail.total_state = 41;
    this.detail.total_local = 17;
    this.detail.total_tribal = 28;
    this.detail.total_private = 10;
    this.detail.average_click_rate = '37 minutes';
    this.detail.average_time_to_click = '1 day 42 minutes';
  }
}
