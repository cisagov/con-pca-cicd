import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Customer, Contact } from 'src/app/models/customer.model'
import { Observable } from 'rxjs';
import { type } from 'os';

// Json Definition returned for Customer from API

@Injectable()
export class CustomerService {
  private api = 'http://localhost:8010/proxy'

  constructor(private http: HttpClient) { }

  // Gets all Customers
  public getCustomers() {
    let url = `${this.api}/api/v1/customers/`;
    return this.http.get(url, { observe: 'body', responseType: 'json'});
  }

  public patchCustomer(data: Customer) {
    return this.http.patch(`${this.api}/api/v1/customer/${data.customer_uuid}/`, data);
  }
}
