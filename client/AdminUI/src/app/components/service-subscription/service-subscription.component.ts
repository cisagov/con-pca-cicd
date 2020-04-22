import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { LayoutMainService } from 'src/app/services/layout-main.service';

@Component({
  selector: 'app-service-subscription',
  styleUrls: ['./service-subscription.component.scss'],
  templateUrl: './service-subscription.component.html',
})
export class ServiceSubscriptionComponent implements OnInit {

  constructor(
    private layoutSvc: LayoutMainService
  ) { 
    layoutSvc.setTitle("Create Subscription");
  }

  ngOnInit(): void {
  }

}