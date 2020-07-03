import {
  HttpClientModule,
  HTTP_INTERCEPTORS,
  HttpClient
} from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule, APP_INITIALIZER } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AngularEditorModule } from '@kolkov/angular-editor';
import { MaterialModule } from './material.module';
import { MatSortModule } from '@angular/material/sort';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AmplifyService } from 'aws-amplify-angular';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { SubscriptionsComponent } from './components/subscriptions/subscriptions.component';
import { LayoutBlankComponent } from './components/layout/layout-blank/layout-blank.component';
import { LayoutMainComponent } from './components/layout/layout-main/layout-main.component';
import { SearchPanelComponent } from './components/search-panel/search-panel.component';
import { ManageSubscriptionComponent } from './components/subscriptions/manage-subscription/manage-subscription.component';
import { DeceptionCalculatorComponent } from './components/deception-calculator/deception-calculator.component';
import { UserAuthService } from './services/user-auth.service';
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
import { HelpFilesComponent } from './components/help-files/help-files.component';
import { CustomerService } from './services/customer.service';
import { CustomersComponent } from './components/customers/customers.component';
import { AddCustomerDialogComponent } from './components/customers/add-customer-dialog/add-customer-dialog.component';
import { AddContactDialogComponent } from './components/contacts/add-contact-dialog/add-contact-dialog.component';
import { ViewContactDialogComponent } from './components/contacts/view-contact-dialog/view-contact-dialog.component';
import { DeleteSubscription, DeleteSubscriptionDialog } from 'src/app/components/subscriptions/delete-subscription/delete-subscription.component';
import { StopTemplateDialogComponent } from './components/template-manager/stop-template-dialog/stop-template-dialog.component';
import { SendingProfilesComponent } from './components/sending-profiles/sending-profiles.component';
import { SendingProfileDetailComponent } from './components/sending-profiles/sending-profile-detail.component';
import { CustomerSubscriptionsComponent } from './components/subscriptions/customer-subscriptions/customer-subscriptions.component';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { SubDashboardComponent } from './components/subscriptions/sub-dashboard/sub-dashboard.component';
import { ConfirmComponent } from './components/dialogs/confirm/confirm.component';
import { TagSelectionComponent } from './components/dialogs/tag-selection/tag-selection.component';
import { SettingsHttpService } from './services/settings-http.service';
import { RetireTemplateDialogComponent } from './components/template-manager/retire-template-dialog/retire-template-dialog.component';
import { CustomerDialogComponent } from './components/dialogs/customer-dialog/customer-dialog.component';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { AlertComponent } from './components/dialogs/alert/alert.component';
import { SafePipe } from './helper/safe.pipe';
import { SvgTimelineComponent } from './components/subscriptions/svg-timeline/svg-timeline.component';
import { AuthAppendInterceptor } from './helper/AuthAppendInterceptor'
import { UnauthorizedInterceptor } from './helper/UnauthorizedInterceptor'
import { DhsPocComponent } from './components/user-admin/dhs-poc/dhs-poc.component';
import { DhsPocDetailComponent } from './components/user-admin/dhs-poc/dhs-poc-detail.component';
import { InputTrimDirective } from './helper/input-trim.directive';

export function app_Init(settingsHttpService: SettingsHttpService) {
  return () => settingsHttpService.initializeApp()
}


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
    HelpFilesComponent,
    CustomersComponent,
    AddCustomerDialogComponent,
    AddContactDialogComponent,
    ViewContactDialogComponent,
    DeleteSubscription,
    DeleteSubscriptionDialog,
    StopTemplateDialogComponent,
    SendingProfilesComponent,
    SendingProfileDetailComponent,
    CustomerSubscriptionsComponent,
    SubDashboardComponent,
    ConfirmComponent,
    TagSelectionComponent,
    RetireTemplateDialogComponent,
    CustomerDialogComponent,
    AlertComponent,
    SafePipe,
    SvgTimelineComponent,
    DhsPocComponent,
    DhsPocDetailComponent,
    InputTrimDirective,
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
    HttpClientModule,
    NgxChartsModule,
  ],
  providers: [
    SubscriptionService,
    DeceptionCalculatorService,
    CustomerService,
    TemplateManagerService,
    ThemeService,
    LayoutMainService,
    HttpClient,
    AmplifyService,
    UserAuthService,
    { provide: MAT_DIALOG_DATA, useValue: [] },
    { provide: APP_INITIALIZER, useFactory: app_Init, deps: [SettingsHttpService], multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: AuthAppendInterceptor, multi: true},
    { provide: HTTP_INTERCEPTORS, useClass: UnauthorizedInterceptor, multi: true},
  ],
  exports: [
    MatSortModule
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
