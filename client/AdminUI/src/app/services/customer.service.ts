import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ICustomer, IContact, ICustomerContact } from 'src/app/models/customer.model'
import { Observable } from 'rxjs';

// Json Definition returned for Customer from API


const headers = {
  'Content-Type': 'application/json'
}

@Injectable()
export class CustomerService {
  private api = 'http://localhost:8010/proxy'

  constructor(private http: HttpClient) { }

  public getCustomerContactList(customers: ICustomer[]): ICustomerContact[] {
    let customerContacts: ICustomerContact[] = [];
    console.log(customers[0]);
    console.log(customers);

    // customers.map(
    //   (customer: Customer) => {
    //     console.log(customer.contactList);
    //     customer.contactList.map(
    //       (contact: Contact) => {
    //         console.log(contact);
    //         let customerContact: ICustomerContact = {
    //           customerUuid: customer.uuid,
    //           customerName: customer.name,
    //           firstName: contact.firstName,
    //           lastName: contact.lastName,
    //           title: contact.title,
    //           phone: contact.phone,
    //           email: contact.email,
    //           notes: contact.notes
    //         }
    //         customerContacts.push(customerContact);
    //       }
    //     );
    //   }
    // );

    return customerContacts;
  }

  // Gets all Customers
  public getCustomers(): Observable<ICustomer[]> {
    let url = `${this.api}/api/v1/customers/`
    return this.http.get<ICustomer[]>(url, { headers });
  }

  public patchCustomer(data: ICustomer) {
    return this.http.patch(`${this.api}/api/v1/customer/${data.uuid}/`, data, { headers })
  }
}
