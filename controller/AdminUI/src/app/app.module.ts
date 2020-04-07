import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from './material.module';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { SubscriptionsComponent } from './components/subscriptions/subscriptions.component';
import { LayoutBlankComponent } from './components/layout/layout-blank/layout-blank.component';
import { LayoutMainComponent } from './components/layout/layout-main/layout-main.component';
import { SubscriptionsService } from './components/subscriptions/subscriptions.service';
import { SearchPanelComponent } from './components/search-panel/search-panel.component';
import { ServiceSubscriptionComponent } from './components/service-subscription/service-subscription.component';
import { CreateSubscriptionComponent } from './components/subscriptions/create-subscription/create-subscription.component';
import { AutosizeModule } from 'node_modules/ngx-autosize';
import { MatNativeDateModule } from '@angular/material/core';

@NgModule({
  declarations: [
    AppComponent, 
    SubscriptionsComponent, 
    LayoutBlankComponent, 
    LayoutMainComponent, 
    SearchPanelComponent, 
    ServiceSubscriptionComponent,
    CreateSubscriptionComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule, 
    MaterialModule, 
    FormsModule, 
    ReactiveFormsModule,
    AutosizeModule,
    MatDatepickerModule,
    MatNativeDateModule
  ],
  providers: [
    SubscriptionsService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
