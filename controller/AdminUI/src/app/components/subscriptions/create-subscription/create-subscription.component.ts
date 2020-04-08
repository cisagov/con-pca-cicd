import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { Router } from '@angular/router';
import { Organization, Contact } from 'src/app/models/organization.model';
import { Subscription } from 'src/app/models/subscription.model';

@Component({
  selector: 'app-create-subscription',
  templateUrl: './create-subscription.component.html'
})
export class CreateSubscriptionComponent implements OnInit {
  orgId: number;

  fullOrg: Organization;
  contactsForOrg: Contact[] = [];
  currentOrg: Organization = new Organization();
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

    // get the organization and contacts from the API
    this.subscriptionSvc.getOrganization(this.orgId).subscribe((o: Organization) => {

      this.fullOrg = o;
      this.currentOrg = o;

      this.contactsForOrg = this.subscriptionSvc.getContactsForOrg();
      this.currentContact = this.contactsForOrg[0];
    });

    // since the above subscription will fail, do some setup here
    this.fullOrg = this.subscriptionSvc.organization;
    this.subscriptionSvc.organization = this.fullOrg;
    this.currentOrg = this.fullOrg;

    this.contactsForOrg = this.subscriptionSvc.getContactsForOrg();
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
    let subscription = new Subscription();
    this.subscriptionSvc.subscription = subscription;

    subscription.organization = this.currentOrg;

    // start date
    subscription.startDate = this.startDate;

    // tags / keywords
    subscription.setKeywordsFromCSV(this.tags);

    // set the target list
    subscription.setTargetsFromCSV(this.csvText);

    // call service with everything needed to start the subscription
    this.subscriptionSvc.submitSubscription().subscribe(
      resp => {
        this.router.navigate(['subscription']);
      });

    // DUMMY LINE - in real life it will happen above in the subscribe
    this.router.navigate(['subscription']);

  }
}
