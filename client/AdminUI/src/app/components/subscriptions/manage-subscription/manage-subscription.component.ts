import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatDialogConfig, MatDialog } from '@angular/material/dialog';
import { FormGroup, FormControl, FormBuilder, Validators } from '@angular/forms';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { Router, ActivatedRoute } from '@angular/router';
import { Customer, Contact } from 'src/app/models/customer.model';
import { Subscription, Target } from 'src/app/models/subscription.model';
import { Guid } from 'guid-typescript';
import { UserService } from 'src/app/services/user.service';
import { CustomerService } from 'src/app/services/customer.service';
import { CustomersComponent } from 'src/app/components/customers/customers.component';
import { XlsxToCsv } from 'src/app/helper/XlsxToCsv';
import { ArchiveSubscriptionDialogComponent } from '../archive-subscription-dialog/archive-subscription-dialog.component';


@Component({
  selector: 'app-manage-subscription',
  templateUrl: './manage-subscription.component.html'
})
export class ManageSubscriptionComponent implements OnInit, OnDestroy {
  private routeSub: any;

  subscribeForm: FormGroup;
  submitted = false;


  action_EDIT: string = 'edit';
  action_CREATE: string = 'create';
  action: string = this.action_EDIT;

  // CREATE or EDIT 
  pageMode: string = 'CREATE';

  subscription: Subscription;
  customer: Customer = new Customer();
  primaryContact: Contact = new Contact();

  startDate: Date = new Date();
  startAt = new Date();

  url: string;
  keywords: string;

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
    public dialog: MatDialog,
    public formBuilder: FormBuilder
  ) {

  }

  /**
   * INIT
   */
  ngOnInit(): void {

    // build form
    this.subscribeForm = new FormGroup({
      selectedCustomerUuid: new FormControl('', Validators.required),
      primaryContact: new FormControl(null, Validators.required),
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
    this.action = this.action_CREATE;
    let sub = this.subscriptionSvc.subscription;
    sub = new Subscription();
    this.subscription = sub;
    sub.subscription_uuid = Guid.create().toString();




    // START TEMP ------------------------
    // find Globex or randomly pick an existing customer for now
    /*if (!this.subscription.customer_uuid) {
      this.customerSvc.getCustomers().subscribe((c: Customer[]) => {

        // first look for Globex
        let globex = c.find(x => x.identifier == 'GLBX');
        if (globex == null) {

          // if not found, just pick a random customer
          let rnd = Math.floor(Math.random() * Math.floor(c.length));
          this.customer = c[rnd];
        } else {
          this.customer = globex;
        }

        this.f.selectedCustomerUuid.setValue(this.customer.customer_uuid);
      });
    }*/
    // END TEMP --------------------------
  }

  setCustomer(){
    if(this.customerSvc.selectedCustomer.length > 0){
      this.subscribeForm.patchValue({
        selectedCustomerUuid: this.customerSvc.selectedCustomer
      });
      this.customerSvc.getCustomer(this.customerSvc.selectedCustomer).subscribe(
        (data: Customer) => {
          this.customer = data;
          this.f.selectedCustomerUuid.setValue(this.customer.customer_uuid)
        }
      )
    }
    
  }

  /**
   * EDIT mode
   */
  loadPageForEdit(params: any) {
    let sub = this.subscriptionSvc.subscription;
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

        this.customerSvc.getCustomer(s.customer_uuid)
          .subscribe((c: Customer) => {
            this.customer = c;
          });
      });
  }

  /**
   * 
   * @param customer_uuid 
   */
  loadContactsForCustomer(customer_uuid: string) {
    // get the customer and contacts from the API
    this.customerSvc.getCustomer(customer_uuid).subscribe((c: Customer) => {
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
      this.setCustomer();
    })
  }

  /**
   * Shows Dialog for archiving a subscription
   */
  public showArchiveDialog(): void {
    const dialogRef = this.dialog.open(
      ArchiveSubscriptionDialogComponent, {
        data: this.subscription
      }
    )
  }

  /**
   * 
   */
  changePrimaryContact(e: any) {
    if (!this.customer) {
      return;
    }
    this.primaryContact = this.customer.contact_list
      .find(x => (x.email) == e.value);
    this.subscription.primary_contact = this.primaryContact;
    this.subscriptionSvc.subscription.primary_contact = this.primaryContact;

    // patch the subscription in real time if in edit mode
    if (this.pageMode == 'EDIT') {
      this.subscriptionSvc.updatePrimaryContact(this.subscription.subscription_uuid, this.primaryContact)
        .subscribe();
    }
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

  /**
   * Submits the form to create a new Subscription.
   */
  onSubmit() {
    this.submitted = true;

    // stop here if form is invalid
    if (this.subscribeForm.invalid) {
      return;
    }

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

    sub.url = this.url;

    // keywords
    sub.keywords = this.f.keywords.value;

    // set the target list
    let csv = this.f.csvText.value;
    sub.setTargetsFromCSV(csv);

    // call service with everything needed to start the subscription
    this.subscriptionSvc.submitSubscription(sub).subscribe(
      resp => {
        alert("Your subscription was created as " + sub.name);
        this.router.navigate(['subscriptions']);
      },
      error => {
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
