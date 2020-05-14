import { Component, OnInit } from '@angular/core';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { FormControl } from '@angular/forms';
import { StatusList } from 'src/app/models/status.model';
import { Subscription } from 'src/app/models/subscription.model';
import { MatTableDataSource } from '@angular/material/table';
import { Contact, Customer } from 'src/app/models/customer.model';
import { CustomerService } from 'src/app/services/customer.service';

interface ICustomerSubscription {
  customer: Customer;
  subscription: Subscription;
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './subscriptions.component.html',
  styleUrls: ['./subscriptions.component.scss']
})
export class SubscriptionsComponent implements OnInit {
  public data_source: MatTableDataSource<ICustomerSubscription>;

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
    "last_updated",
    "active"
  ];


  constructor(
    private subscription_service: SubscriptionService,
    private customer_service: CustomerService,
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
      console.log(data)
      let subscriptions = this.subscription_service.getSubscriptions(data)
      this.customer_service.requestGetCustomers().subscribe((data: any[]) => {
        let customers = this.customer_service.getCustomers(data)
        let customerSubscriptions: ICustomerSubscription[] = []
        subscriptions.map((s: Subscription) => {
          let customerSubscription: ICustomerSubscription = {
            customer: customers.find(o => o.customer_uuid == s.customer_uuid),
            subscription: s
          }
          customerSubscriptions.push(customerSubscription);
        })
        this.data_source.data = customerSubscriptions
      })
    })
  } 

  runSearch(){
    console.log("Search is running");
    //make a call to the api to retreive the list of subscriptions 
  }
}