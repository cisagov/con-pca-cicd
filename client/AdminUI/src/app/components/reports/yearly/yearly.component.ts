import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AppSettings } from 'src/app/AppSettings';
import { ReportsService } from 'src/app/services/reports.service';

@Component({
  selector: 'app-yearly',
  templateUrl: './yearly.component.html',
  styleUrls: ['./yearly.component.scss']
})
export class YearlyComponent implements OnInit {

  private routeSub: any;
  subscriptionUuid: string;
  reportStartDate: Date;
  detail: any;

  improvingTrend = false;
  degradingTrend = false;

  dateFormat = AppSettings.DATE_FORMAT;

  /**
   *
   */
  constructor(
    public reportsSvc: ReportsService,
    private route: ActivatedRoute,
  ) { }

  /**
   *
   */
  ngOnInit(): void {
    this.routeSub = this.route.params.subscribe(params => {
      this.subscriptionUuid = params.id;
      const isDate = new Date(params.start_date);
      const isHeadless = params.isHeadless;

      if (isDate.getTime()) {
        this.reportStartDate = isDate;
      } else {
        console.log('Invalid Date time provided, defaulting to now');
        this.reportStartDate = new Date();
      }
      this.reportsSvc.getYearlyReport(this.subscriptionUuid, this.reportStartDate, isHeadless).subscribe(resp => {
        this.detail = resp;

        this.fake();

        this.renderReport();
      },
        error => {
          console.log(error);


          this.fake();
          this.renderReport();
        });
    });
  }

  /**
   * FAKE
   */
  fake() {
    this.detail = {
      target_year: {
        start_date: '2019-01-31',
        end_date: '2020-01-31'
      }
    };
  }

  /**
   *
   */
  renderReport() {

  }
}
