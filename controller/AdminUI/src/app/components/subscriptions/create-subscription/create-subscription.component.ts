import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-subscription',
  templateUrl: './create-subscription.component.html'
})
export class CreateSubscriptionComponent implements OnInit {
  fullOrg: any;
  contactsForOrg: any[] = [];
  currentOrg: any;
  currentContact: any;


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
    this.fullOrg = this.subscriptionSvc.getOrganization();
    this.currentOrg = this.fullOrg.organization;

    this.contactsForOrg = this.subscriptionSvc.getContactsForOrg();
    this.currentContact = this.contactsForOrg[0];

    console.log(this.currentContact);
  }

  /**
   * 
   */
  changeContact(e: any) {
    // the change event bound in the template is not calling this method...

    console.log('changeContact');
  }

  /**
   * 
   */
  createAndLaunchSubscription() {

    // call service with everything needed to start the subscription
    this.subscriptionSvc.submitSubscription(
      {

      }
    ).subscribe(
      resp => {
        console.log('bogus.org response!');
        this.router.navigate(['subscription']);
      },
      error => {
        this.router.navigate(['subscription']);
      });
  }
}
