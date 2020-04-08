import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { Router } from '@angular/router';
import { Organization, Contact } from 'src/app/models/organization.model';

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

      this.currentOrg = this.fullOrg;

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
    // Why is the change event bound in the template 
    // not calling this method?

    console.log('changeContact');
  }

  /**
   * 
   */
  createAndLaunchSubscription() {

    console.log('createAndLaunchSubscription');
    // call service with everything needed to start the subscription
    this.subscriptionSvc.submitSubscription().subscribe(
      resp => {
        console.log('bogus.org response!');
        this.router.navigate(['subscription']);
      },
      error => {
        console.log('error');
        this.router.navigate(['subscription']);
      });

      // DUMMY LINE - in real life it will happen above in the subscribe
      this.router.navigate(['subscription']);

  }
}
