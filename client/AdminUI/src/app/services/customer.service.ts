import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Customer, Contact } from 'src/app/models/customer.model'

// Json Definition returned for Customer from API
const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  })
}

@Injectable()
export class CustomerService {
  private api = 'http://localhost:8010/proxy'

  constructor(private http: HttpClient) { }

  // Gets all Customers
  public getCustomers() {
    let url = `${this.api}/api/v1/customers/`;
    return this.http.get(url);
  }

  public setContacts(customer_uuid: string, contacts: Contact[]) {
    let data = {
      contact_list: contacts
    }

    return this.http.patch(`${this.api}/api/v1/customer/${customer_uuid}/`, JSON.stringify(data), httpOptions);
  }

  public patchCustomer(data: Customer) {
    return this.http.patch(`${this.api}/api/v1/customer/${data.customer_uuid}/`, data);
  }
}
