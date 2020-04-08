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
   contactDataSource: any = [];
   displayedColumns: string[] = ['name', 'title', 'email', 'phone'];

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

   firstName = new FormControl('', [Validators.required]);
   lastName = new FormControl('', [Validators.required]);
   title = new FormControl('');
   email = new FormControl('', [Validators.required, Validators.email]);
   officePhone = new FormControl('');
   mobilePhone = new FormControl('');
   contactNotes = new FormControl('');


  constructor() { }

  showAddContact(){
    this.addContact = this.addContact ? false : true;
  }

  checkDataSourceLength(){
    return this.contactDataSource.length > 0;
  }

  ngOnInit(): void {
    
  }
}