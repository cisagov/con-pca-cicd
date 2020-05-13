import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Customer, Contact, NewCustomer } from 'src/app/models/customer.model'
import { environment } from 'src/environments/environment';
import { Observable } from 'rxjs';

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
    requestData.map((x: any) => {
      let customer: Customer = {
        customer_uuid: x.customer_uuid,
        name: x.name,
        identifier: x.identifier,
        address_1: x.address_1,
        address_2: x.address_2,
        city: x.city,
        state: x.state,
        zip_code: x.zip_code,
        contact_list: []
      }
      customer.contact_list.map((y: any) => {
        let contact: Contact = {
          first_name: y.first_name,
          last_name: y.last_name,
          title: y.title,
          phone: y.phone,
          email: y.email,
          notes: y.notes
        }
        customer.contact_list.push(contact)
      })
      customers.push(customer)
    })
    return customers
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
