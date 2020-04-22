import { HttpClientModule, HTTP_INTERCEPTORS, HttpClient } from '@angular/common/http';
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
import { CreateSubscriptionComponent } from './components/subscriptions/create-subscription/create-subscription.component';
import { DeceptionCalculatorComponent } from './components/deception-calculator/deception-calculator.component';
import { DeceptionCalculatorService } from './components/deception-calculator/deception-calculator.service';
import { AutosizeModule } from 'node_modules/ngx-autosize';
import { AddOrganizationComponent } from './components/organization/add-organization/add-organization.component';
import { SubscriptionService } from './services/subscription.service';
import { ThemeService } from './services/theme.service';


@NgModule({
  declarations: [
    AppComponent, 
    SubscriptionsComponent, 
    LayoutBlankComponent, 
    LayoutMainComponent, 
    SearchPanelComponent, 
    ServiceSubscriptionComponent,
    AddOrganizationComponent,
    CreateSubscriptionComponent,
    DeceptionCalculatorComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule, 
    MaterialModule, 
    FormsModule, 
    ReactiveFormsModule,
    AutosizeModule,
    HttpClientModule
  ],
  providers: [
    SubscriptionsService,    
    DeceptionCalculatorService,
    ThemeService,
    HttpClient,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
