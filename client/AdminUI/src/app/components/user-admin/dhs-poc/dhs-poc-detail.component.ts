import { Component, OnInit, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Contact } from 'src/app/models/customer.model';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-dhs-poc-detail',
  templateUrl: './dhs-poc-detail.component.html'
})
export class DhsPocDetailComponent implements OnInit {

  /**
   * NEW or EDIT
   */
  mode = 'new';

  contactForm: FormGroup;
  submitted = false;
  contact: Contact;

  constructor(
    public dialogRef: MatDialogRef<DhsPocDetailComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    public subscriptionSvc: SubscriptionService
  ) {
    this.contact = data.contact;
  }

  /**
   * convenience getter for easy access to form fields
   */
  get f() {
    return this.contactForm.controls;
  }

  /**
   *
   */
  ngOnInit(): void {
    this.contactForm = new FormGroup({
      firstName: new FormControl('', Validators.required),
      lastName: new FormControl('', Validators.required)
    });

    if (!!this.contact.dhs_contact_uuid) {
      this.mode = 'edit';

      this.f.firstName.setValue(this.contact.first_name);
      this.f.lastName.setValue(this.contact.last_name);
    }
  }

  /**
   *
   */
  onSaveClick() {
    this.submitted = true;

    if (this.contactForm.invalid) {
      return;
    }

    const c = new Contact();
    c.first_name = this.f.firstName.value;
    c.last_name = this.f.lastName.value;

    this.subscriptionSvc.saveDhsContact(c).subscribe(() => {
      this.dialogRef.close();
    });
  }

  /**
   *
   */
  onCancelClick() {
    this.dialogRef.close();
  }
}
