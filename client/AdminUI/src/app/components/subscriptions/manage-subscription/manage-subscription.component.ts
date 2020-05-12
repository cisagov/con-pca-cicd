import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { Router, ActivatedRoute } from '@angular/router';
import { Customer, Contact } from 'src/app/models/customer.model';
import { Subscription, SubscriptionContactModel, SubscriptionClicksModel } from 'src/app/models/subscription.model';
import { Guid } from 'guid-typescript';
import { UserService } from 'src/app/services/user.service';


@Component({
  selector: 'app-manage-subscription',
  templateUrl: './manage-subscription.component.html'
})
export class ManageSubscriptionComponent implements OnInit, OnDestroy {
  private routeSub: any;

  subscription: Subscription;

  customerId: string;

  action_MANAGE: string = 'manage';
  action_CREATE: string = 'create';
  action: string = this.action_MANAGE;

  // CREATE or MANAGE (edit existing)
  pageMode: string = 'CREATE';

  subscriptionCustomer: Customer;
  contactsForOrg: Contact[] = [];
  currentOrg: Customer = new Customer();
  currentContact: Contact = new Contact();

  startDate: Date = new Date();
  startAt = new Date();

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

    this.routeSub = this.route.params.subscribe(params => {
      if (!params.id) {
        this.pageMode = 'CREATE';
      }
      this.customerId = params.id;
    });


    if (this.pageMode == 'CREATE') {
      this.action = this.action_CREATE;
      this.subscription = new Subscription();
    }

    // get the customer and contacts from the API
    this.subscriptionSvc.getCustomer(this.customerId).subscribe((o: Customer) => {

      this.subscriptionCustomer = o;
      this.currentOrg = o;

      this.contactsForOrg = this.subscriptionSvc.getContactsForCustomer();
      this.currentContact = this.contactsForOrg[0];
    });

    // since the above subscription will fail, do some setup here
    this.subscriptionCustomer = this.subscriptionSvc.customer;
    this.subscriptionSvc.customer = this.subscriptionCustomer;
    this.currentOrg = this.subscriptionCustomer;

    this.contactsForOrg = this.subscriptionSvc.getContactsForCustomer();
    this.currentContact = this.contactsForOrg[0];
  }

  /**
   * 
   */
  changeContact(e: any) {
    this.currentContact = this.currentOrg.contacts.find(x => x.id == e.value);
  }

  /**
   * 
   */
  createAndLaunchSubscription() {
    console.log('createAndLaunchSubscription');

    // set up the subscription and persist it in the service
    this.subscription = new Subscription();

    //subscription.organization_structure = this.currentOrg;
    this.subscription.customer_uuid = "14892635-c166-4797-991f-6c266e01586e";
    //subscription.organization = "Some Company.1com";
    this.subscription.active = true;
    this.subscription.additional_contact_list = [];
    this.subscription.cb_timestamp = new Date();
    //subscription.click_list = [];
    //TODO Need service to get the current user
    //Ask Jason.
    this.subscription.created_by = "Test User REPLACEME";


    //subscription.first_report_timestamp = null;
    this.subscription.gophish_campaign_list = [];

    this.subscription.last_updated_by = this.userSvc.getCurrentUser();
    this.subscription.lub_timestamp = new Date();
    this.subscription.name = "SC-1.Matt-Daemon.1.1"; //auto generated name
    //subscription.orgKeywords = ["Test", "Debug", "Dummy Org"];
    //subscription.organization_structure = new Organization();
    this.subscription.primary_contact = new SubscriptionContactModel();
    this.subscription.primary_contact.first_name = "Barry";
    this.subscription.primary_contact.last_name = "Hansen";
    this.subscription.primary_contact.office_phone = "208-716-2687";

    //subscription.report_count = 0;
    this.subscription.start_date = this.startDate;
    this.subscription.status = "New Not Started";
    this.subscription.subscription_uuid = Guid.create().toString();

    // set the target list
    this.subscription.setTargetsFromCSV(this.csvText);

    // tags / keywords
    this.subscription.setKeywordsFromCSV(this.tags);


    // call service with everything needed to start the subscription
    this.subscriptionSvc.submitSubscription(this.subscription).subscribe(
      resp => {
        alert("Your subscription was created as " + this.subscription.name);
        this.router.navigate(['subscription']);
      });
  }

  addDays(date, days) {
    var result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  }

  ngOnDestroy() {
    this.routeSub.unsubscribe();
  }
}
