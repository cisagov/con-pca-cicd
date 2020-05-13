import { Component, OnInit, Inject } from '@angular/core';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { FormGroup, FormControl } from '@angular/forms';
import { MatDialogRef, MatDialog, MatDialogConfig, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatTableDataSource } from '@angular/material/table';
import {CustomerService} from 'src/app/services/customer.service'
import { MatTab } from '@angular/material/tabs'; 
import { Contact, Customer } from 'src/app/models/customer.model';

interface ICustomerContact {
  customer_uuid: string;
  customer_name: string;
  first_name: string;
  last_name: string;
  title: string;
  phone: string;
  email: string;
  notes: string;
}

interface ICustomer {
  customer_uuid: string;
  customer_name: string;
}

let customerContacts: ICustomerContact[] = []
let distinctCustomers: ICustomer[] = []

// =======================================
// MAIN CONTACTS PAGE
// =======================================
@Component({
  selector: '',
  templateUrl: './contacts.component.html',
  styleUrls: ['./contacts.component.scss'],
})
export class ContactsComponent implements OnInit {
  dataSource: MatTableDataSource<ICustomerContact>;
  displayedColumns = [
    "customer_name",
    "first_name",
    "last_name",
    "title",
    "select"
  ];

  constructor(
    private layoutSvc: LayoutMainService, 
    public dialog: MatDialog,
    public customerService: CustomerService) {
    layoutSvc.setTitle('Con-PCA Contacts Page');
  }

  searchFilter(searchValue: string): void {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  openAddDialog(): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.data = {}
    const dialogRef = this.dialog.open(AddContactDialog, dialogConfig);

    dialogRef.afterClosed().subscribe(value => {
      this.refresh()
    })
  }

  openViewDialog(row: ICustomerContact): void {
    const dialogRef = this.dialog.open(
      ViewContactDialog, {
        data: row
      }
    );
    dialogRef.afterClosed().subscribe(value => {
      this.refresh()
    })
  }

  private refresh(): void {
    this.customerService.getCustomers().subscribe((data: any[]) => {
      distinctCustomers = []
      customerContacts = []

      data.map((customer: any) => {
        distinctCustomers.push({
          customer_name: customer.name,
          customer_uuid: customer.customer_uuid
        })
        customer.contact_list.map((contact: any) => {
          customerContacts.push({
            customer_uuid: customer.customer_uuid,
            customer_name: customer.name,
            first_name: contact.first_name,
            last_name: contact.last_name,
            title: contact.title,
            phone: contact.phone,
            email: contact.email,
            notes: contact.notes,
          })
        })
      })
      this.dataSource.data = customerContacts;
    })
  }

  private setFilterPredicate() {
    this.dataSource.filterPredicate = (data: ICustomerContact, filter: string) => {
      var words = filter.split(' ');
      let searchData = `${data.first_name.toLowerCase()} ${data.last_name.toLowerCase()} ${data.customer_name.toLowerCase()} ${data.title.toLowerCase()}`
      for (var i = 0; i < words.length; i++) {
        if (words[i] == null || words[i] == '' || words[i] == ' ') {
          continue;
        }
        var isMatch = searchData.indexOf(words[i].trim().toLowerCase()) > -1;
        
        if (!isMatch) {
          return false;
        }
      }
      return true;
    };
  }

  ngOnInit() {
    this.dataSource = new MatTableDataSource();
    this.refresh();
    this.setFilterPredicate();
  }
}

@Component({
  selector: 'add-contact-dialog',
  templateUrl: 'dialogues/add-contact-dialog.html',
  styleUrls: ['./contacts.component.scss'],
})
export class AddContactDialog {
  addContactFormGroup = new FormGroup({
    customer_uuid: new FormControl(),
    first_name: new FormControl(),
    last_name: new FormControl(),
    title: new FormControl(),
    phone: new FormControl(),
    email: new FormControl(),
    notes: new FormControl()
  })

  customers: ICustomer[] = [  ]


  constructor(
    public dialogRef: MatDialogRef<AddContactDialog>,
    public customerService: CustomerService) { 
    this.customers = distinctCustomers;
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  onSaveClick(): void {
    let uuid = this.addContactFormGroup.controls['customer_uuid'].value
    let contacts: Contact[] = [];
    customerContacts.map(val => {
      if (val.customer_uuid == uuid) {
        let c: Contact = {
          first_name: val.first_name,
          last_name: val.last_name,
          title: val.title,
          phone: val.phone,
          email: val.email,
          notes: val.notes
        }
        contacts.push(c);
      }
    })

    let contact: Contact = {
      first_name: this.addContactFormGroup.controls['first_name'].value,
      last_name: this.addContactFormGroup.controls['last_name'].value,
      title: this.addContactFormGroup.controls['title'].value,
      phone: this.addContactFormGroup.controls['phone'].value,
      email: this.addContactFormGroup.controls['email'].value,
      notes: this.addContactFormGroup.controls['notes'].value
    }
    contacts.push(contact)

    this.customerService.setContacts(
      uuid,
      contacts
    ).subscribe()

    this.dialogRef.close();
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }
}


// =======================================
// VIEW CONTACT DIALOG
// =======================================
@Component({
  selector: 'view-contact-dialog',
  templateUrl: 'dialogues/view-contact-dialog.html',
  styleUrls: ['./contacts.component.scss'],
})
export class ViewContactDialog {
  data: ICustomerContact;
  edit: boolean = false;

  contactFormGroup = new FormGroup({
    first_name: new FormControl(),
    last_name: new FormControl(),
    title: new FormControl(),
    primary_contact: new FormControl(),
    phone: new FormControl(),
    email: new FormControl(),
    notes: new FormControl(),
  })

  initialData: ICustomerContact;

  constructor(
    public dialogRef: MatDialogRef<ViewContactDialog>,
    public customerService: CustomerService,
    @Inject(MAT_DIALOG_DATA) data) {
      this.data = data;
      this.initialData = Object.assign({}, data);
    }

  onSaveExitClick(): void {
    this.saveContacts();
    this.dialogRef.close();
  }

  onCancelExitClick(): void {
    this.dialogRef.close();
  }

  onDeleteClick(): void {
    const index = customerContacts.indexOf(this.data, 0);
    if (index > -1) {
      customerContacts.splice(index, 1);
    }
    this.saveContacts();
    this.dialogRef.close();
  }

  private saveContacts(): void {
    let uuid = this.data.customer_uuid
    let contacts: Contact[] = [];
    customerContacts.map(val => {
      if (val.customer_uuid == uuid) {
        let c: Contact = {
          first_name: val.first_name,
          last_name: val.last_name,
          title: val.title,
          phone: val.phone,
          email: val.email,
          notes: val.notes
        }
        contacts.push(c);
      }
    })

    this.customerService.setContacts(
      uuid,
      contacts
    ).subscribe()
  }
}