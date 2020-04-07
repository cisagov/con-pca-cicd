import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class SubscriptionService {

  /**
   * 
   */
  constructor(
    private http: HttpClient
  ) { }

  /**
   * In real life, API call happens here and the model
   * is returned.
   * For now, a hard-coded model is returned.
   */
  getOrganization() {
    let fullOrg = {
      organization:
      {
        id: 918,
        orgName: "Delta Airlines Inc.",
        orgAbbrev: "DAL",
        orgAddr1: "1030 Delta Blvd",
        orgCity: "Atlanta",
        orgState: "GA",
        orgType: "Private Non-Government"
      },
      contacts: [
        {
          id: 127,
          firstName: "Mary",
          lastName: "Stephens",
          title: "CISO",
          phone: "208-716-2687",
          email: "MaryStephens@doe.gov"
        },
        {
          id: 123,
          firstName: "Dean",
          lastName: "Young",
          title: "VP Sales",
          phone: "208-716-0218",
          email: "DeanYoung@doe.gov"
        },
        {
          id: 141,
          firstName: "David",
          lastName: "Merrill",
          title: "VP R&D",
          phone: "208-716-8613",
          email: "DavidMerrill@doe.gov"
        },
        {
          id: 98,
          firstName: "Ronald",
          lastName: "Clark",
          title: "VP Human Resources",
          phone: "208-716-3310",
          email: "RonaldClark@doe.gov"
        }
      ]
    };

    return fullOrg;
  }

  /**
   * Returns an array of simple contact
   * names and IDs for the organization.
   */
  getContactsForOrg() {
    let o = this.getOrganization();
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
   * Sends all information to the API to start a new subscription.
   * @param s 
   */
  submitSubscription(s: any) {
    return this.http.post('http://bogus.org/subscription/submit', s);
  }
}
