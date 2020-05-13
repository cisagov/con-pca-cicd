
/**
 * The subscribing organization/stakeholder.
 */
export class Customer {
    customer_uuid: number;
    name: string;
    identifier: string;
    address_1: string;
    address_2: string;
    city: string;
    state: string;
    zip_code: string;

    contact_list: Contact[];
}

/**
 * A point of contact within an Organization
 */
export class Contact {
    id: string;
    first_name: string;
    last_name: string;
    title: string;
    office_phone: string;
    mobile_phone: string;
    email: string;
    notes: string;

    /**
     * 
     */
    public get fullName() {
        return this.first_name + ' ' + this.last_name;
    }
}
