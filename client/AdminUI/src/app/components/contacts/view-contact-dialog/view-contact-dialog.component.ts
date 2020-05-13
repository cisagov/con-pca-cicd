import { Component, OnInit, Inject } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { CustomerService } from 'src/app/services/customer.service';
import { ICustomerContact, Customer, Contact } from 'src/app/models/customer.model';

@Component({
  selector: 'app-view-contact-dialog',
  templateUrl: './view-contact-dialog.component.html',
  styleUrls: ['../contacts.component.scss']
})
export class ViewContactDialogComponent implements OnInit {
  form_group = new FormGroup({
    first_name: new FormControl(),
    last_name: new FormControl(),
    title: new FormControl(),
    primary_contact: new FormControl(),
    phone: new FormControl(),
    email: new FormControl(),
    notes: new FormControl(),
  })

  customer: Customer
  initial: ICustomerContact
  data: ICustomerContact

  constructor(
    public dialog_ref: MatDialogRef<ViewContactDialogComponent>,
    public customer_service: CustomerService,
    @Inject(MAT_DIALOG_DATA) data) {
      this.data = data;
      this.initial = Object.assign({}, data);
  }

  ngOnInit(): void {
    this.customer_service.requestGetCustomer(this.data.customer_uuid).subscribe((data: any) => {
      this.customer = this.customer_service.getCustomer(data)
    })
  }

  onSaveExitClick(): void {
    this.saveContacts()
    this.dialog_ref.close()
  }

  onDeleteClick(): void {
    const index = customerContacts.indexOf(this.data, 0);
    if (index > -1) {
      customerContacts.splice(index, 1);
    }
    this.saveContacts();
    this.dialogRef.close();
  }

  onCancelExitClick(): void {
    this.dialog_ref.close()
  }

  saveContacts(): void {

  }

  getContactIndex(): number {
    for (var i = 0; i < this.customer.contact_list.length; i++) {
      var contact: Contact = this.customer.contact_list[i]
      if(
        contact.first_name == this.initial.first_name &&
        contact.last_name == this.initial.last_name &&
        contact.email == this.initial.email &&
        contact.notes == this.initial.notes &&
        contact.title == this.initial.title) {
          return i
        }
    }
  }
}

// export class ViewContactDialog {

//   onDeleteClick(): void {
//     const index = customerContacts.indexOf(this.data, 0);
//     if (index > -1) {
//       customerContacts.splice(index, 1);
//     }
//     this.saveContacts();
//     this.dialogRef.close();
//   }

//   private saveContacts(): void {
//     let uuid = this.data.customer_uuid
//     let contacts: Contact[] = [];
//     customerContacts.map(val => {
//       if (val.customer_uuid == uuid) {
//         let c: Contact = {
//           first_name: val.first_name,
//           last_name: val.last_name,
//           title: val.title,
//           phone: val.phone,
//           email: val.email,
//           notes: val.notes
//         }
//         contacts.push(c);
//       }
//     })

//     this.customerService.setContacts(
//       uuid,
//       contacts
//     ).subscribe()
//   }
// }