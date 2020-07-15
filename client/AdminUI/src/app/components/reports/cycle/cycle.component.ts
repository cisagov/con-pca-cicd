import { Component, OnInit } from '@angular/core';
import { NullishCoalescePipe } from 'src/app/pipes/nullish-coalesce.pipe';
import { ReportsService } from 'src/app/services/reports.service';
import { AppSettings } from 'src/app/AppSettings';

@Component({
  selector: 'app-cycle',
  templateUrl: './cycle.component.html',
  styleUrls: ['./cycle.component.scss']
})
export class CycleComponent implements OnInit {

  detail: any;

  dateFormat = AppSettings.DATE_FORMAT;

  /**
   *
   */
  constructor(
    public reportsSvc: ReportsService,
  ) { }

  /**
   *
   */
  ngOnInit(): void {
    const u1 = 'bf9db4d1-3789-4065-8bab-c663dfecbcfc';
    const u2 = 'fd13b4ce-3fb1-4645-961a-175099cb5e83';
    this.reportsSvc.getCycleReport(u2, new Date()).subscribe(resp => {
      this.detail = resp;

      console.log(resp);

      // RKW - fake in some metrics
      this.detail.metrics.number_of_clicked_emails = 1;
      //this.detail.metrics.number_of_email_sent_overall = 100;


      this.renderReport();
    });
  }

  /**
   *
   */
  renderReport() {
  }
}
