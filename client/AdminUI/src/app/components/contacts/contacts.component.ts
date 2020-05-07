import { Component, OnInit } from '@angular/core';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { FormGroup, FormControl } from '@angular/forms';
import { MatDialogRef, MatDialog } from '@angular/material/dialog';
import { MatTableDataSource } from '@angular/material/table';

export interface ContactsInfo {
  CompanyName: string;
  FirstName: string;
  LastName: string;
  Position: string;
  PrimaryContact: string;
  PhoneNumber: string;
}

const contactsData: ContactsInfo[] = [
  { CompanyName: "Idaho National Labs", FirstName: " Barry", LastName: "Hansen", Position: "CEO", PrimaryContact: "Yes", PhoneNumber: "(208)222-2000"},
  { CompanyName: "Idaho National Labs", FirstName: "  Randy", LastName: " Woods", Position: "Developer", PrimaryContact: "No", PhoneNumber: "(208)222-2183", },
  { CompanyName: "Idaho National Labs", FirstName: "  McKenzie", LastName: " Willmore", Position: "Team Manager", PrimaryContact: "Yes", PhoneNumber: "(208)222-2544", },
  { CompanyName: "Idaho National Labs", FirstName: "  Jason", LastName: " Kuipers", Position: "Developer", PrimaryContact: "No", PhoneNumber: "(208)222-2923", },
  { CompanyName: "Idaho National Labs", FirstName: "  Bill", LastName: " Martin", Position: "Testing", PrimaryContact: "No", PhoneNumber: "(208)222-2070", },
  { CompanyName: "Neetflix Streaming Services", FirstName: "  John", LastName: " Galetti", Position: "CEO", PrimaryContact: "No", PhoneNumber: "(509)345-4455", },
  { CompanyName: "Neetflix Streaming Services", FirstName: "  David", LastName: " Olsavsky", Position: "CFO", PrimaryContact: "No", PhoneNumber: "(509)345-4455", },
  { CompanyName: "Neetflix Streaming Services", FirstName: "  Jeff", LastName: " Wilke", Position: "HR Lead", PrimaryContact: "Yes", PhoneNumber: "(509)745-3021", },
  { CompanyName: "Plumbing & Pipes Co", FirstName: "  Douglas", LastName: " Brand", Position: "Sales Manager", PrimaryContact: "Yes", PhoneNumber: "(208)735-7483", },
  { CompanyName: "Plumbing & Pipes Co", FirstName: "  Valerie", LastName: " Anders", Position: "CTO", PrimaryContact: "Yes", PhoneNumber: "(208)735-74783", },
  { CompanyName: "Next Level Tech", FirstName: "  Judith", LastName: " Fulmer", Position: "Company Rep", PrimaryContact: "Yes", PhoneNumber: "(877)503-2277", },
  { CompanyName: "Next Level Tech", FirstName: "  Sarah", LastName: " Fulmer", Position: "Company Rep", PrimaryContact: "No", PhoneNumber: "(877)503-2278", },
  { CompanyName: "Next Level Tech", FirstName: "  Kevin", LastName: " Turner", Position: "Security", PrimaryContact: "No", PhoneNumber: "(877)503-2279", },
  { CompanyName: "Next Level Tech", FirstName: "  Cody", LastName: " Smith", Position: "IT Manager", PrimaryContact: "No", PhoneNumber: "(877)503-2280", },
];

@Component({
  selector: '',
  templateUrl: './contacts.component.html',
  styleUrls: ['./contacts.component.scss'],
})
export class ContactsComponent implements OnInit {
  body_content_height: number;
  dataSource = new MatTableDataSource(contactsData)

  advancedFormGroup = new FormGroup({
    firstName: new FormControl(),
    lastName: new FormControl(),
    company: new FormControl(),
    position: new FormControl(),
    phoneNumber: new FormControl(),
    primaryContacts: new FormControl(),
    exactMatches: new FormControl(),
    startDate: new FormControl(),
    endDate: new FormControl()
  })

  displayedColumns = ["CompanyName",
    "FirstName",
    "LastName",
    "Position",
    "PrimaryContact",
    "Action"];

  constructor(
    private layoutSvc: LayoutMainService, public dialog: MatDialog) {
    layoutSvc.setTitle('Con-PCA Contacts Page');
  }

  searchFilter = (searchValue: string) => {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  openDeleteDialog(): void {
    const dialogRef = this.dialog.open(
      DeleteContactDialog
    );
  }

  openAddDialog(): void {
    const dialogRef = this.dialog.open(
      AddContactDialog
    );
  }

  openUpdateDialog(): void {
    const dialogRef = this.dialog.open(
      UpdateContactDialog
    );
  }

  openViewDialog(): void {
    const dialogRef = this.dialog.open(
      ViewContactDialog
    );
  }

  ngOnInit() {
  }

}

@Component({
  selector: 'delete-contact-dialog',
  templateUrl: 'dialogues/delete-contact-dialog.html'
})
export class DeleteContactDialog {
  constructor(
    public dialogRef: MatDialogRef<DeleteContactDialog>
  ) {}

  onNoClick(): void {
    this.dialogRef.close();
  }
}

@Component({
  selector: 'add-contact-dialog',
  templateUrl: 'dialogues/add-contact-dialog.html'
})
export class AddContactDialog {
  constructor(
    public dialogRef: MatDialogRef<AddContactDialog>
  ) {}

  onNoClick(): void {
    this.dialogRef.close();
  }
}

@Component({
  selector: 'view-contact-dialog',
  templateUrl: 'dialogues/view-contact-dialog.html'
})
export class ViewContactDialog {
  constructor(
    public dialogRef: MatDialogRef<ViewContactDialog>
  ) {}

  onNoClick(): void {
    this.dialogRef.close();
  }
}

@Component({
  selector: 'update-contact-dialog',
  templateUrl: 'dialogues/update-contact-dialog.html'
})
export class UpdateContactDialog {
  constructor(
    public dialogRef: MatDialogRef<UpdateContactDialog>
  ) {}

  onNoClick(): void {
    this.dialogRef.close();
  }
}