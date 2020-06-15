import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-customer-dialog',
  templateUrl: './customer-dialog.component.html'
})
export class CustomerDialogComponent implements OnInit {

  constructor(
    public dialogRef: MatDialogRef<CustomerDialogComponent>
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
