import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from './material.module';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { SubscriptionsComponent } from './components/subscriptions/subscriptions.component';
import { LayoutBlankComponent } from './components/layout/layout-blank/layout-blank.component';
import { LayoutMainComponent } from './components/layout/layout-main/layout-main.component';
import { SubscriptionsService } from './components/subscriptions/subscriptions.service';
import { SearchPanelComponent } from './components/search-panel/search-panel.component';
import { ServiceSubscriptionComponent } from './components/service-subscription/service-subscription.component';

@NgModule({
  declarations: [
    AppComponent, 
    SubscriptionsComponent, 
    LayoutBlankComponent, 
    LayoutMainComponent, 
    SearchPanelComponent, 
    ServiceSubscriptionComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule, 
    MaterialModule, 
    FormsModule, 
    ReactiveFormsModule
  ],
  providers: [
    SubscriptionsService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
