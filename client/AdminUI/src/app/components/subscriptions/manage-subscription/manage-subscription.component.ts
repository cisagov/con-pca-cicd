import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { Router, ActivatedRoute } from '@angular/router';
import { Customer, Contact } from 'src/app/models/customer.model';
import { Subscription, SubscriptionClicksModel } from 'src/app/models/subscription.model';
import { Guid } from 'guid-typescript';
import { UserService } from 'src/app/services/user.service';


@Component({
  selector: 'app-manage-subscription',
  templateUrl: './manage-subscription.component.html'
})
export class ManageSubscriptionComponent implements OnInit, OnDestroy {
  private routeSub: any;


  action_MANAGE: string = 'manage';
  action_CREATE: string = 'create';
  action: string = this.action_MANAGE;

  // CREATE or MANAGE (edit existing)
  pageMode: string = 'CREATE';

  customer: Customer;
  customerContacts: Contact[] = [];
  primaryContact: Contact = new Contact();

  startDate: Date = new Date();
  startAt = new Date();

  url: string;
  tags: string;

  // The raw CSV content of the textarea
  csvText: string;

  /**
   * 
   */
  constructor(
    public subscriptionSvc: SubscriptionService,
    private router: Router,
    private route: ActivatedRoute,
    private userSvc: UserService
  ) {

  }

  /**
   * 
   */
  ngOnInit(): void {
    this.pageMode = 'MANAGE';

    this.subscriptionSvc.subscription = new Subscription();
    let sub = this.subscriptionSvc.subscription;

    this.routeSub = this.route.params.subscribe(params => {
      if (!params.id) {
        this.pageMode = 'CREATE';
        sub = new Subscription();
        sub.subscription_uuid = Guid.create().toString();
      } else {
        sub.subscription_uuid = params.id;
      }

      if (this.pageMode == 'CREATE') {
        this.action = this.action_CREATE;

        // TEMP TEMP TEMP
        sub.customer_uuid = '14892635-c166-4797-991f-6c266e01586e';
      }


      // get the customer and contacts from the API
      this.subscriptionSvc.getCustomer(sub.customer_uuid).subscribe((c: Customer) => {
        this.customer = c;

        this.customerContacts = this.subscriptionSvc.getContactsForCustomer(c);
        console.log('customerContacts: ');
        console.log(this.customerContacts);

        this.primaryContact = this.customerContacts[0];
        console.log('primaryContact: ');
        console.log(this.primaryContact);
      });
    });
  }

  /**
   * 
   */
  changePrimary(e: any) {
    this.primaryContact = this.customer.contact_list.find(x => x.first_name == e.value);
  }

  /**
   * 
   */
  createAndLaunchSubscription() {
    console.log('createAndLaunchSubscription');

    let sub = this.subscriptionSvc.subscription;

    // set up the subscription and persist it in the service
    sub = new Subscription();

    sub.customer_uuid = "14892635-c166-4797-991f-6c266e01586e";
    sub.primary_contact = this.primaryContact;
    sub.additional_contact_list = [];

    sub.active = true;

    sub.created_by = this.userSvc.getCurrentUser();

    sub.gophish_campaign_list = [];

    sub.last_updated_by = this.userSvc.getCurrentUser();
    sub.lub_timestamp = new Date();

    sub.name = "SC-1.Matt-Daemon.1.1"; //auto generated name


    sub.start_date = this.startDate;
    sub.status = "New Not Started";

    // set the target list
    sub.setTargetsFromCSV(this.csvText);

    sub.url = this.url;

    // tags / keywords
    sub.keywords = this.tags;


    // call service with everything needed to start the subscription
    this.subscriptionSvc.submitSubscription(sub).subscribe(
      resp => {
        alert("Your subscription was created as " + sub.name);
        this.router.navigate(['subscriptions']);
      },
      error => {
        console.log(error);
        alert("An error occurred submitting the subscription: " + error.error);
      });
  }

  /**
   * 
   * @param date 
   * @param days 
   */
  addDays(date, days) {
    var result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  }

  /**
   * 
   */
  ngOnDestroy() {
    this.routeSub.unsubscribe();
  }
}
