import { Component, OnInit, Input } from '@angular/core';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { Subscription } from 'src/app/models/subscription.model';
import { Customer } from 'src/app/models/customer.model'

@Component({
  selector: 'customer-subscriptions.component',
  templateUrl: './customer-subscriptions.component.html',
  styleUrls: ['./customer-subscriptions.component.scss']
})

export class FileteredSubscriptionListComponent implements OnInit {
  
    @Input() customer: Customer;
    subscriptions: Subscription[]

    displayedColumns = [
      "subscription_name"
    ]

    constructor(
        public subscriptionSvc: SubscriptionService
    ){}

    ngOnInit(): void {
        this.subscriptionSvc.getSubscriptionsByCustomer(this.customer).subscribe((data: any[]) => {
          this.subscriptions = data as Subscription[]
        })        
    }
}