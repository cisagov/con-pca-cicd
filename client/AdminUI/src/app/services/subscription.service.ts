import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Customer, Contact } from '../models/customer.model';
import { environment } from 'src/environments/environment';
import { Subscription } from '../models/subscription.model';
import { CustomerService } from './customer.service';
import { Template } from '../models/template.model';
import { Observable } from 'rxjs';

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

  cameFromSubscription: boolean;

  /**
   * 
   * @param http 
   * @param customer_service 
   */
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
   * @param subscription_uuid 
   */
  public getSubscription(subscription_uuid: string) {
    let url = `${environment.apiEndpoint}/api/v1/subscription/${subscription_uuid}/`
    return this.http.get(url)
  }

  public deleteSubscription(subscription: Subscription) {
    return new Promise((resolve, reject) => {
      this.http
        .delete(`${environment.apiEndpoint}/api/v1/subscription/${subscription.subscription_uuid}/`)
        .subscribe(
          success => {
            resolve(success);
          },
          error => {
            reject(error)
          }
        )
    })
  }

  /**
   * Sends all information to the API to start a new subscription.
   * @param s 
   */
  submitSubscription(subscription: Subscription) {
    return this.http.post('http://localhost:8000/api/v1/subscriptions/', subscription)
  }

  /**
   * Sends information to the API to update a subscription
   * @param subscription 
   */
  patchSubscription(subscription: Subscription) {
    return this.http.patch(`http://localhost:8000/api/v1/subscription/${subscription.subscription_uuid}/`, subscription)
  }

  /**
   * Patches the subscription with the new primary contact.
   * @param subscriptUuid 
   * @param contact 
   */
  updatePrimaryContact(subscriptUuid: string, contact: Contact) {
    let primary = { primary_contact: contact };
    return this.http.patch(`http://localhost:8000/api/v1/subscription/${subscriptUuid}/`, primary)
  }

  /**
   * Gets all subscriptions for a given template.
   * @param template 
   */
  public getSubscriptionsByTemplate(template: Template) {
    return this.http.get(`${environment.apiEndpoint}/api/v1/subscription/template/${template.template_uuid}`)
  }

  /**
   * Gets all subscriptions for a given customer.
   * @param template 
   */
  public getSubscriptionsByCustomer(customer: Customer) {
    return this.http.get(`${environment.apiEndpoint}/api/v1/subscription/customer/${customer.customer_uuid}`)
  }

  public stopSubscription(subscription: Subscription) {
    return this.http.get(`${environment.apiEndpoint}/api/v1/subscription/stop/${subscription.subscription_uuid}/`)
  }

  /**
   * Gets timeline items for the subscription.
   */
  public getTimelineItems(subscription_uuid) {
    let url = `${environment.apiEndpoint}/api/v1/subscription/timeline/${subscription_uuid}/`
    return this.http.get(url);
  }
}
