import { Component, OnInit } from '@angular/core';
import { FormControl, NgForm, FormGroupDirective, Validators } from '@angular/forms';
import { MyErrorStateMatcher } from '../../../helper/ErrorStateMatcher';

@Component({
  selector: 'app-add-organization',
  templateUrl: './add-organization.component.html',
  styleUrls: ['./add-organization.component.scss']
})
export class AddOrganizationComponent implements OnInit {

   model:any;
   addContact:boolean = false;

   matchOrganizationName = new MyErrorStateMatcher();
   matchOrganizationIdentifier = new MyErrorStateMatcher();
   matchAddress1 = new MyErrorStateMatcher();
   matchCity = new MyErrorStateMatcher();
   matchState = new MyErrorStateMatcher();
   matchZip = new MyErrorStateMatcher();
   
   organizationId = new FormControl('');
   organizationName = new FormControl('', [Validators.required]);
   organizationIdentifier = new FormControl('', [Validators.required]);
   address1 = new FormControl('', [Validators.required]);
   address2 = new FormControl('');
   city = new FormControl('', [Validators.required]);
   state = new FormControl('', [Validators.required]);
   zip = new FormControl('', [Validators.required]);

  constructor() { }

  showAddContact(){
    this.addContact = this.addContact ? false : true;
  }

  ngOnInit(): void {
    
  }
}