import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatDialogConfig, MatDialog, MatDialogRef } from '@angular/material/dialog';
import { FormGroup, FormControl, FormBuilder, Validators } from '@angular/forms';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { Router, ActivatedRoute } from '@angular/router';
import { Customer, Contact } from 'src/app/models/customer.model';
import { Subscription, Target, GoPhishCampaignModel, TimelineItem } from 'src/app/models/subscription.model';
import { Guid } from 'guid-typescript';
import { UserService } from 'src/app/services/user.service';
import { CustomerService } from 'src/app/services/customer.service';
import { XlsxToCsv } from 'src/app/helper/XlsxToCsv';
import * as moment from 'node_modules/moment/moment';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { CustomerDialogComponent } from '../../dialogs/customer-dialog/customer-dialog.component';
import { AlertComponent } from '../../dialogs/alert/alert.component';
import { isSameDate } from 'src/app/helper/utilities';
import { ConfirmComponent } from '../../dialogs/confirm/confirm.component';
import { SendingProfileService } from 'src/app/services/sending-profile.service';
import { SettingsService } from 'src/app/services/settings.service';


@Component({
  selector: 'app-manage-subscription',
  templateUrl: './manage-subscription.component.html',
  styleUrls: ['./manage-subscription.component.scss']
})
export class ManageSubscriptionComponent implements OnInit, OnDestroy {
  private routeSub: any;
  dialogRefConfirm: MatDialogRef<ConfirmComponent>;

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
  dhsContactUuid: string;

  startDate: Date = new Date();
  startAt = new Date();

  url: string;
  keywords: string;

  sendingProfiles = [];

  // The raw CSV content of the textarea
  csvText: string;

  timelineItems: any[] = [];


  /**
   *
   */
  constructor(
    public subscriptionSvc: SubscriptionService,
    public customerSvc: CustomerService,
    public sendingProfileSvc: SendingProfileService,
    private router: Router,
    private route: ActivatedRoute,
    private userSvc: UserService,
    public dialog: MatDialog,
    public formBuilder: FormBuilder,
    public layoutSvc: LayoutMainService,
    public settingsService: SettingsService
  ) {
    layoutSvc.setTitle('Subscription');
    this.loadDhsContacts();
    this.loadSendingProfiles();
  }

  /**
   * INIT
   */
  ngOnInit(): void {

    // build form
    this.subscribeForm = new FormGroup({
      selectedCustomerUuid: new FormControl('', {
        validators: Validators.required
      }),
      primaryContact: new FormControl(null, {
        validators: Validators.required
      }),
      dhsContact: new FormControl(null, {
        validators: Validators.required
      }),
      startDate: new FormControl(new Date()),
      url: new FormControl(''),
      keywords: new FormControl(''),
      sendingProfile: new FormControl('', {
        validators: Validators.required
      }),
      csvText: new FormControl('', {
        validators: Validators.required
      }),
      removeDuplicateTargets: new FormControl(true)
    }, {
      updateOn: 'blur'

    });

    this.onChanges();

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
   * Setup handlers for form field updates
   */
  onChanges(): void {
    this.f.startDate.valueChanges.subscribe(val => {
      this.subscription.start_date = val;
      this.persistChanges();
    });
    this.f.url.valueChanges.subscribe(val => {
      this.subscription.url = val;
      this.persistChanges();
    });
    this.f.keywords.valueChanges.subscribe(val => {
      this.subscription.keywords = val;
      this.persistChanges();
    });
    this.f.sendingProfile.valueChanges.subscribe(val => {
      this.subscription.sending_profile_name = val;
    });
    this.f.csvText.valueChanges.subscribe(val => {
      this.subscription.target_email_list = this.buildTargetsFromCSV(val);
      this.f.csvText.setValue(this.formatTargetsToCSV(this.subscription.target_email_list), { emitEvent: false });
      this.persistChanges();
    });
    this.f.removeDuplicateTargets.valueChanges.subscribe(val => {
      this.subscriptionSvc.removeDupeTargets = val;
    });
  }

  /**
   * Sends the model to the API if the subscription is in edit mode.
   */
  persistChanges() {
    // patch the subscription in real time if in edit mode
    if (this.pageMode.toLowerCase() === 'edit') {
      this.subscriptionSvc.patchSubscription(this.subscription).subscribe();
    }
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
    this.subscription = new Subscription();
    this.subscription.subscription_uuid = Guid.create().toString();
    this.enableDisableFields();
  }

  /**
   * EDIT mode
   */
  loadPageForEdit(params: any) {
    const sub = this.subscriptionSvc.subscription;
    sub.subscription_uuid = params.id;

    this.subscriptionSvc.getSubscription(sub.subscription_uuid)
      .subscribe((s: Subscription) => {
        this.subscription = s as Subscription;
        this.subscriptionSvc.subscription = this.subscription;
        this.layoutSvc.setTitle(`Subscription - ${this.subscription.name}`);
        this.f.primaryContact.setValue(s.primary_contact.email);
        this.f.dhsContact.setValue(s.dhs_contact_uuid);
        this.f.url.setValue(s.url);
        this.f.keywords.setValue(s.keywords);
        this.f.csvText.setValue(this.formatTargetsToCSV(s.target_email_list));
        this.f.removeDuplicateTargets.setValue(this.subscriptionSvc.removeDupeTargets);
        this.f.sendingProfile.setValue(s.sending_profile_name);

        this.enableDisableFields();

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

  /**
   * Gets all known DHS contacts from the API.
   */
  loadDhsContacts() {
    this.subscriptionSvc.getDhsContacts().subscribe((data: any) => {
      this.dhsContacts = data;
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
   *
   */
  loadSendingProfiles() {
    // get the customer and contacts from the API
    this.sendingProfileSvc.getAllProfiles().subscribe((data: any) => {
      this.sendingProfiles = data;
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
  public archiveSubscription(): void {
    this.dialogRefConfirm = this.dialog.open(ConfirmComponent, { disableClose: false });
    this.dialogRefConfirm.componentInstance.confirmMessage =
      `Archive '${this.subscription.name}?'`;
    this.dialogRefConfirm.componentInstance.title = 'Confirm Archive';
    this.dialogRefConfirm.afterClosed().subscribe(result => {
      if (result) {
        this.subscription.archived = true;
        this.subscriptionSvc
          .patchSubscription(this.subscription).subscribe(() => { });
        this.enableDisableFields();
      }
    });
  }

  /**
   * Shows Dialog for unarchiving a subscription
   */
  public unarchiveSubscription(): void {
    this.dialogRefConfirm = this.dialog.open(ConfirmComponent, { disableClose: false });
    this.dialogRefConfirm.componentInstance.confirmMessage =
      `Unarchive '${this.subscription.name}?'`;
    this.dialogRefConfirm.componentInstance.title = 'Confirm unarchive';
    this.dialogRefConfirm.afterClosed().subscribe(result => {
      if (result) {
        this.subscription.archived = false;
        this.subscriptionSvc
          .patchSubscription(this.subscription).subscribe(() => { });
        this.enableDisableFields();
      }
    });
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
      this.subscriptionSvc.changePrimaryContact(this.subscription.subscription_uuid, this.primaryContact)
        .subscribe();
    }
  }

  /**
   *
   */
  changeDhsContact(e: any) {
    const contact = this.dhsContacts
      .find(x => (x.dhs_contact_uuid) === e.value);
    if (contact) {
      this.dhsContactUuid = contact.dhs_contact_uuid;
      this.subscription.dhs_contact_uuid = this.dhsContactUuid;

      // patch the subscription in real time if in edit mode
      if (this.pageMode === 'EDIT') {
        this.subscriptionSvc.changeDhsContact(this.subscription.subscription_uuid, this.dhsContactUuid)
          .subscribe();
      }
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

  subValid() {
    this.submitted = true;

    // stop here if form is invalid
    if (this.subscribeForm.invalid) {
      return false;
    }

    return true;
  }

  startSubscription() {
    this.dialogRefConfirm = this.dialog.open(ConfirmComponent, { disableClose: false });
    this.dialogRefConfirm.componentInstance.confirmMessage =
      `Are you sure you want to restart ${this.subscription.name}?`;
    this.dialogRefConfirm.componentInstance.title = 'Confirm Restart';

    this.dialogRefConfirm.afterClosed().subscribe(result => {
      if (result) {
        // persist any changes before restart
        this.subscriptionSvc.patchSubscription(this.subscription).subscribe(x => {

          // restart
          this.subscriptionSvc.restartSubscription(this.subscription.subscription_uuid).subscribe(
            (resp: Subscription) => {
              this.subscription = resp;
              this.enableDisableFields();
              this.dialog.open(AlertComponent, {
                data: {
                  title: '',
                  messageText: `Subscription ${this.subscription.name} was restarted.`
                }
              });
            },
            error => {
              this.dialog.open(AlertComponent, {
                data: {
                  title: 'Error',
                  messageText: 'An error occurred restarting the subscription: ' + error.error
                }
              });
            });
        });
      }
    });
  }

  stopSubscription() {
    this.dialogRefConfirm = this.dialog.open(ConfirmComponent, { disableClose: false });
    this.dialogRefConfirm.componentInstance.confirmMessage =
      `Are you sure you want to stop ${this.subscription.name}?`;
    this.dialogRefConfirm.componentInstance.title = 'Confirm Stop';

    this.dialogRefConfirm.afterClosed().subscribe(result => {
      if (result) {
        this.subscriptionSvc.stopSubscription(this.subscription.subscription_uuid).subscribe(
          (resp: Subscription) => {
            this.subscription = resp;
            this.enableDisableFields();
            this.dialog.open(AlertComponent, {
              data: {
                title: '',
                messageText: `Subscription ${this.subscription.name} was stopped`
              }
            });
          },
          error => {
            this.dialog.open(AlertComponent, {
              data: {
                title: 'Error',
                messageText: 'An error occurred stopping the subscription: ' + error.error
              }
            });
          });
      }
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
    sub.dhs_contact_uuid = this.dhsContactUuid;
    sub.active = true;

    sub.lub_timestamp = new Date();
    sub.name = 'SC-1.' + this.customer.name + '.1.1'; // auto generated name
    sub.start_date = this.startDate;
    sub.status = 'New Not Started';

    sub.url = this.f.url.value;

    // keywords
    sub.keywords = this.f.keywords.value;

    // set the target list
    const csv = this.f.csvText.value;
    sub.target_email_list = this.buildTargetsFromCSV(csv);

    sub.sending_profile_name = this.f.sendingProfile.value;

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
   * Enables and disabled fields based on the subscription status.
   */
  enableDisableFields() {
    const status = this.subscription?.status?.toLowerCase();
    if (status === 'in progress') {
      this.f.url.disable();
      this.f.keywords.disable();
      this.f.sendingProfile.disable();
      this.f.csvText.disable();
    } else {
      this.f.url.enable();
      this.f.keywords.enable();
      this.f.sendingProfile.enable();
      this.f.csvText.enable();
    }
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
   * Converts a string with CSV lines into Targets.
   * Format: email, firstname, lastname, position
   * @param csv A comma-separated string with linefeed delimiters
   */
  public buildTargetsFromCSV(csv: string): Target[] {
    let targetList: Target[] = [];
    if (!csv) {
      return;
    }
    const lines = csv.split('\n');
    lines.forEach((line: string) => {
      const parts = line.split(',');
      if (parts.length === 4) {
        const t = new Target();
        t.email = parts[0].trim();
        t.first_name = parts[1].trim();
        t.last_name = parts[2].trim();
        t.position = parts[3].trim();
        targetList.push(t);
      }
    });

    // remove duplicate emails if desired
    if (this.subscriptionSvc.removeDupeTargets) {
      const uniqueArray: Target[] = targetList.filter((t1, index) => {
        return index === targetList.findIndex(t2 => {
          return t2.email.toLowerCase() === t1.email.toLowerCase();
        });
      });
      targetList = uniqueArray;
    }

    return targetList;
  }

  /**
   * Formats Targets for display in the form.
   */
  formatTargetsToCSV(targetList: Target[]) {
    if (!targetList) {
      return '';
    }
    let output = '';
    targetList.forEach((t: Target) => {
      output += `${t.email}, ${t.first_name}, ${t.last_name}, ${t.position}\n`;
    });

    if (output.length > 0) {
      output = output.substring(0, output.length - 1);
    }

    return output;
  }

  viewMonthlyReport() {
    let url = `${this.settingsService.settings.apiUrl}/api/v1/reports/${this.subscription.subscription_uuid}/pdf/monthly/`;
    window.open(url, "_blank");
  }

  viewCycleReport() {
    let url = `${this.settingsService.settings.apiUrl}/api/v1/reports/${this.subscription.subscription_uuid}/pdf/cycle/`;
    window.open(url, "_blank");
  }

  sendMonthlyReport() {
    let url = `${this.settingsService.settings.apiUrl}/api/v1/reports/$${this.subscription.subscription_uuid}/email/monthly/`;
    window.open(url, "_blank");
  }

  sendCycleReport() {
    let url = `${this.settingsService.settings.apiUrl}/api/v1/reports/${this.subscription.subscription_uuid}/email/cycle/`;
    window.open(url, "_blank");
  }

  /* Not in use yet

  viewYearlyReport() {
    let url = `${this.settingsService.settings.apiUrl}/api/v1/reports/${this.subscription.subscription_uuid}/pdf/yearly/`;
    window.open(url, "_blank");
  }

  sendYearlyReport() {
    let url = `${this.settingsService.settings.apiUrl}/api/v1/reports/${this.subscription.subscription_uuid}/email/yearly/`;
    window.open(url, "_blank");
  }
  */

  /**
   *
   */
  ngOnDestroy() {
    this.routeSub.unsubscribe();
  }
}
