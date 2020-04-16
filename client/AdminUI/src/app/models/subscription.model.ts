import { Organization } from './organization.model';
export class GoPhishCampaignsModel{

}

export class SubscriptionContactModel{

}

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
    organization: string;
    start_date: Date;
    end_date: Date;
    report_count: number;
    gophish_campaign_list: GoPhishCampaignsModel[];
    first_report_timestamp: Date;
    primary_contact: SubscriptionContactModel;
    additional_contact_list: SubscriptionContactModel[];
    status: string;
    //target_email_list: string[];
    target_email_list: Target[] = [];
    click_list: SubscriptionClicksModel[];
    templates_selected: string[];
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
                t.firstName = parts[1].trim();
                t.lastName = parts[2].trim();
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
    firstName: string;
    lastName: string;
    position: string;
    email: string;
}
