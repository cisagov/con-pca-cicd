import { Component, OnInit } from '@angular/core';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'src/app/models/subscription.model';
import { Customer } from 'src/app/models/customer.model';
import { CustomerService } from 'src/app/services/customer.service';

interface ICustomerSubscription {
  customer: Customer;
  subscription: Subscription;
}

@Component({
  selector: 'app-view-subscription',
  templateUrl: './view-subscription.component.html',
  styleUrls: ['./view-subscription.component.scss']
})
export class ViewSubscriptionComponent implements OnInit {
  public data: ICustomerSubscription;
  public start_at = new Date();
  public csv_text: string;

  constructor(
    private subscription_service: SubscriptionService,
    private customer_service: CustomerService,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.get_subscription(params.id)
    })
  }

  private get_subscription(subscription_uuid: string) {
    this.subscription_service.getSubscription(subscription_uuid).subscribe((data: any) => {
      let subscription = this.subscription_service.toSubscription(data)
      this.customer_service.getCustomer(subscription.customer_uuid).subscribe((data: any) => {
        let customer = this.customer_service.toCustomer(data)
        this.data = {
          customer: customer,
          subscription: subscription
        }
      })
    })
  }
}
