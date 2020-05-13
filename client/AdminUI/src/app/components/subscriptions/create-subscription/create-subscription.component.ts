import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { Router } from '@angular/router';
import { Customer, Contact } from 'src/app/models/customer.model';
import { Subscription, SubscriptionContactModel, SubscriptionClicksModel } from 'src/app/models/subscription.model';
import { Guid } from 'guid-typescript';

@Component({
  selector: 'app-create-subscription',
  templateUrl: './create-subscription.component.html'
})
export class CreateSubscriptionComponent implements OnInit {
  orgId: number;

  fullOrg: Customer;
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
    private router: Router
  ) {

  }

  /**
   * 
   */
  ngOnInit(): void {


    // TEMP
    this.orgId = 123;

    // get the customer and contacts from the API
    this.subscriptionSvc.getCustomer(this.orgId).subscribe((o: Customer) => {

      this.fullOrg = o;
      this.currentOrg = o;

      this.contactsForOrg = this.subscriptionSvc.getContactsForCustomer();
      this.currentContact = this.contactsForOrg[0];
    });

    // since the above subscription will fail, do some setup here
    this.fullOrg = this.subscriptionSvc.customer;
    this.subscriptionSvc.customer = this.fullOrg;
    this.currentOrg = this.fullOrg;

    this.contactsForOrg = this.subscriptionSvc.getContactsForCustomer();
    this.currentContact = this.contactsForOrg[0];
  }

  /**
   * 
   */
  createAndLaunchSubscription() {
    console.log('createAndLaunchSubscription');

    // set up the subscription and persist it in the service
    let subscription = new Subscription();    

    //subscription.organization_structure = this.currentOrg;
    subscription.customer_uuid = "0bd5b1c8-3f9c-482e-afe5-c9f865f890a1";
    //subscription.organization = "Some Company.1com";
    subscription.active = true;
    subscription.additional_contact_list = [];
    subscription.cb_timestamp = new Date();
    //subscription.click_list = [];
    //TODO Need service to get the current user
    //Ask Jason.
    subscription.created_by = "Test User REPLACEME";    
    //no end date at this time 
    
    //subscription.end_date =  this.addDays(new Date(),90);
    //subscription.first_report_timestamp = null;
    subscription.gophish_campaign_list = [];
    //TODO Need service to get the current user
    //Ask Jason.    
    subscription.last_updated_by = "Test User REPLACEME";
    subscription.lub_timestamp = new Date();
    subscription.name = "SC-1.Matt-Daemon.1.1"; //auto generated name
    //subscription.orgKeywords = ["Test", "Debug", "Dummy Org"];
    //subscription.organization_structure = new Organization();
    subscription.primary_contact = new SubscriptionContactModel();
    subscription.primary_contact.first_name = "Barry";
    subscription.primary_contact.last_name = "Hansen";
    subscription.primary_contact.office_phone = "208-716-2687";
    
    //subscription.report_count = 0;
    subscription.start_date = this.startDate;
    subscription.status = "New Not Started";
    subscription.subscription_uuid = Guid.create().toString();
    // set the target list
    subscription.setTargetsFromCSV(this.csvText);
    //subscription.templates_selected = [];    
    // tags / keywords
    subscription.setKeywordsFromCSV(this.tags);


    // call service with everything needed to start the subscription
    this.subscriptionSvc.submitSubscription(subscription).subscribe(
      resp => {
        alert("Your subscription was created as "+subscription.name);
        this.router.navigate(['subscription']);
      });

    // DUMMY LINE - in real life it will happen above in the subscribe
    // this.router.navigate(['subscription']);

  }

  addDays(date, days) {
    var result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  }
}
