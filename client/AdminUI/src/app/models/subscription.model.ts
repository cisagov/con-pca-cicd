import { Contact } from './customer.model';
import * as moment from 'node_modules/moment/moment';

export class GoPhishCampaignModel {
  campaign_id: Number;
  completed_date?: Date;
  created_date: Date;
  email_template: string;
  groups: any[];
  landing_page_template: string;
  launch_date: Date;
  name: string;
  results: any[];
  send_by_date: Date;
  status: string;
  target_email_list: any[];
  timeline: CampaignTimelineItem[];
}

export class CampaignTimelineItem {
  email: string;
  time: Date;
  message: string;
  details: string;
}

// Use Contact class  defined in customer.model
// export class SubscriptionContactModel{
//     first_name: string;
//     last_name: string;
//     office_phone: string;
// }

export interface SubscriptionClicksModel {}

export class Subscription {
  active: boolean;
  archived: boolean;
  customer_uuid: string;
  keywords: string;
  lub_timestamp: Date;
  manually_stopped: boolean;
  name: string;
  primary_contact: Contact;
  start_date: Date;
  status: string;
  subscription_uuid: string;
  url: string;
  target_email_list: Target[] = [];
  gophish_campaign_list: GoPhishCampaignModel[];

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

/**
 * A point in time during the life of a subscription.
 */
export class TimelineItem {
  id?: number;

  // The font awesome class string to show above the timeline item
  icon: string;

  title: string;
  creatorName?: string = 'Joe';
  description?: string = 'Basic Description';
  buttonText?: string = 'Basic button text';
  date: moment.Moment;
}
