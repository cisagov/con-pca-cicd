export class Customer {
    customer_uuid: string;
    name: string;
    identifier: string;
    address_1: string;
    address_2: string;
    city: string;
    state: string;
    zip_code: string;
    contact_list: Contact[]
}

export class NewCustomer {
    name: string;
    identifier: string;
    address_1: string;
    address_2: string;
    city: string;
    state: string;
    zip_code: string;
    contact_list: Contact[]
}
  
export class Contact {
    first_name: string;
    last_name: string;
    title: string;
    office_phone: string;
    mobile_phone: string;
    email: string;
    notes: string;
    active: boolean;
}

export interface ICustomerContact {
    customer_uuid: string;
    customer_name: string;
    first_name: string;
    last_name: string;
    title: string;
    office_phone: string;
    mobile_phone: string;
    email: string;
    notes: string;
  }

