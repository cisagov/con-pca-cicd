import { Component, OnInit, ViewChild } from '@angular/core';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { Subscription } from 'src/app/models/subscription.model';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';


@Component({
  selector: 'subscription-report-tab',
  templateUrl: './subscription-report-tab.component.html',
  styleUrls: ['./subscription-report-tab.component.scss'] 
})
export class SubscriptionReportTab implements OnInit {

  subscription: Subscription
  selectedCycle: any
  emailsSent = new MatTableDataSource<any>();
  @ViewChild(MatSort) sort: MatSort;
  displayedColumns = [
    'report',
    'sent',
    'to',
    'from',
    'bcc',
    'manual',
  ];

  constructor(
      private subscriptionSvc: SubscriptionService,
  ) {}

  ngOnInit() {
      this.subscriptionSvc.subBehaviorSubject.subscribe(data => {
          if("subscription_uuid" in data){
            this.subscription = data
            console.log(this.subscription)
            // this.subscriptionSvc.getSusbcriptionStatusEmailsSent(data.subscription_uuid).subscribe((data) => console.log("do"))
            this.emailsSent.data = this.subscriptionSvc.getSusbcriptionStatusEmailsSent(data.subscription_uuid)
            this.emailsSent.sort = this.sort;
            console.log(this.emailsSent.data)
            //@ts-ignore
            this.selectedCycle = this.subscription.cycles[0]
          }
      })
  }

  refresh() {
    // this.subscriptionSvc.getEmailsSentBySubId(this.subscription.subscription_uuid).subscribe((data: any[]) => {
    //   this.emailsSent.data = data;
    //   this.emailsSent.sort = this.sort;
    // });
  }

  downloadObject(filename, blob) {
    const a = document.createElement('a');
    const objectUrl = URL.createObjectURL(blob);
    a.href = objectUrl;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(objectUrl);
  }

  cycleChange(event){
      console.log("cycle period changed, new Value ready for choosing the correct report")
      console.log(event.value)
  }
  
  viewMonthlyReport() {
    this.subscriptionSvc.getMonthlyReport(this.subscription).subscribe(blob => {
      this.downloadObject('monthly_subscription_report.pdf', blob);
    });
  }

  viewCycleReport() {
    this.subscriptionSvc.getCycleReport(this.subscription).subscribe(blob => {
      this.downloadObject('cycle_subscription_report.pdf', blob);
    });
  }

  viewYearlyReport() {
    this.subscriptionSvc.getYearlyReport(this.subscription).subscribe(blob => {
      this.downloadObject('yearly_subscription_report.pdf', blob);
    });
  }

  sendMonthlyReport() {
    this.subscriptionSvc.sendMonthlyReport(this.subscription).subscribe(() => {
      console.log('Sending monthly report.');
    });
  }

  sendCycleReport() {
    this.subscriptionSvc.sendMonthlyReport(this.subscription).subscribe(() => {
      console.log('Sending cycle report.');
    });
  }

  sendYearlyReport() {
    this.subscriptionSvc.sendYearlyReport(this.subscription).subscribe(() => {
      console.log('Sending yearly report.');
    });
  }

}
