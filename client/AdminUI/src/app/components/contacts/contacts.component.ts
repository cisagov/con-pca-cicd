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
  { CompanyName: "Idaho National Labs", FirstName: " Jason", LastName: "Bourne", Position: "Janitor", PrimaryContact: "Yes", PhoneNumber: "(208)222-2000"},
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

  openAddDialog(): void {
    const dialogRef = this.dialog.open(
      AddContactDialog
    );
  }

  openViewDialog(): void {
    const dialogRef = this.dialog.open(
      ViewContactDialog
    );
  }

  ngOnInit() {

    // New predicate for filtering.
    // The default predicate will only compare words against a single column.
    // Ex. if you search "Barry Hansen" no results would return because there are two columns...
    // One for firstname and one for last name.
    // This new predicate will search each word against all columns, if a word doesn't match anywhere...
    // no results will be returned.
    this.dataSource.filterPredicate = (data: ContactsInfo, filter: string) => {
      var words = filter.split(' ');

      // Create search data once so it's not created each time in loop
      let searchData = `${data.FirstName.toLowerCase()} ${data.LastName.toLowerCase()} ${data.CompanyName.toLowerCase()} ${data.Position.toLowerCase()}`

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