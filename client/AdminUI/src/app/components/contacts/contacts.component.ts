import { Component, OnInit, Inject } from '@angular/core';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { FormGroup, FormControl } from '@angular/forms';
import { MatDialogRef, MatDialog, MatDialogConfig, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatTableDataSource } from '@angular/material/table';
import {CustomerService} from 'src/app/services/customer.service'
import { MatTab } from '@angular/material/tabs';

export interface ICustomerContact {
  customer_uuid: string;
  customer_name: string;
  first_name: string;
  last_name: string;
  title: string;
  phone: string;
  email: string;
  notes: string;
}

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


  // Filters search on key up in search bar
  searchFilter(searchValue: string): void {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  // Opens a dialog box for adding a contact
  openAddDialog(): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.data = {}
    const dialogRef = this.dialog.open(AddContactDialog, dialogConfig);

    dialogRef.afterClosed().subscribe(value => {
      this.refresh()
    })
  }

  // Opens a dialog box for viewing, editing and deleting a contact
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

  // Refreshes the data source view
  refresh(): void {
    this.dataSource.data = this.dataSource.data;
  }

  private setCustomerContactList() {
    this.customerService.getCustomers().subscribe((data: any[]) => {
      let customerContactList: ICustomerContact[] = []

      data.map((customer: any) => {
        customer.contact_list.map((contact: any) => {
          customerContactList.push({
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
      console.log(customerContactList);
      this.dataSource.data = customerContactList;
    })
  }

  // custom filter predicate to search list
  private setFilterPredicate() {
    this.dataSource.filterPredicate = (data: ICustomerContact, filter: string) => {
      var words = filter.split(' ');

      // Create search data once so it's not created each time in loop
      let searchData = `${data.first_name.toLowerCase()} ${data.last_name.toLowerCase()} ${data.customer_name.toLowerCase()} ${data.title.toLowerCase()}`

      for (var i = 0; i < words.length; i++) {

        // Don't want to compare bad input
        if (words[i] == null || words[i] == '' || words[i] == ' ') {
          continue;
        }

        // Check if search data contains the word
        var isMatch = searchData.indexOf(words[i].trim().toLowerCase()) > -1;
        
        // If there's no match for the word, return false
        if (!isMatch) {
          return false;
        }
      }
      
      // return true if false was never returned
      return true;
    };
  }

  ngOnInit() {
    this.dataSource = new MatTableDataSource();
    this.setCustomerContactList();
    this.setFilterPredicate();
  }
}

// =======================================
// ADD CONTACT DIALOG
// =======================================
@Component({
  selector: 'add-contact-dialog',
  templateUrl: 'dialogues/add-contact-dialog.html',
  styleUrls: ['./contacts.component.scss'],
})
export class AddContactDialog {
  data: ICustomerContact;
  isPrimary = false;
  addContactCustomer: string;
  addContactFirstName: string;
  addContactLastName: string;
  addContactTitle: string;
  addContactPrimary: string;
  addContactPhone: string;
  addContactEmail: string;
  addContactNotes: string;


  constructor(
    public dialogRef: MatDialogRef<AddContactDialog>,
  ) {}

  onNoClick(): void {
    this.dialogRef.close();
  }

  onSaveClick(): void {
    if (this.isPrimary == true) {
        this.addContactPrimary = "Yes"
    } else {
      this.addContactPrimary = "No"
    }

    customerContactList.push({
      customer_name: this.addContactCustomer, 
      customer_uuid: '',
      first_name: this.addContactFirstName,
      last_name: this.addContactLastName, 
      title: this.addContactTitle,
      phone: this.addContactPhone,
      email: this.addContactEmail, 
      notes: this.addContactNotes
    });
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
    customer: new FormControl(),
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
    @Inject(MAT_DIALOG_DATA) data) {
      this.data = data;
      this.initialData = Object.assign({}, data);
      this.contactFormGroup.disable();
    }

  onEditClick(): void {
    this.edit = true;
    this.contactFormGroup.enable();
  }

  onSaveEditClick(): void {
    this.edit = false;
    this.contactFormGroup.disable();
  }

  onCancelEditClick(): void {
    this.contactFormGroup.patchValue(this.initialData);
    console.log(this.data);
  }

  onDeleteClick(): void {
    const index = customerContactList.indexOf(this.data, 0);
    console.log(index)
    if (index > -1) {
      customerContactList.splice(index, 1);
    }
    this.dialogRef.close();
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  get diagnostic() {return JSON.stringify(this.data)}
}