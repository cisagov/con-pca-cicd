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
    //temp initialize customer with mock data
    this.customers.push(this.TEMPGETORG());
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
    // TEMP
    this.customer = this.TEMPGETORG();
    return new Observable<Customer>();


    return this.http.get('http://bogus.org/subscription/getorg?id=' + customerId);
  }

  /**
   * In real life, API call happens here and the new
   * customer is created.
   * For now, a hard-coded model is returned.
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
  getContactsForCustomer() {
    let o = this.customer;
    let a = [];
    o.contacts.forEach(x => {
      a.push({
        id: x.id,
        name: x.firstName + ' ' + x.lastName
      });
    });
    return a;
  }

  /**
   * TEMP TEMP
   * This mocks up an Organization that would be returned from an API call
   */
  TEMPGETORG(): Customer {
    let o = new Customer();
    o.id = 123;
    o.orgName = "Delta Airlines";
    o.orgAbbrev = "DAL";
    o.orgAddress1 = "1030 Delta Blvd";
    o.orgCity = "Atlanta";
    o.orgState = "GA";
    o.orgZip = "30354";

    o.orgType = "Private Non-Government";

    o.contacts = [];
    o.contacts.push(
      {
        id: '201',
        firstName: 'Mary',
        lastName: 'Stephens',
        title: 'CISO',
        phone: '208-716-2687',
        email: 'Mary.Stephens@delta.com',
        contactNotes: ''
      }
    );

    o.contacts.push(
      {
        id: '202',
        firstName: 'John',
        lastName: 'Shirlaw',
        title: 'VP R&D',
        phone: '208-921-1010',
        email: 'John.Shirlaw@delta.com',
        contactNotes:''
      });

    o.contacts.push(
      {
        id: '203',
        firstName: 'Yanik',
        lastName: 'Zarabraya',
        title: 'VP HR',
        phone: '208-377-9339',
        email: 'Yanik.Zarabraya@delta.com',
        contactNotes: ''
      });

    console.log(o);
    return o;
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
