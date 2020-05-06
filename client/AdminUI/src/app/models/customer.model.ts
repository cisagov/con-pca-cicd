
/**
 * The subscribing organization/stakeholder.
 */
export class Customer {
    id: number;
    orgName: string;
    orgAbbrev: string;
    orgAddress1: string;
    orgAddress2: string;
    orgCity: string;
    orgState: string;
    orgZip: string;
    orgType: string;

    contacts: Contact[];
}

/**
 * A point of contact within an Organization
 */
export class Contact {
    id: string;
    firstName: string;
    lastName: string;
    title: string;
    phone: string;
    email: string;
    contactNotes: string;
}
