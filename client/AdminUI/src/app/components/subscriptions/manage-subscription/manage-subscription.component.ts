import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatDialogConfig, MatDialog } from '@angular/material/dialog';
import { FormGroup, FormControl, FormBuilder, Validators } from '@angular/forms';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { Router, ActivatedRoute } from '@angular/router';
import { Customer, Contact } from 'src/app/models/customer.model';
import { Subscription, Target, GoPhishCampaignModel, TimelineItem } from 'src/app/models/subscription.model';
import { Guid } from 'guid-typescript';
import { UserService } from 'src/app/services/user.service';
import { CustomerService } from 'src/app/services/customer.service';
import { CustomersComponent } from 'src/app/components/customers/customers.component';
import { XlsxToCsv } from 'src/app/helper/XlsxToCsv';
import { ArchiveSubscriptionDialogComponent } from '../archive-subscription-dialog/archive-subscription-dialog.component';
import * as moment from 'node_modules/moment/moment';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { CustomerDialogComponent } from '../../dialogs/customer-dialog/customer-dialog.component';
import { AlertComponent } from '../../dialogs/alert/alert.component';
import { isSameDate } from 'src/app/helper/utilities';


@Component({
  selector: 'app-manage-subscription',
  templateUrl: './manage-subscription.component.html',
  styleUrls: ['./manage-subscription.component.scss']
})
export class ManageSubscriptionComponent implements OnInit, OnDestroy {
  private routeSub: any;

  subscribeForm: FormGroup;
  submitted = false;


  actionEDIT = 'edit';
  actionCREATE = 'create';
  action: string = this.actionEDIT;

  // CREATE or EDIT
  pageMode = 'CREATE';

  subscription: Subscription;
  customer: Customer = new Customer();
  primaryContact: Contact = new Contact();
  dhsContacts = [];
  dhsContact: string;

  startDate: Date = new Date();
  startAt = new Date();

  url: string;
  keywords: string;

  // The raw CSV content of the textarea
  csvText: string;

  timelineItems: any[] = [];


  /**
   *
   */
  constructor(
    public subscriptionSvc: SubscriptionService,
    public customerSvc: CustomerService,
    private router: Router,
    private route: ActivatedRoute,
    private userSvc: UserService,
    public dialog: MatDialog,
    public formBuilder: FormBuilder,
    public layoutSvc: LayoutMainService
  ) {
    layoutSvc.setTitle('Subscription');
    this.getDhsContacts();
  }

  /**
   * INIT
   */
  ngOnInit(): void {

    // build form
    this.subscribeForm = new FormGroup({
      selectedCustomerUuid: new FormControl('', Validators.required),
      primaryContact: new FormControl(null, Validators.required),
      dhsContact: new FormControl(null, Validators.required),
      startDate: new FormControl(new Date()),
      url: new FormControl(''),
      keywords: new FormControl(''),
      csvText: new FormControl('', Validators.required)
    });


    this.pageMode = 'EDIT';

    this.subscriptionSvc.subscription = new Subscription();

    this.routeSub = this.route.params.subscribe(params => {
      if (!params.id) {
        this.loadPageForCreate(params);
      } else {
        this.loadPageForEdit(params);
      }
    });
  }

  /**
   * convenience getter for easy access to form fields
   */
  get f() { return this.subscribeForm.controls; }


  /**
   * CREATE mode
   */
  loadPageForCreate(params: any) {
    this.pageMode = 'CREATE';
    this.action = this.actionCREATE;
    let sub = this.subscriptionSvc.subscription;
    sub = new Subscription();
    this.subscription = sub;
    sub.subscription_uuid = Guid.create().toString();
  }

  /**
   *
   */
  setCustomer() {
    if (this.customerSvc.selectedCustomer.length > 0) {
      this.subscribeForm.patchValue({
        selectedCustomerUuid: this.customerSvc.selectedCustomer
      });
      this.customerSvc.getCustomer(this.customerSvc.selectedCustomer).subscribe(
        (data: Customer) => {
          this.customer = data;
          this.f.selectedCustomerUuid.setValue(this.customer.customer_uuid);
        }
      );
    }
  }

  getDhsContacts() {
    this.subscriptionSvc.getDhsContacts().subscribe((data: any) => {
      this.dhsContacts = data;
    });
  }

  /**
   * EDIT mode
   */
  loadPageForEdit(params: any) {
    const sub = this.subscriptionSvc.subscription;
    sub.subscription_uuid = params.id;

    this.subscriptionSvc.getSubscription(sub.subscription_uuid)
      .subscribe((s: Subscription) => {
        this.subscription = s;
        this.f.primaryContact.setValue(s.primary_contact.email);
        this.f.url.setValue(s.url);
        this.f.url.disable();
        this.f.keywords.setValue(s.keywords);
        this.f.keywords.disable();
        this.f.csvText.setValue(this.emailDisplay(s.target_email_list));
        this.f.csvText.disable();

        this.buildSubscriptionTimeline(s);

        this.customerSvc.getCustomer(s.customer_uuid)
          .subscribe((c: Customer) => {
            this.customer = c;
          });
      });
  }

  /**
   *
   */
  loadContactsForCustomer(customerUuid: string) {
    // get the customer and contacts from the API
    this.customerSvc.getCustomer(customerUuid).subscribe((c: Customer) => {
      this.customer = c;

      this.customer.contact_list = this.customerSvc.getContactsForCustomer(c);
      this.primaryContact = this.customer.contact_list[0];
    });
  }

  /**
   * Boils down all events in all campaigns in the subscription to a simple
   * series of events:  subscription start, cycle starts and today.
   */
  buildSubscriptionTimeline(s: Subscription) {
    const items: TimelineItem[] = [];

    items.push({
      title: 'Subscription Started',
      date: moment(s.start_date)
    });

    // now extract a simple timeline based on campaign events
    s.gophish_campaign_list.forEach((c: GoPhishCampaignModel) => {
      for (const t of c.timeline) {

        // ignore campaigns started on the subscription start date
        if (t.message.toLowerCase() === 'campaign created'
          && isSameDate(t.time, s.start_date)) {
          continue;
        }

        // ignore extra campaign starts we have already put into the list
        if (t.message.toLowerCase() === 'campaign created'
          && items.find(x => isSameDate(x.date, t.time)) !== null) {
          continue;
        }

        if (t.message.toLowerCase() === 'campaign created') {
          items.push({
            title: 'Cycle Start',
            date: moment(t.time)
          });
        }
      }
    });

    // add an item for 'today'
    items.push({
      title: 'Today',
      date: moment()
    });

    this.timelineItems = items;
  }

  /**
   * Presents a customer page to select or create a new customer for
   * this subscription.
   */
  public showCustomerDialog(): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.maxHeight = '80vh';
    dialogConfig.width = '80vw';
    dialogConfig.data = {};
    const dialogRef = this.dialog.open(CustomerDialogComponent, dialogConfig);

    dialogRef.afterClosed().subscribe(value => {
      this.setCustomer();
    });
  }

  /**
   * Shows Dialog for archiving a subscription
   */
  public showArchiveDialog(): void {
    const dialogRef = this.dialog.open(
      ArchiveSubscriptionDialogComponent, {
      data: this.subscription
    }
    );
  }

  /**
   *
   */
  changePrimaryContact(e: any) {
    if (!this.customer) {
      return;
    }
    this.primaryContact = this.customer.contact_list
      .find(x => (x.email) === e.value);
    this.subscription.primary_contact = this.primaryContact;
    this.subscriptionSvc.subscription.primary_contact = this.primaryContact;

    // patch the subscription in real time if in edit mode
    if (this.pageMode === 'EDIT') {
      this.subscriptionSvc.updatePrimaryContact(this.subscription.subscription_uuid, this.primaryContact)
        .subscribe();
    }
  }

  changeDhsContact(e: any) {
    if (!this.dhsContact) {
      return;
    }
    const contact = this.dhsContacts
      .find(x => (x.dhs_contact_uuid) === e.value);
    if (contact) {
      this.dhsContact = contact.dhs_contact_uuid;
      this.subscription.dhs_contact_uuid = this.dhsContact;
    }
  }

  /**
   * Programatically clicks the corresponding file upload element.
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
    const file: any = e.target.files[0];

    const x = new XlsxToCsv();
    x.convert(file).then((xyz: string) => {
      this.csvText = xyz;
      this.f.csvText.setValue(xyz);
    });
  }

  /**
   * Formats emails for display in the form.
   */
  emailDisplay(targetList: Target[]) {
    let output = '';
    targetList.forEach((t: Target) => {
      output += `${t.email}, ${t.first_name}, ${t.last_name}, ${t.position}\n`;
    });
    return output;
  }

  subValid() {
    this.submitted = true;

    // stop here if form is invalid
    if (this.subscribeForm.invalid) {
      return false;
    }

    return true;
  }

  startSubscription() {
    const sub = this.subscriptionSvc.subscription;

    // set up the subscription and persist it in the service
    sub.customer_uuid = this.customer.customer_uuid;
    sub.primary_contact = this.primaryContact;
    sub.active = true;
    sub.lub_timestamp = new Date();
    sub.start_date = this.startDate;
    sub.status = 'Starting';
    sub.url = this.url;
    sub.keywords = this.f.keywords.value;
    // set the target list
    const csv = this.f.csvText.value;
    sub.setTargetsFromCSV(csv);

    // call service with everything needed to start the subscription
    this.subscriptionSvc.restartSubscription(sub).subscribe(
      resp => {
        alert('Subscription ' + sub.name + ' was started');
      },
      error => {
        alert('An error occurred restarting the subscription: ' + error.error);
      });
  }
  /**
   * Submits the form to create a new Subscription.
   */
  onSubmit() {
    if (!this.subValid()) {
      return;
    }

    let sub = this.subscriptionSvc.subscription;

    // set up the subscription and persist it in the service
    sub = new Subscription();

    sub.customer_uuid = this.customer.customer_uuid;
    sub.primary_contact = this.primaryContact;
    sub.dhs_contact_uuid = this.dhsContact;
    sub.active = true;

    sub.lub_timestamp = new Date();
    sub.name = 'SC-1.' + this.customer.name + '.1.1'; // auto generated name
    sub.start_date = this.startDate;
    sub.status = 'New Not Started';

    sub.url = this.url;

    // keywords
    sub.keywords = this.f.keywords.value;

    // set the target list
    const csv = this.f.csvText.value;
    sub.setTargetsFromCSV(csv);

    // call service with everything needed to start the subscription
    this.subscriptionSvc.submitSubscription(sub).subscribe(
      resp => {
        this.dialog.open(AlertComponent, {
          data: {
            title: '',
            messageText: 'Your subscription was created as ' + sub.name
          }
        });

        this.router.navigate(['subscriptions']);
      },
      error => {
        this.dialog.open(AlertComponent, {
          data: {
            title: 'Error',
            messageText: 'An error occurred submitting the subscription: ' + error.error
          }
        });
      });
  }



  /**
   *
   */
  addDays(date, days) {
    const result = new Date(date);
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
