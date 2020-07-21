import { Component, OnInit } from '@angular/core';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { SettingsService } from 'src/app/services/settings.service';
import { StatisticsService } from 'src/app/services/statistics.service';
import { humanTiming } from 'src/app/helper/utilities';

@Component({
  selector: 'app-aggregate-stats',
  templateUrl: './aggregate-stats.component.html'
})
export class AggregateStatsComponent implements OnInit {

  detail: any;
  click_rate: string;
  avg_time_to_click: string;

  constructor(
    public layoutSvc: LayoutMainService,
    public settingsSvc: SettingsService,
    public statsSvc: StatisticsService
  ) {
    layoutSvc.setTitle('Aggregate Statistics');
  }

  /**
   *
   */
  ngOnInit(): void {
    this.statsSvc.getAggregateStats().subscribe(result => {
      this.detail = result;

      if (!this.detail.click_rate_across_all_customers) {
        this.click_rate = '(none)';
      } else {
        this.click_rate = humanTiming(this.detail.click_rate_across_all_customers);
      }

      if (!this.detail.average_time_to_click_all_customers) {
        this.avg_time_to_click = '(none)';
      } else {
        this.avg_time_to_click = humanTiming(this.detail.average_time_to_click_all_customers);
      }
    },
      error => {
        console.log(error);
      });
  }
}
