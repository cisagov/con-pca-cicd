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
    this.reportsSvc.getCycleReport('bf9db4d1-3789-4065-8bab-c663dfecbcfc', new Date()).subscribe(resp => {
      this.detail = resp;
      this.renderReport();
    });
  }

  /**
   *
   */
  renderReport() {
  }
}
