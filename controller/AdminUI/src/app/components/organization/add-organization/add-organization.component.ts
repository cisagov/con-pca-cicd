import { Component, OnInit } from '@angular/core';
import { FormControl, NgForm, FormGroupDirective, Validators, FormGroup } from '@angular/forms';
import { MyErrorStateMatcher } from '../../../helper/ErrorStateMatcher';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { Contact, Organization } from 'src/app/models/organization.model';

@Component({
  selector: 'app-add-organization',
  templateUrl: './add-organization.component.html',
  styleUrls: ['./add-organization.component.scss']
})
export class AddOrganizationComponent implements OnInit {

   model:any;
   addContact:boolean = false;
   contactDataSource: any = [];
   displayedColumns: string[] = ['name', 'title', 'email', 'phone'];
   contactError='';
   contacts:Array<Contact> = [];

   matchOrganizationName = new MyErrorStateMatcher();
   matchOrganizationIdentifier = new MyErrorStateMatcher();
   matchAddress1 = new MyErrorStateMatcher();
   matchCity = new MyErrorStateMatcher();
   matchState = new MyErrorStateMatcher();
   matchZip = new MyErrorStateMatcher();
   
   matchFirstName = new MyErrorStateMatcher();
   matchLastName = new MyErrorStateMatcher();
   matchEmail = new MyErrorStateMatcher();
   
   organizationId = new FormControl({value: '8b045ff5-b60d-4309-926c-a676b4028011', disabled: true});
   organizationName = new FormControl('', [Validators.required]);
   organizationIdentifier = new FormControl('', [Validators.required]);
   address1 = new FormControl('', [Validators.required]);
   address2 = new FormControl('');
   city = new FormControl('', [Validators.required]);
   state = new FormControl('', [Validators.required]);
   zip = new FormControl('', [Validators.required]);

   

   contactFormGroup = new FormGroup({
    firstName: new FormControl('', [Validators.required]),
    lastName: new FormControl('', [Validators.required]),
    title: new FormControl(''),
    email: new FormControl('', [Validators.required, Validators.email]),
    phone: new FormControl(''),
    contactNotes: new FormControl(''),
   });


  constructor( public subSvc: SubscriptionService) { }

  pushContact(){
    if(this.contactFormGroup.valid)
    {
      var contact: Contact = {
        id: null,
        phone: this.contactFormGroup.controls['phone'].value,
        email: this.contactFormGroup.controls['email'].value,
        firstName: this.contactFormGroup.controls['firstName'].value,
        lastName: this.contactFormGroup.controls['lastName'].value,
        title: this.contactFormGroup.controls['title'].value,
        contactNotes: this.contactFormGroup.controls['contactNotes'].value,
      };
      
      this.contacts.push(contact);
      this.clearContact();
    }
    else{
      this.contactError = "Fix required fields."
    }
  }

  clearContact(){
    this.contactFormGroup.setValue({
      firstName: '',
      lastName: '',
      title: '',
      email: '',
      phone: '',
      contactNotes: '',
    });
    this.contactFormGroup.controls['firstName'].setErrors(null);
    this.contactFormGroup.controls['lastName'].setErrors(null);
    this.contactFormGroup.controls['email'].setErrors(null);
    this.contactFormGroup.clearValidators();
    this.contactError = '';
  }

  showAddContact(){
    this.addContact = this.addContact ? false : true;
  }

  checkDataSourceLength(){
    return this.contacts.length > 0;
  }

  ngOnInit(): void {
    
  }
}