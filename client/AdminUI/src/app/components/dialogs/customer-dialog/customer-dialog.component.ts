import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { CustomersComponent } from '../../customers/customers.component';

@Component({
  selector: 'app-customer-dialog',
  templateUrl: './customer-dialog.component.html'
})
export class CustomerDialogComponent implements OnInit {

  showButtons = true;

  constructor(
    public dialogRef: MatDialogRef<CustomerDialogComponent>
  ) { }

  ngOnInit(): void {
  }


  /**
   * Hide my buttons because I am hosting an embedded component with buttons.
   */
  hideButtons() {
    this.showButtons = false;
  }

  /**
   *
   */
  onCancelClick() {
    this.dialogRef.close();
  }
}
