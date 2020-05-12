import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Customer, Contact, IApiCustomer, IApiContact, ICustomerContact } from 'src/app/models/customer.model'

// Json Definition returned for Customer from API


const headers = {
  'Content-Type': 'application/json'
}

@Injectable()
export class CustomerService {
  private api = 'http://localhost:8010/proxy'

  constructor(private http: HttpClient) { }

  public getCustomerContactList(customers: Customer[]): ICustomerContact[] {
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
  public getCustomers(): Customer[] {
    
    let results: Customer[] = []
    let url = `${this.api}/api/v1/customers/`

    this.http.get<IApiCustomer[]>(url, { headers }).subscribe(data => {
      data.map((item: IApiCustomer) => {
        results.push(this.customerJsonToObject(item))
      })
    })

    return results;
  }

  public patchCustomer(data: Customer) {
    return this.http.patch(`${this.api}/api/v1/customer/${data.uuid}/`, data, { headers })
  }

  private customerJsonToObject(item: IApiCustomer): Customer {
    let contacts: Contact[] = []
    
    item.contact_list.map(
      (contact: IApiContact) => {
        let o: Contact = this.contactJsonToObject(contact);
        contacts.push(o)
      }
    )

    let customer = new Customer();
    customer.uuid = item.customer_uuid;
    customer.name = item.name;
    customer.identifier = item.identifier;
    customer.address1 = item.address_1;
    customer.address2 = item.address_2;
    customer.city = item.city;
    customer.state = item.state;
    customer.zipCode = item.zip_code;
    customer.contactList = contacts;
    return customer;
  }

  private contactJsonToObject(item: IApiContact): Contact {
    let contact = new Contact();
    contact.firstName = item.first_name;
    contact.lastName = item.last_name;
    contact.title = item.title;
    contact.phone = item.phone;
    contact.email = item.email;
    contact.notes = item.notes;
    return contact;
  }
}
