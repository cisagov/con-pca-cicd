import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { CustomersComponent } from '../../customers/customers.component';
import { CustomerService } from 'src/app/services/customer.service';

@Component({
  selector: 'app-customer-dialog',
  templateUrl: './customer-dialog.component.html'
})
export class CustomerDialogComponent implements OnInit {

  showButtons = true;

  constructor(
    public dialogRef: MatDialogRef<CustomerDialogComponent>,
    public customerSvc: CustomerService
  ) { }

  ngOnInit(): void {
  }

  /**
   *
   */
  onCancelClick() {
    this.dialogRef.close();
  }
}
