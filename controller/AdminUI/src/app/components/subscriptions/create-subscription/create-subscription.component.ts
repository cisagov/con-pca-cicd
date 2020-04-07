import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { SubscriptionService } from 'src/app/services/subscription.service';

@Component({
  selector: 'app-create-subscription',
  templateUrl: './create-subscription.component.html'
})
export class CreateSubscriptionComponent implements OnInit {
  contactsForOrg: any[] = [];
  orgContact: any;




  constructor(
    public subscriptionSvc: SubscriptionService
  ) {
  }

  ngOnInit(): void {

    
    this.orgContact = this.subscriptionSvc.getOrganization();

    this.contactsForOrg = this.subscriptionSvc.getContactsForOrg();
  }

  changeContact(e) {
    console.log(e);
  }

}
