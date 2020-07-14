import { Component, OnInit } from '@angular/core';
import { drawSvgCircle } from 'src/app/helper/svgHelpers';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-monthly',
  templateUrl: './monthly.component.html',
  styleUrls: ['./monthly.component.scss']
})
export class MonthlyComponent implements OnInit {

  start_date: any;
  end_date: any;
  customer_name: any;
  customer_address: any;
  customer_address_2: any;
  primary_contact_name: any;
  primary_contact_email: any;
  dhs_contact_email: any;
  dhs_contact_mobile_phone: any;
  metrics: any;
  total_users_targeted: number;
  sent_circle_svg: any;
  opened_circle_svg: any;
  clicked_circle_svg: any;

  groups: any[] = [];
  groupX = 90;
  graph_height = 100;


  constructor(
    public sanitizer: DomSanitizer
  ) { }

  ngOnInit(): void {

    // RKW TEMP BEGIN
    this.metrics = {};
    this.metrics.number_of_email_sent_overall = 100;
    this.metrics.number_of_opened_emails = 10;
    this.metrics.number_of_clicked_emails = 7;
    this.total_users_targeted = 517;
    // RKW TEMP END

    this.sent_circle_svg = drawSvgCircle(this.metrics['number_of_email_sent_overall'], this.total_users_targeted);
    this.opened_circle_svg = drawSvgCircle(this.metrics['number_of_opened_emails'], this.total_users_targeted);
    this.clicked_circle_svg = drawSvgCircle(this.metrics['number_of_clicked_emails'], this.total_users_targeted);




    this.groups.push({ name: 'Sent', lowNormalized: 20, modNormalized: 50, highNormalized: 90 });
    this.groups.push({ name: 'Opened', lowNormalized: 20, modNormalized: 50, highNormalized: 90 });
    this.groups.push({ name: 'Clicked', lowNormalized: 20, modNormalized: 50, highNormalized: 30 });
    this.groups.push({ name: 'Submitted', lowNormalized: 20, modNormalized: 50, highNormalized: 90 });
    this.groups.push({ name: 'Reported', lowNormalized: 20, modNormalized: 50, highNormalized: 90 });

  }


}
