import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LayoutMainComponent } from './components/layout/layout-main/layout-main.component';
import { SubscriptionsComponent } from './components/subscriptions/subscriptions.component';
import { ManageSubscriptionComponent } from './components/subscriptions/manage-subscription/manage-subscription.component';
import { DeceptionCalculatorComponent } from './components/deception-calculator/deception-calculator.component';
import { TemplateManagerComponent } from './components/template-manager/template-manager.component';
import { SearchPanelComponent } from './components/search-panel/search-panel.component';
import { ContactsComponent } from './components/contacts/contacts.component';
import { DomainsComponent } from './components/domains/domains.component';
import { TemplatesPageComponent } from './components/templates-page/templates-page.component';
import { UserAdminComponent } from './components/user-admin/user-admin.component';
import { CustomersComponent } from './components/customers/customers.component';
import { AddCustomerComponent } from './components/customer/add-customer/add-customer.component'
import { SendingProfilesComponent } from './components/sending-profiles/sending-profiles.component';
import { DhsPocComponent } from './components/user-admin/dhs-poc/dhs-poc.component';


const routes: Routes = [
  {
    path: 'subscriptions',
    component: LayoutMainComponent,
    children: [
      { path: '', component: SubscriptionsComponent },
      { path: '', component: SearchPanelComponent, outlet: 'sidebar' }
    ]
  },
  {
    path: 'create-subscription',
    component: LayoutMainComponent,
    children: [{ path: '', component: ManageSubscriptionComponent }]
  },
  {
    path: 'view-subscription',
    component: LayoutMainComponent,
    children: [{ path: ':id', component: ManageSubscriptionComponent }]
  },
  {
    path: 'deceptioncalculator',
    component: LayoutMainComponent,
    children: [{ path: '', component: DeceptionCalculatorComponent }]
  },
  {
    path: 'deceptioncalculator/:templateId',
    component: LayoutMainComponent,
    children: [{ path: '', component: DeceptionCalculatorComponent }]
  },
  {
    path: 'templatemanager',
    component: LayoutMainComponent,
    children: [{ path: '', component: TemplateManagerComponent }]
  },
  {
    path: 'templatemanager/:templateId',
    component: LayoutMainComponent,
    children: [{ path: '', component: TemplateManagerComponent }]
  },
  {
    path: 'templates', component: LayoutMainComponent,
    children: [
      { path: '', component: TemplatesPageComponent }
    ]
  },
  {
    path: 'contacts', component: LayoutMainComponent,
    children: [
      { path: '', component: ContactsComponent }
    ]
  },
  {
    path: 'customers', component: LayoutMainComponent,
    children: [
      { path: '', component: CustomersComponent }
    ]
  },
  {
    path: 'customer/:customerId', component: LayoutMainComponent,
    children: [
      { path: '', component: AddCustomerComponent }
    ]
  },
  {
    path: 'domains', component: LayoutMainComponent,
    children: [
      { path: '', component: DomainsComponent }
    ]
  },
  {
    path: 'useradmin', component: LayoutMainComponent,
    children: [
      { path: '', component: UserAdminComponent }
    ]
  },
  {
    path: 'dhspoc', component: LayoutMainComponent,
    children: [
      { path: '', component: DhsPocComponent }
    ]
  },
  {
    path: 'sending-profiles', component: LayoutMainComponent,
    children: [
      { path: '', component: SendingProfilesComponent }
    ]
  },
  {
    path: '', component: LayoutMainComponent,
    children: [
      { path: '', component: SubscriptionsComponent }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
