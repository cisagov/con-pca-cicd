import { Component, OnInit } from '@angular/core';
import { NullishCoalescePipe } from 'src/app/pipes/nullish-coalesce.pipe';
import { ReportsService } from 'src/app/services/reports.service';
import { AppSettings } from 'src/app/AppSettings';
import { ActivatedRoute } from '@angular/router';

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
      this.reportsSvc.getCycleReport(this.subscriptionUuid, new Date()).subscribe(resp => {
        this.detail = resp;


        // RKW - fake in some metrics
        this.fake();

        this.renderReport();
      });
    });
  }


  fake() {

    this.detail.metrics.number_of_clicked_emails = 1;
    // this.detail.metrics.number_of_email_sent_overall = 100;

    this.detail.metrics = {
      number_of_email_sent_overall: 117,
      number_of_opened_emails: 40,
      number_of_clicked_emails: 17,
      number_of_reported_emails: 3,
      averate_time_to_first_click: '07:00',
      stats: [
        {
          type: 'sent',
          low: 40,
          lowN: 0,
          moderate: 40,
          moderateN: 0,
          high: 37,
          highN: 0
        },
        {
          type: 'opened',
          low: 15,
          lowN: 0,
          moderate: 12,
          moderateN: 0,
          high: 6,
          highN: 0
        },
        {
          type: 'clicked',
          low: 1,
          lowN: 0,
          moderate: 1,
          moderateN: 0,
          high: 1,
          highN: 0
        },
        {
          type: 'submitted',
          low: 1,
          lowN: 0,
          moderate: 1,
          moderateN: 0,
          high: 1,
          highN: 0
        },
        {
          type: 'reported',
          low: 1,
          lowN: 0,
          moderate: 1,
          moderateN: 0,
          high: 1,
          highN: 0
        },
      ]
    };
  }

  /**
   *
   */
  renderReport() {
  }
}
