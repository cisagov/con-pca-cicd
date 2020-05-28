import { Contact } from './customer.model';


export class GoPhishCampaignsModel {

}

// Use Contact class  defined in customer.model
// export class SubscriptionContactModel{
//     first_name: string;
//     last_name: string;
//     office_phone: string;    
// }

export interface SubscriptionClicksModel {

}

export class Subscription {
    active: boolean;
    archived: boolean;
    customer_uuid: string;
    keywords: string;
    lub_timestamp: Date;
    name: string;
    primary_contact: Contact;
    start_date: Date;
    status: string;
    subscription_uuid: string;
    url: string;
    target_email_list: Target[] = [];

    /**
     * Converts a string with CSV lines into Targets.
     * Format: email, firstname, lastname, position
     * @param csv 
     */
    public setTargetsFromCSV(csv: string) {
        this.target_email_list = [];
        if (!csv) {
            return;
        }
        let lines = csv.split('\n');
        lines.forEach((line: string) => {
            let parts = line.split(',');
            if (parts.length == 4) {
                let t = new Target();
                t.email = parts[0].trim();
                t.first_name = parts[1].trim();
                t.last_name = parts[2].trim();
                t.position = parts[3].trim();
                this.target_email_list.push(t);
            }
        });
    }
}

/**
 * An individual being phished.
 */
export class Target {
    first_name: string;
    last_name: string;
    position: string;
    email: string;
}
