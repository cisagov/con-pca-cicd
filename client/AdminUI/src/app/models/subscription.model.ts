import { Customer, Contact } from './customer.model';


export class GoPhishCampaignsModel{

}

// Use Contact class  defined in customer.model
// export class SubscriptionContactModel{
//     first_name: string;
//     last_name: string;
//     office_phone: string;    
// }

export interface SubscriptionClicksModel{

}

/**
 * The ongoing agreement to be phished.
 */
export class Subscription {
    //TODO: need to deal with the duplication 
    //From organization
    //organization_structure: Organization;
    startDate: Date;
    //orgKeywords: string[] = [];    

    subscription_uuid: string;    
    customer_uuid: string;
    name: string;
    //organization: string;
    start_date: Date;
    //end_date: Date;
    //report_count: number;
    gophish_campaign_list: GoPhishCampaignsModel[];
    //first_report_timestamp: Date;
    primary_contact: Contact;
    additional_contact_list: Contact[];
    status: string;
    //target_email_list: string[];
    target_email_list: Target[] = [];
    //click_list: SubscriptionClicksModel[];
    //templates_selected: string[];
    active: boolean;
    created_by: string
    cb_timestamp: Date;
    last_updated_by:string;
    lub_timestamp:Date;


    /**
     * 
     * @param csv 
     */
    setKeywordsFromCSV(csv: string) {
        //TODO: fix the api call to allow for these 
        //things
        // this.orgKeywords = [];

        // if (!csv) {
        //     return;
        // }

        // let lines = csv.split('\n');
        // lines.forEach((line: string) => {
        //     let words = line.split(',');
        //     words.forEach(w => {
        //         w = w.trim();
        //         if (w != '') {
        //             this.orgKeywords.push(w);
        //         }
        //     });
        // });
    }

    /**
     * Converts a string with CSV lines into Targets.
     * Format: email, firstname, lastname, position
     * @param csv 
     */
    setTargetsFromCSV(csv: string) {
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
