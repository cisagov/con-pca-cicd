import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Customer } from '../models/customer.model';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Subscription } from '../models/subscription.model';

const headers = {
   headers: new HttpHeaders()
     .set('Content-Type', 'application/json'),
   params: new HttpParams()
 };


@Injectable({
  providedIn: 'root'
})
export class SubscriptionService {
  customer: Customer;
  customers: Array<Customer> = [];

  constructor(private http: HttpClient) { }

  public requestGetSubscriptions() { 
    let url = `${environment.apiEndpoint}/api/v1/subscriptions/`
    return this.http.get(url)
  }
  
  public getSubscriptions(requestData: any[]): Subscription[] {
    let subscriptions: Subscription[] = []
    requestData.map((s: any) => {
      subscriptions.push(this.getSubscription(s))
    })
    return subscriptions
  }

  public getSubscription(requestData: any): Subscription {
    let subscription: Subscription = {
      active: requestData.active,
      customer_uuid: requestData.customer_uuid,
      keywords: requestData.keywords,
      name: requestData.name,
      start_date: requestData.start_date,
      status: requestData.status,
      subscription_uuid: requestData.subscription_uuid,
      url: requestData.url
    }

    return subscription
  }

  /**
   * In real life, API call happens here and the model
   * is returned.
   * For now, a hard-coded model is returned.
   */
  getCustomer(customerId: string) {
    return this.http.get('http://localhost:8000/api/v1/customer/' + customerId);
  }

  /**
   * In real life, the customer is posted from the customer component,
   * not the subscription component.
   */
  postCustomer(org: Customer){
    this.customers.push(org);
    return new Observable<Customer>();

    return this.http.post('http://bogus.org/subscription/postOrg', org);
  }

  /**
   * Returns an array of simple contact
   * names and IDs for the customer.
   */
  getContactsForCustomer(c: Customer) {
    console.log('getContactsForCustomer:');
    console.log(c);

    let a = [];
    c.contact_list.forEach(x => {
      a.push({
        name: x.first_name + ' ' + x.last_name
      });
    });
    return a;
  }


  /**
   * Sends all information to the API to start a new subscription.
   * @param s 
   */
  submitSubscription(subscription) {
    //NEED TO MAKE THIS LOOK at the 
    return this.http.post('http://localhost:8000/api/v1/subscriptions/', subscription)
  }
}
