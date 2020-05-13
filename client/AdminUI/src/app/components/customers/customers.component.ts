import { Component, OnInit } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { CustomerService } from 'src/app/services/customer.service';
import { MatDialogConfig, MatDialog } from '@angular/material/dialog';
import { AddCustomerDialogComponent } from './add-customer-dialog/add-customer-dialog.component';

interface ICustomer {
  uuid: string;
  name: string;
  identifier: string;
  address_1: string;
  address_2: string;
  city: string;
  state: string;
  zip_code: string;
}

@Component({
  selector: 'app-customers',
  templateUrl: './customers.component.html',
  styleUrls: ['./customers.component.scss']
})
export class CustomersComponent implements OnInit {
  private data_source: MatTableDataSource<ICustomer>;
  displayed_columns = [
    "name",
    "identifier",
    "address_1",
    "address_2",
    "city",
    "state",
    "zip_code"
  ]

  constructor(
    private layout_service: LayoutMainService,
    public customer_service: CustomerService,
    public dialog: MatDialog
  ) { 
    layout_service.setTitle('Con-PCA Customers Page')
  }

  private refresh(): void {
    let customers: ICustomer[] = [];
    this.customer_service.getCustomers().subscribe((data: any[]) => {
      data.map((customer: any) => {
        customers.push({
          uuid: customer.customer_uuid,
          name: customer.name,
          identifier: customer.identifier,
          address_1: customer.address_1,
          address_2: customer.address_2,
          city: customer.city,
          state: customer.state,
          zip_code: customer.zip_code
        })
      })
      this.data_source.data = customers;
    }) 
  }

  private open_add_customer_dialog(): void {
    const dialog_config = new MatDialogConfig();
    dialog_config.data = {}
    const dialog_ref = this.dialog.open(AddCustomerDialogComponent, dialog_config);

    dialog_ref.afterClosed().subscribe(value => {
      this.refresh();
    })
  }

  ngOnInit(): void {
    this.data_source = new MatTableDataSource();
    this.refresh();
  }

}
