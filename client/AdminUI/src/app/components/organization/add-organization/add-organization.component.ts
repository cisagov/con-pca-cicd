import { Component, OnInit } from '@angular/core';
import { FormControl, NgForm, FormGroupDirective, Validators, FormGroup } from '@angular/forms';
import { MyErrorStateMatcher } from '../../../helper/ErrorStateMatcher';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { Contact, Organization } from 'src/app/models/organization.model';
import { Guid } from 'guid-typescript';

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
   orgError='';
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
   
   organizationFormGroup = new FormGroup({
    organizationId: new FormControl({value: '', disabled: true}),
    organizationName: new FormControl('', [Validators.required]),
    organizationIdentifier: new FormControl('', [Validators.required]),
    address1: new FormControl('', [Validators.required]),
    address2: new FormControl(''),
    city: new FormControl('', [Validators.required]),
    state: new FormControl('', [Validators.required]),
    zip: new FormControl('', [Validators.required]),
   });

   contactFormGroup = new FormGroup({
    firstName: new FormControl('', [Validators.required]),
    lastName: new FormControl('', [Validators.required]),
    title: new FormControl(''),
    email: new FormControl('', [Validators.required, Validators.email]),
    phone: new FormControl(''),
    contactNotes: new FormControl(''),
   });


  constructor( public subscriptionSvc: SubscriptionService) { 
    this.organizationFormGroup.controls["organizationId"].setValue(Guid.create());
  }

  createNew(){
    this.clearOrganization();
  }

  pushOrganization(){
    if(this.organizationFormGroup.valid && this.contacts.length > 0)
    {
      var organization: Organization = {
        id: this.organizationFormGroup.controls["organizationId"].value,
        orgName: this.organizationFormGroup.controls["organizationName"].value,
        orgAbbrev: this.organizationFormGroup.controls["organizationIdentifier"].value,
        orgAddress1: this.organizationFormGroup.controls["address1"].value,
        orgAddress2: this.organizationFormGroup.controls["address2"].value,
        orgCity: this.organizationFormGroup.controls["city"].value,
        orgState: this.organizationFormGroup.controls["state"].value,
        orgZip: this.organizationFormGroup.controls["zip"].value,
        orgType: "",
        contacts: this.contacts
      }

      this.subscriptionSvc.postOrganization(organization).subscribe((o:Organization) => {
        this.clearOrganization();
      });
    } else if( !this.organizationFormGroup.valid )
    {
      this.orgError = "Fix required fields";
    } else if( this.contacts.length < 1){
      this.orgError = "Please add at least one contact";
    }
  }

  pushContact(){
    if(this.contactFormGroup.valid)
    {
      var contact: Contact = {
        id: Guid.create().toString(),
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

  clearOrganization(){

    this.organizationFormGroup.reset();
    this.organizationFormGroup.controls["organizationId"].setValue(Guid.create());
    this.contacts = [];
    this.orgError = '';
  }

  clearContact(){
    this.contactFormGroup.reset();
    this.contactError = '';
    this.contactFormGroup.markAsUntouched();
  }

  showAddContact(){
    this.addContact = this.addContact ? false : true;
    if(!this.addContact)
    {
      this.clearContact();
    }
  }

  checkDataSourceLength(){
    return this.contacts.length > 0;
  }

  ngOnInit(): void {
    
  }
}