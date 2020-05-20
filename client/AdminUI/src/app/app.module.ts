import {
  HttpClientModule,
  HTTP_INTERCEPTORS,
  HttpClient
} from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AngularEditorModule } from '@kolkov/angular-editor';
import { MaterialModule } from './material.module';
import { MatSortModule } from '@angular/material/sort'
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { SubscriptionsComponent } from './components/subscriptions/subscriptions.component';
import { LayoutBlankComponent } from './components/layout/layout-blank/layout-blank.component';
import { LayoutMainComponent } from './components/layout/layout-main/layout-main.component';
import { SearchPanelComponent } from './components/search-panel/search-panel.component';
import { ManageSubscriptionComponent } from './components/subscriptions/manage-subscription/manage-subscription.component';
import { DeceptionCalculatorComponent } from './components/deception-calculator/deception-calculator.component';
import { DeceptionCalculatorService } from './services/deception-calculator.service';
import { TemplateManagerComponent } from './components/template-manager/template-manager.component';
import { TemplateManagerService } from './services/template-manager.service';
import { ListFilterPipe } from './pipes/list-filter.pipe';
import { AutosizeModule } from 'node_modules/ngx-autosize';
import { AddCustomerComponent } from './components/customer/add-customer/add-customer.component';
import { SubscriptionService } from './services/subscription.service';
import { ThemeService } from './services/theme.service';
import { LayoutMainService } from './services/layout-main.service';

import { ContactsComponent } from './components/contacts/contacts.component';
import { DomainsComponent } from './components/domains/domains.component';
import { TemplatesPageComponent } from './components/templates-page/templates-page.component';
import { UserAdminComponent } from './components/user-admin/user-admin.component';
import { CustomerService } from './services/customer.service';
import { CustomersComponent } from './components/customers/customers.component';
import { AddCustomerDialogComponent } from './components/customers/add-customer-dialog/add-customer-dialog.component';
import { AddContactDialogComponent } from './components/contacts/add-contact-dialog/add-contact-dialog.component';
import { ViewContactDialogComponent } from './components/contacts/view-contact-dialog/view-contact-dialog.component';
import { DeleteSubscription, DeleteSubscriptionDialog} from 'src/app/components/subscriptions/delete-subscription/delete-subscription.component'


@NgModule({
  declarations: [
    AppComponent,
    SubscriptionsComponent,
    LayoutBlankComponent,
    LayoutMainComponent,
    SearchPanelComponent,
    AddCustomerComponent,
    ManageSubscriptionComponent,
    DeceptionCalculatorComponent,

    TemplateManagerComponent,
    ListFilterPipe,
    ContactsComponent,
    DomainsComponent,
    TemplatesPageComponent,
    UserAdminComponent,
    CustomersComponent,
    AddCustomerDialogComponent,
    AddContactDialogComponent,
    ViewContactDialogComponent,
    DeleteSubscription,
    DeleteSubscriptionDialog,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AngularEditorModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule,
    MatSortModule,
    FormsModule,
    ReactiveFormsModule,
    AutosizeModule,
    HttpClientModule
  ],
  providers: [
    SubscriptionService,
    DeceptionCalculatorService,
    CustomerService,
    TemplateManagerService,
    ThemeService,
    LayoutMainService,
    HttpClient
  ],
  exports: [
    MatSortModule
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
