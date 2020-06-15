import { Component, OnInit, ViewChild } from '@angular/core';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { Subscription } from 'src/app/models/subscription.model';
import { MatTableDataSource } from '@angular/material/table';
import { Customer } from 'src/app/models/customer.model';
import { CustomerService } from 'src/app/services/customer.service';
import { AppSettings } from 'src/app/AppSettings';
import {
  MatDialog,
  MatDialogConfig,
  MatDialogRef
} from '@angular/material/dialog';
import { ConfirmComponent } from '../dialogs/confirm/confirm.component';

interface ICustomerSubscription {
  customer: Customer;
  subscription: Subscription;
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './subscriptions.component.html',
  styleUrls: ['./subscriptions.component.scss']
})
export class SubscriptionsComponent implements OnInit {
  public data_source: MatTableDataSource<ICustomerSubscription>;

  displayed_columns = [
    'name',
    'status',
    'primary_contact',
    'customer',
    'start_date',
    'last_updated',
    'select'
  ];
  dialogRefConfirm: MatDialogRef<ConfirmComponent>;
  showArchived: boolean = false;

  dateFormat = AppSettings.DATE_FORMAT;

  constructor(
    private subscription_service: SubscriptionService,
    private customer_service: CustomerService,
    private layoutSvc: LayoutMainService,
    public dialog: MatDialog
  ) {
    layoutSvc.setTitle('Subscriptions');
  }

  ngOnInit(): void {
    this.layoutSvc.setTitle('Subscriptions');
    this.data_source = new MatTableDataSource();
    this.refresh();
    this.setFilterPredicate();
  }

  refresh() {
    this.subscription_service
      .getSubscriptions(this.showArchived)
      .subscribe((data: any[]) => {
        let subscriptions = data as Subscription[];
        this.customer_service.getCustomers().subscribe((data: any[]) => {
          let customers = data as Customer[];
          let customerSubscriptions: ICustomerSubscription[] = [];
          subscriptions.map((s: Subscription) => {
            let customerSubscription: ICustomerSubscription = {
              customer: customers.find(o => o.customer_uuid == s.customer_uuid),
              subscription: s
            };
            customerSubscriptions.push(customerSubscription);
          });
          this.data_source.data = customerSubscriptions;
        });
      });
  }

  private setFilterPredicate() {
    this.data_source.filterPredicate = (
      data: ICustomerSubscription,
      filter: string
    ) => {
      var words = filter.split(' ');
      let searchData = `${data.subscription.name.toLowerCase()} ${data.subscription.status.toLowerCase()} ${data.customer.name.toLowerCase()} ${data.subscription.primary_contact.first_name.toLowerCase()} ${data.subscription.primary_contact.last_name.toLowerCase()}`;
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

  public searchFilter(searchValue: string): void {
    const filterValue = (event.target as HTMLInputElement).value;
    this.data_source.filter = filterValue.trim().toLowerCase();
  }

  public onArchiveToggle(): void {
    if (this.displayed_columns.includes('archived')) {
      this.displayed_columns.splice(this.displayed_columns.length - 2, 1);
    } else {
      this.displayed_columns.splice(
        this.displayed_columns.length - 1,
        0,
        'archived'
      );
    }
    this.refresh();
  }

  public stopSubscription(row: any) {
    this.dialogRefConfirm = this.dialog.open(ConfirmComponent, {
      disableClose: false
    });
    this.dialogRefConfirm.componentInstance.confirmMessage = `This will stop subscription '${row.subscription.name}'.  Do you want to continue?`;
    this.dialogRefConfirm.componentInstance.title = 'Confirm Delete';

    this.dialogRefConfirm.afterClosed().subscribe(result => {
      if (result) {
        this.subscription_service
          .stopSubscription(row.subscription.subscription_uuid)
          .subscribe((data: any) => {
            this.refresh();
          });

        //this.deleteProfile(row);
      }
      this.dialogRefConfirm = null;
    });
  }
}
