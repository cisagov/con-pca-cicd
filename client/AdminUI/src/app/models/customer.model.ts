
 export class Customer {
    public uuid: string;
    public name: string;
    public identifier: string;
    public address1: string;
    public address2: string;
    public city: string;
    public state: string;
    public zipCode: string;
    public contactList: Contact[];
}

/**
 * A point of contact within an Organization
 */
export class Contact {
    public firstName: string;
    public lastName: string;
    public title: string;
    public phone: string;
    public email: string;
    public notes: string;
}

export interface IApiCustomer {
    customer_uuid: string,
    name: string,
    identifier: string,
    address_1: string,
    address_2: string,
    city: string,
    state: string,
    zip_code: string,
    contact_list: IApiContact[]
  }
  
  export interface IApiContact {
    first_name: string,
    last_name: string,
    title: string,
    phone: string,
    email: string,
    notes: string
  }

  export interface ICustomerContact {
      customerUuid: string,
      customerName: string,
      firstName: string,
      lastName: string,
      title: string,
      phone: string,
      email: string,
      notes: string,
  }