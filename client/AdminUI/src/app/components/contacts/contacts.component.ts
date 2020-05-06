import { Component, OnInit, Input } from '@angular/core';
import { LayoutMainService } from 'src/app/services/layout-main.service';

@Component({
  selector: '',
  templateUrl: './contacts.component.html',
  styleUrls: ['./contacts.component.scss'],
})

export class ContactsComponent implements OnInit {
  body_content_height: number;
  advancedSearch: boolean = false;

  displayedColumns = ["CompanyName",
    "FirstName",
    "LastName",
    "Position",
    "PrimaryContact",
    "PhoneNumber"];
  contactsData = [
    { "CompanyName": "Idaho National Labs", "FirstName": "  Barry", "LastName": " Hansen", "Position": "CEO", "PrimaryContact": " Yes", "PhoneNumber": "(208)222-2082", },
    { "CompanyName": "Idaho National Labs", "FirstName": "  Randy", "LastName": " Woods", "Position": "Developer", "PrimaryContact": " No", "PhoneNumber": "(208)222-2183", },
    { "CompanyName": "Idaho National Labs", "FirstName": "  McKenzie", "LastName": " Willmore", "Position": "Team Manager", "PrimaryContact": " Yes", "PhoneNumber": "(208)222-2544", },
    { "CompanyName": "Idaho National Labs", "FirstName": "  Jason", "LastName": " Kuipers", "Position": "Developer", "PrimaryContact": " No", "PhoneNumber": "(208)222-2923", },
    { "CompanyName": "Idaho National Labs", "FirstName": "  Bill", "LastName": " Martin", "Position": "Testing", "PrimaryContact": " No", "PhoneNumber": "(208)222-2070", },
    { "CompanyName": "Neetflix Streaming Services", "FirstName": "  John", "LastName": " Galetti", "Position": "CEO", "PrimaryContact": " No", "PhoneNumber": "(509)345-4455", },
    { "CompanyName": "Neetflix Streaming Services", "FirstName": "  David", "LastName": " Olsavsky", "Position": "CFO", "PrimaryContact": " No", "PhoneNumber": "(509)345-4455", },
    { "CompanyName": "Neetflix Streaming Services", "FirstName": "  Jeff", "LastName": " Wilke", "Position": "HR Lead", "PrimaryContact": " Yes", "PhoneNumber": "(509)745-3021", },
    { "CompanyName": "Plumbing & Pipes Co", "FirstName": "  Douglas", "LastName": " Brand", "Position": "Sales Manager", "PrimaryContact": " Yes", "PhoneNumber": "(208)735-7483", },
    { "CompanyName": "Plumbing & Pipes Co", "FirstName": "  Valerie", "LastName": " Anders", "Position": "CTO", "PrimaryContact": " Yes", "PhoneNumber": "(208)735-74783", },
    { "CompanyName": "Next Level Tech", "FirstName": "  Judith", "LastName": " Fulmer", "Position": "Company Rep", "PrimaryContact": " Yes", "PhoneNumber": "(877)503-2277", },
    { "CompanyName": "Next Level Tech", "FirstName": "  Sarah", "LastName": " Fulmer", "Position": "Company Rep", "PrimaryContact": " No", "PhoneNumber": "(877)503-2278", },
    { "CompanyName": "Next Level Tech", "FirstName": "  Kevin", "LastName": " Turner", "Position": "Security", "PrimaryContact": " No", "PhoneNumber": "(877)503-2279", },
    { "CompanyName": "Next Level Tech", "FirstName": "  Cody", "LastName": " Smith", "Position": "IT Manager", "PrimaryContact": " No", "PhoneNumber": "(877)503-2280", },
  ];

  constructor(private layoutSvc: LayoutMainService) {
    layoutSvc.setTitle('Con-PCA Contacts Page');
  }

  showAdvancedSearch() {
    this.advancedSearch = !(this.advancedSearch);
  }

  ngOnInit() {
  }

}