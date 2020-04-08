import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LayoutBlankComponent } from './components/layout/layout-blank/layout-blank.component';
import { LayoutMainComponent } from './components/layout/layout-main/layout-main.component';
import { SubscriptionsComponent } from './components/subscriptions/subscriptions.component';
import { ServiceSubscriptionComponent } from './components/service-subscription/service-subscription.component';
import { SearchPanelComponent } from './components/search-panel/search-panel.component';

const routes: Routes = [
  {
    path:'subscription', component: LayoutMainComponent, 
    children: [
      { path: '', component: SubscriptionsComponent}
    ]
  },
  {
    path:'subscriptions', component: SearchPanelComponent,
    outlet: "sidebar"
  },
  {
    path:'servicesubscription', component: LayoutMainComponent, 
    children: [
      { path: '', component: ServiceSubscriptionComponent}
    ]
  },
  {
    path:'', component: LayoutMainComponent,
    children: [
      { path: '', component: SubscriptionsComponent}
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
