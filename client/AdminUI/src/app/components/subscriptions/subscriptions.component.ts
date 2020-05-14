import { Component, OnInit } from '@angular/core';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { FormControl } from '@angular/forms';
import { StatusList } from 'src/app/models/status.model';
import { Subscription } from 'src/app/models/subscription.model';
import { MatTableDataSource } from '@angular/material/table';
import { MatTab } from '@angular/material/tabs';


const subscription_data: Subscription[] = [
  {
    name: 'rand-subscription',
    primary_contact: 'Rand Al Thor',
    customer: 'Some Company',
    status: 'Waiting on SRF',
    active: true,
    start_date: new Date('2020-08-26')
  },
  {
    name: 'perrin-subscription',
    primary_contact: 'Perrin Aybara',
    customer: 'Other Company',
    status: 'Stopped',
    active: true,
    start_date: new Date('2020-04-20')
  },
  {
    name: 'matt-subscription',
    primary_contact: 'Matt Cauthon',
    customer: 'Best Company',
    status: 'Running',
    active: true,
    start_date: new Date('2020-05-13')
  }
]

@Component({
  selector: 'app-dashboard',
  templateUrl: './subscriptions.component.html',
  styleUrls: ['./subscriptions.component.scss']
})
export class SubscriptionsComponent implements OnInit {
  public data_source: MatTableDataSource<Subscription>;

  status = new FormControl();
  searchAll: string;
  searchOrganization: string;
  searchSubscriptionName: string;
  searchPrimaryContact: string;
  searchStatus: string[];

  statusList = new StatusList().staticStatusList;

  displayed_columns = [
    "name",
    "status",
    "primary_contact",
    "customer",
    "start_date",
    "active"
  ];

  

  constructor(
    private subscription_service: SubscriptionService,
    private layoutSvc: LayoutMainService
    ) { 
      layoutSvc.setTitle("Subscriptions");
    }

  ngOnInit(): void {    
    this.layoutSvc.setTitle("Subscriptions");
    this.data_source = new MatTableDataSource();

    this.refresh();
  }

  refresh() {
    this.subscription_service.requestGetSubscriptions().subscribe((data: any[]) => {
      let subscriptions = this.subscription_service.getSubscriptions(data)
      this.data_source.data = subscriptions
    })
  } 

  runSearch(){
    console.log("Search is running");
    //make a call to the api to retreive the list of subscriptions 
  }
}