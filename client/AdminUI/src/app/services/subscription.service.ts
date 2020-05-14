import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Customer } from '../models/customer.model';
import { Observable } from 'rxjs';
import { Subscription } from 'src/app/models/subscription.model';
import { Router } from "@angular/router";

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

  /**
   * The service keeps a copy of the Customer
   */
  customer: Customer;
  customers: Array<Customer> = [];
  /**
   * 
   */
  constructor(
    private http: HttpClient
  ) { 

  }

  getSubscriptionsData(){
     return this.http.get('http://localhost:8000/api/v1/subscriptions/', headers);
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
