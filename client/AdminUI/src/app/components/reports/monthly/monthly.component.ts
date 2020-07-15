import { Component, OnInit } from '@angular/core';
import { drawSvgCircle } from 'src/app/helper/svgHelpers';
import { DomSanitizer } from '@angular/platform-browser';
import { ReportsService } from 'src/app/services/reports.service';
import { analyzeAndValidateNgModules } from '@angular/compiler';

@Component({
  selector: 'app-monthly',
  templateUrl: './monthly.component.html',
  styleUrls: ['./monthly.component.scss']
})
export class MonthlyComponent implements OnInit {

  detail: any;


  sentCircleSvg: any;
  openedCircleSvg: any;
  clickedCircleSvg: any;

  groups: any[] = [];
  groupX = 90;
  graphHeight = 100;


  constructor(
    public sanitizer: DomSanitizer,
    public reportsSvc: ReportsService,
  ) { }

  ngOnInit(): void {
    // this.reportsSvc.getMonthlyReport('XXXXXXXXXXX', new Date()).subscribe(resp => {
    //   this.renderReport(resp);
    // });

    // RKW TEMP BEGIN - create dummy response
    const resp = {
      start_date: '',
      end_date: '',
      customer_name: 'Ed Debevic\'s',
      customer_address: '600 West Cruz Avenue',
      customer_address_2: 'Suite #400',
      primary_contact_name: 'Edward Debevic',
      primary_contact_email: 'ed@eds.comm',
      dhs_contact_email: 'Andrew Bernard',
      dhs_contact_mobile_phone: '710-555-1982',
      total_users_targeted: 517,
      metrics: {
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
      }
    };

    // determine normalization factor based on highest count
    let max = 0;
    resp.metrics.stats.forEach((x) => {
      if (x.low > max) {
        max = x.low;
      }
      if (x.moderate > max) {
        max = x.moderate;
      }
      if (x.high > max) {
        max = x.high;
      }
    });
    const normalizationFactor = this.graphHeight / max;

    // normalize the counts
    resp.metrics.stats.forEach((x) => {
      x.lowN = x.low * normalizationFactor;
      x.moderateN = x.moderate * normalizationFactor;
      x.highN = x.high * normalizationFactor;
    });

    this.detail = resp;
    this.renderReport(this.detail);
    // RKW TEMP END
  }

  /**
   * 
   */
  renderReport(data: any) {

    data.metrics.percent_of_clicked_emails = data.metrics.number_of_clicked_emails / data.metrics.number_of_email_sent_overall;
    data.metrics.percent_of_reported_emails = data.metrics.number_of_reported_emails / data.metrics.number_of_email_sent_overall;

    // circles
    this.sentCircleSvg = drawSvgCircle(data.metrics.number_of_email_sent_overall, data.total_users_targeted);
    this.openedCircleSvg = drawSvgCircle(data.metrics.number_of_opened_emails, data.total_users_targeted);
    this.clickedCircleSvg = drawSvgCircle(data.metrics.number_of_clicked_emails, data.total_users_targeted);
  }
}
