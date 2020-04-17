import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Organization } from '../models/organization.model';
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
   * The service keeps a copy of the Organization
   */
  organization: Organization;
  organizations: Array<Organization> = [];
  /**
   * 
   */
  constructor(
    private http: HttpClient
  ) { 
    //temp initialize organization with mock data
    this.organizations.push(this.TEMPGETORG());
  }

  getSubscriptionsData(){
     return this.http.get('http://localhost:8000/api/v1/subscriptions/', headers);
   }

  /**
   * In real life, API call happens here and the model
   * is returned.
   * For now, a hard-coded model is returned.
   */
  getOrganization(orgId: number) {
    // TEMP
    this.organization = this.TEMPGETORG();
    return new Observable<Organization>();


    return this.http.get('http://bogus.org/subscription/getorg?id=' + orgId);
  }

  /**
   * In real life, API call happens here and the new
   * organization is created.
   * For now, a hard-coded model is returned.
   */
  postOrganization(org: Organization){
    this.organizations.push(org);
    return new Observable<Organization>();

    return this.http.post('http://bogus.org/subscription/postOrg', org);
  }

  /**
   * Returns an array of simple contact
   * names and IDs for the organization.
   */
  getContactsForOrg() {
    let o = this.organization;
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
  TEMPGETORG(): Organization {
    let o = new Organization();
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
