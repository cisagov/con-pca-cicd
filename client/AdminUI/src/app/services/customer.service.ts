import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Customer, Contact, NewCustomer, ICustomerContact } from 'src/app/models/customer.model'
import { environment } from 'src/environments/environment';
import { Observable } from 'rxjs';
import { request } from 'http';

// Json Definition returned for Customer from API
const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  })
}

@Injectable()
export class CustomerService {
  constructor(private http: HttpClient) { }

  // Returns observable on http request to get customers
  public requestGetCustomers() {
    let url = `${environment.apiEndpoint}/api/v1/customers/`;
    return this.http.get(url);
  }

  // Generates a list of Customer from request data
  public getCustomers(requestData: any[]): Customer[] {
    let customers: Customer[] = [];
    requestData.map((c: any) => {
      let customer = this.getCustomer(c)
      customers.push(customer)
    })
    return customers
  }

  public getAllContacts(customers: Customer[]): ICustomerContact[] {
    let customerContacts: ICustomerContact[] = []
    customers.map((customer: Customer) => {
      customer.contact_list.map((contact: Contact) => {
        let customerContact: ICustomerContact = {
          customer_uuid: customer.customer_uuid,
          customer_name: customer.name,
          first_name: contact.first_name,
          last_name: contact.last_name,
          title: contact.title,
          phone: contact.phone,
          email: contact.email,
          notes: contact.notes
        }
        customerContacts.push(customerContact)
      })
    })
    return customerContacts;
  }

  public requestGetCustomer(customer_uuid: string) {
    let url = `${environment.apiEndpoint}/api/v1/customer/${customer_uuid}/`;
    return this.http.get(url);
  }

  public getCustomer(requestData: any) {
    let customer: Customer = {
      customer_uuid: requestData.customer_uuid,
      name: requestData.name,
      identifier: requestData.identifier,
      address_1: requestData.address_1,
      address_2: requestData.address_2,
      city: requestData.city,
      state: requestData.state,
      zip_code: requestData.zip_code,
      contact_list: []
    }

    requestData.contact_list.map((c: any) => {
      let contact: Contact = {
        first_name: c.first_name,
        last_name: c.last_name,
        title: c.title,
        phone: c.phone,
        email: c.email,
        notes: c.notes
      }
      customer.contact_list.push(contact)
    })
    return customer
  }

  public setContacts(customer_uuid: string, contacts: Contact[]) {
    let data = {
      contact_list: contacts
    }

    return this.http.patch(`${environment.apiEndpoint}/api/v1/customer/${customer_uuid}/`, JSON.stringify(data), httpOptions);
  }

  public patchCustomer(data: Customer) {
    return this.http.patch(`${environment.apiEndpoint}/api/v1/customer/${data.customer_uuid}/`, data);
  }

  public addCustomer(customer: NewCustomer) {
    return this.http.post(`${environment.apiEndpoint}/api/v1/customers/`, JSON.stringify(customer), httpOptions);
  }
}
