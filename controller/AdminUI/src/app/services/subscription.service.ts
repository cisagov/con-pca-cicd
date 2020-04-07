import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SubscriptionService {

  /**
   * 
   */
  constructor() { }

  /**
   * 
   */
  getOrganization() {
    // in real life, API call happens here...
    let orgContact =
    {
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
      contact: {
        id: 123,
        firstName: "Mary",
        lastName: "Stephens",
        title: "CISO",
        phone: "208-716-2687",
        email: "MaryStephens@doe.gov"
      }
    };

    return orgContact;
  }

  getContactsForOrg() {
    let a = [
      {
        id: 123,
        name: "Mary Stephens"
      },{
        id: 127,
        name: "David Merrill"
      },{
        id: 141,
        name: "Dean Young"
      },{
        id: 98,
        name: "Ronald Clark"
      }
    ];
    return a;
  }
}
