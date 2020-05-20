import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatDialogConfig, MatDialog } from '@angular/material/dialog';
import { FormGroup, FormControl } from '@angular/forms';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { Router, ActivatedRoute } from '@angular/router';
import { Customer, Contact } from 'src/app/models/customer.model';
import { Subscription } from 'src/app/models/subscription.model';
import { Guid } from 'guid-typescript';
import { UserService } from 'src/app/services/user.service';
import { CustomerService } from 'src/app/services/customer.service';
import { CustomersComponent } from 'src/app/components/customers/customers.component';
import { XlsxToCsv } from 'src/app/helper/XlsxToCsv';
import { StringifyOptions } from 'querystring';

@Component({
  selector: 'app-manage-subscription',
  templateUrl: './manage-subscription.component.html'
})
export class ManageSubscriptionComponent implements OnInit, OnDestroy {
  private routeSub: any;


  action_MANAGE: string = 'manage';
  action_CREATE: string = 'create';
  action: string = this.action_MANAGE;

  // CREATE or MANAGE (edit existing)
  pageMode: string = 'CREATE';

  subscription: Subscription;
  customer: Customer = new Customer();
  primaryContact: Contact = new Contact();

  startDate: Date = new Date();
  startAt = new Date();

  url: string;
  tags: string;

  // The raw CSV content of the textarea
  csvText: string;

  /**
   * 
   */
  constructor(
    public subscriptionSvc: SubscriptionService,
    public customerSvc: CustomerService,
    private router: Router,
    private route: ActivatedRoute,
    private userSvc: UserService,
    public dialog: MatDialog
  ) {

  }

  /**
   * INIT
   */
  ngOnInit(): void {
    this.pageMode = 'MANAGE';

    this.subscriptionSvc.subscription = new Subscription();
    let sub = this.subscriptionSvc.subscription;

    this.routeSub = this.route.params.subscribe(params => {
      if (!params.id) {
        this.pageMode = 'CREATE';
        this.action = this.action_CREATE;
        sub = new Subscription();
        this.subscription = sub;
        sub.subscription_uuid = Guid.create().toString();

        // START TEMP ------------------------
        // find Globex or randomly pick an existing customer for now
        if (!this.subscription.customer_uuid) {
          this.customerSvc.requestGetCustomers().subscribe((c: Customer[]) => {

            // first look for Globex
            let globex = c.find(x => x.identifier == 'GLBX');
            if (globex == null) {

              // if not found, just pick a random customer
              let rnd = Math.floor(Math.random() * Math.floor(c.length));
              this.customer = c[rnd];
            } else {
              this.customer = globex;
            }
          });
        }
        // END TEMP --------------------------

      } else {
        sub.subscription_uuid = params.id;

        this.subscriptionSvc.getSubscription(sub.subscription_uuid)
          .subscribe((s: Subscription) => {
            this.subscription = s;
          });
      }
    });
  }


  /**
   * 
   * @param customer_uuid 
   */
  loadContactsForCustomer(customer_uuid: string) {
    // get the customer and contacts from the API
    this.customerSvc.requestGetCustomer(customer_uuid).subscribe((c: Customer) => {
      this.customer = c;

      this.customer.contact_list = this.customerSvc.getContactsForCustomer(c);
      this.primaryContact = this.customer.contact_list[0];
    });
  }

  /**
   * Presents a customer page to select or create a new customer for 
   * this subscription.
   */
  public showCustomerDialog(): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.height = "80vh";
    dialogConfig.width = "80vw";
    dialogConfig.data = {};
    const dialogRef = this.dialog.open(CustomersComponent, dialogConfig);

    dialogRef.afterClosed().subscribe(value => {
      // TODO:  set the subscription's customer here so that
      // the binding will reflect the change in the page
    })
  }

  /**
   * 
   */
  changePrimaryContact(e: any) {
    if (!this.customer) {
      return;
    }
    this.primaryContact = this.customer.contact_list
      .find(x => (x.first_name + '_' + x.last_name) == e.value);
    this.subscription.primary_contact = this.primaryContact;
    this.subscriptionSvc.subscription.primary_contact = this.primaryContact;
  }

  /**
   * Programatically clicks the corresponding file upload element.
   * @param event
   */
  openFileBrowser(event: any) {
    event.preventDefault();
    const element: HTMLElement = document.getElementById('csvUpload') as HTMLElement;
    element.click();
  }

  /**
   * Reads the contents of the event's file and puts them into csvText.
   * @param e The 'file' event
   */
  fileSelect(e: any) {
    let file: any = e.target.files[0];

    let x = new XlsxToCsv();
    x.convert(file).then((xyz: string) => {
      this.csvText = xyz;
    });

  }

  /**
   * 
   */
  createAndLaunchSubscription() {
    console.log('createAndLaunchSubscription');

    let sub = this.subscriptionSvc.subscription;

    // set up the subscription and persist it in the service
    sub = new Subscription();

    sub.customer_uuid = this.customer.customer_uuid;
    sub.primary_contact = this.primaryContact;

    sub.active = true;

    sub.lub_timestamp = new Date();
    sub.name = "SC-1." + this.customer.name + ".1.1"; //auto generated name
    sub.start_date = this.startDate;
    sub.status = "New Not Started";
    // set the target list
    sub.setTargetsFromCSV(this.csvText);
    sub.url = this.url;
    // tags / keywords
    sub.keywords = this.tags;


    // call service with everything needed to start the subscription
    this.subscriptionSvc.submitSubscription(sub).subscribe(
      resp => {
        alert("Your subscription was created as " + sub.name);
        this.router.navigate(['subscriptions']);
      },
      error => {
        console.log(error);
        alert("An error occurred submitting the subscription: " + error.error);
      });
  }

  /**
   * 
   * @param date 
   * @param days 
   */
  addDays(date, days) {
    var result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  }

  /**
   * 
   */
  ngOnDestroy() {
    this.routeSub.unsubscribe();
  }
}
