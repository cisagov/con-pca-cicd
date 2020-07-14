import { Component, OnInit } from '@angular/core';
import { NullishCoalescePipe } from 'src/app/pipes/nullish-coalesce.pipe';

@Component({
  selector: 'app-cycle',
  templateUrl: './cycle.component.html',
  styleUrls: ['./cycle.component.scss']
})
export class CycleComponent implements OnInit {

  target_cycle: any;
  customer: any;
  primary_contact: any;
  primary_contact_email: any;
  dhs_contact_name: any;
  DHS_contact: any;
  metrics: any;
  cycles: any[];
  subscription_stats: any;
  templates_by_group: any[];
  click_time_vs_report_time: any[];

  constructor() { }

  ngOnInit(): void {
  }
}
