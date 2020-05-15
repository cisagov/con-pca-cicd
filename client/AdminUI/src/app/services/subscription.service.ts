import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Customer } from '../models/customer.model';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Subscription } from '../models/subscription.model';
import { CustomerService } from './customer.service';

const headers = {
  headers: new HttpHeaders()
    .set('Content-Type', 'application/json'),
  params: new HttpParams()
};


@Injectable({
  providedIn: 'root'
})
export class SubscriptionService {
  subscription: Subscription;
  customer: Customer;
  customers: Array<Customer> = [];

  constructor(private http: HttpClient, private customer_service: CustomerService) { }

  /**
   * 
   */
  public getSubscriptions() {
    let url = `${environment.apiEndpoint}/api/v1/subscriptions/`
    return this.http.get(url)
  }

  /**
   * 
   * @param requestData 
   */
  public toSubscriptions(requestData: any[]): Subscription[] {
    let subscriptions: Subscription[] = []
    requestData.map((s: any) => {
      subscriptions.push(this.toSubscription(s))
    })
    return subscriptions
  }

  /**
   * 
   * @param subscription_uuid 
   */
  public getSubscription(subscription_uuid: string) {
    let url = `${environment.apiEndpoint}/api/v1/subscription/${subscription_uuid}/`
    return this.http.get(url)
  }

  /**
   * 
   * @param requestData 
   */
  public toSubscription(requestData: any): Subscription {
    let subscription: Subscription = {
      active: requestData.active,
      customer_uuid: requestData.customer_uuid,
      keywords: requestData.keywords,
      lub_timestamp: requestData.lub_timestamp,
      name: requestData.name,
      primary_contact: this.customer_service.getContact(requestData.primary_contact),
      start_date: requestData.start_date,
      status: requestData.status,
      subscription_uuid: requestData.subscription_uuid,
      url: requestData.url,
      target_email_list: requestData.target_email_list,
      setTargetsFromCSV: null
    }

    return subscription
  }

  /**
   * Sends all information to the API to start a new subscription.
   * @param s 
   */
  submitSubscription(subscription: Subscription) {
    return this.http.post('http://localhost:8000/api/v1/subscriptions/', subscription)
  }
}
