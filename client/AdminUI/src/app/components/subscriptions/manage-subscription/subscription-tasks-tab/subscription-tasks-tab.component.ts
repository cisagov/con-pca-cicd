import { Component, OnInit } from '@angular/core';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { Subscription, Task } from 'src/app/models/subscription.model';
import { MatTableDataSource } from '@angular/material/table';
import { AppSettings } from 'src/app/AppSettings';

@Component({
  selector: 'app-subscription-tasks-tab',
  templateUrl: './subscription-tasks-tab.component.html',
  styleUrls: ['./subscription-tasks-tab.component.scss']
})
export class SubscriptionTasksTabComponent implements OnInit {
  tasks = new MatTableDataSource<Task>();

  dateFormat = AppSettings.DATE_FORMAT;

  displayedColumns = [
    'task_uuid',
    'message_type',
    'scheduled_date',
    'executed',
    'executed_date',
    'error'
  ];

  constructor(
    private subscriptionSvc: SubscriptionService,
  ) { }

  ngOnInit() {
    this.subscriptionSvc.subBehaviorSubject.subscribe(data => {
      if ('subscription_uuid' in data) {
        this.tasks.data = data.tasks;
      }
    });
  }

}
