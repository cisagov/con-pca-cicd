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

  /**
   *
   */
  ngOnInit(): void {
    this.statsSvc.getAggregateStats().subscribe(result => {
      this.detail = result;

      if (!this.detail.click_rate_across_all_customers) {
        this.detail.click_rate_across_all_customers = '(none)';
      }

      if (!this.detail.average_time_to_click_all_customers) {
        this.detail.average_time_to_click_all_customers = '(none)';
      }
    },
      error => {
        console.log(error);
      });
  }
}
