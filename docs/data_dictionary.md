# CON-PCA Data Dictionary

This document is the data dictionary for Con-PCA stored in a MongoDB database. This information is organized by collection (table).

## Collections

- [_campaign_ Collection](#_campaign_)
- [_customer_ Collection](#_customer_)
- [_dhs_contact_ Collection](#_dhs_contact_)
- [_landing_page_ Collection](#_landing_page_)
- [_recommendations_ Collection](#_recommendations_)
- [_subscription_ Collection](#_subscription_)
- [_tag_definition_ Collection](#_tag_definition_)
- [_target_ Collection](#_target_)
- [_template_ Collection](#_template_)

### _campaign_

This collection contains campaigns that are associated with a cycle within a subscription. A cycle can have up to 15 campaigns. A campaign is GoPhish terminology. For more info see the [GoPhish documentation](https://docs.getgophish.com/user-guide/documentation/campaigns).

- campaign_uuid [*UUID*]: Application produced UUID for a campaign.
- subscription_uuid [*UUID*]: Subscription that a campaign belongs to.
- cycle_uuid [*UUID*]: Which cycle within a subscription the campaign belongs to.
- name [*String*]: The application produced name for the campaign.
- created_date [*DateTime*]: The date the campaign was created in GoPhish.
- launch_date [*DateTime*]: The date the campaign was launched in GoPhish.
- send_by_date [*DateTime*]: The date all phishing emails need to be sent by for a campaign.
- completed_date [*DateTime*]: The date that the campaign has been stopped/completed.
- email_template [*String*]: The name of the email template that is attached to the campaign.
- email_template_id [*Integer*]: The id from GoPhish of the email template attached to the campaign.
- template_uuid [*UUID*]: The template UUID that's attached to the campaign.
- deception_level [*Integer*]: The deception level of a given campaign. Ranges from 1 to 3 with 3 being the highest.
- landing_page_template [*String*]: The name of the landing page associated with the campaign.
- status [*String*]: The current status of the campaign from GoPhish.
- results [*List(Dictionary)*]: Phishing results for individual targets within a campaign.
  - id [*Integer*]: The id of the result in GoPhish.
  - first_name [*String*]: The first name of the target.
  - last_name [*String*]: The last name of the target.
  - position [*String*]: The job position of the target.
  - status [*String*]: The status of the target being phished. Given by GoPhish.
  - ip [*String*]: The IP address of the target.
  - latitude [*Float*]: The latitude of the target.
  - longitude [*Float*]: The longitude of the target.
  - send_date [*DateTime*]: The date the target was sent a phish.
  - reported [*Boolean*]: Whether the target reported the email.
- phish_results [*Dictionary*]: Overall phishing results for a campaign.
  - sent [*Integer*]: The amount of emails sent for a campaign.
  - opened [*Integer*]: The amount of emails opened for a campaign.
  - clicked [*Integer*]: The amount of links clicked in a campaign.
  - submitted [*Integer*]: The amount of user that submitted data in a campaign.
  - reported [*Integer*]: The amount of phishing emails reported in a campaign.
- phish_results_dirty [*Boolean*]: A boolean that states whether phish results need to be reproduced when statistics are queried.
- groups [*List(Dictionary)]: GoPhish groups of targets associated with a campaign.
  - id [*Integer*]: ID of group in GoPhish.
  - name [*String*]: Name of the group in GoPhish.
  - targets [*List(Dictionary)*]: Targets in a group.
    - first_name [*String*]: First name of the target.
    - last_name [*String*]: Last name of the target.
    - position [*String*]: Job position of the target.
    - email [*String*]: Email of the target.
  - modified_date [*DateTime*]: Date group was modified in GoPhish.
- timeline [*List(Dictionary)*]: The timeline of events that happen in a campaign.
  - email [*String*]: The email address for the timeline event.
  - time [*DateTime*]: The time that the event occured.
  - message [*String*]: The name of the event that occured (ex. Email Opened, Email Sent)
  - details [*String*]: Additional details about the event that occured.
  - duplicate [*Boolean*]: Whether the event already exists.
- target_email_list [*List(Dictionary)*]
  - first_name [*String*]: First name of the target.
  - last_name [*String*]: Last name of the target.
  - position [*String*]: Job position of the target.
  - email [*String*]: Email of the target.
- smtp [*Dictionary*]
  - id [*Integer*]: The id in Gophish of the sending profile.
  - name [*String*]: The name in Gophish of the sending profile.
  - host [*String*]: The hostname for the sending profile.
  - interface_type [*String*]: The interface type for the sending profile (SMTP).
  - from_address [*String*]: The from address for the sending profile.
  - ignore_cert_errors [*Boolean*]: Whether to ignore cert errors when communicating with the server.
  - modified_date [*DateTime*]: The time that the sending profile was last modified in GoPhish.
  - headers [*List(Dictionary)*]: The email headers associated with a sending profile.
    - key [*String*]: The key of the email header.
    - value [*String*]: The value of the email header.

### _customer_

This is information about a customer that will be signed up for a subscription.

- customer_uuid [*UUID*]: The application produced UUID for a customer.
- name [*String*]: The name of the customer.
- identifier [*String*]: The shortened identifier for a customer.
- address_1 [*String*]: Address field for a customer.
- address_2 [*String*]: Address field for a customer.
- city [*String*]: City for a customer.
- state [*String*]: State of a customer.
- zip_code [*String*]: The zip code for the customer.
- customer_type [*String*]: The type of customer (Fed, state, local, tribal, private).
- contact_list [*List(Dictionary)*]: List of contacts for a customer.
  - first_name [*String*]: First name of the contact.
  - last_name [*String*]: Last name of the contact.
  - title [*String*]: Title of the contact.
  - office_phone [*String*]: The office phone number of the contact.
  - mobile_phone [*String*]: The mobile phone number of the contact.
  - email [*String*]: The email of the contact.
  - notes [*String*]: Additional notes for the contact.
  - active [*Boolean*]: Whether the contact is currently active.
- sector [*String*]: The sector of the customer.
- industry [*String*]: The industry of the customer.

### _dhs_contact_

This is a contact within DHS that will be bcc'd on reporting emails.

- dhs_contact_uuid [*UUID*]: The uuid of the DHS Contact.
- first_name [*String*]: The first name of the DHS Contact.
- last_name [*String*]: The last name of the DHS Contact.
- title [*String*]: The title of the DHS Contact.
- office_phone [*String*]: The office phone number of the DHS Contact.
- mobile_phone [*String*]: The mobile phone number of the DHS Contact.
- email [*String*]: The email address of the DHS Contact.
- notes [*String*]: Additional notes for the DHS Contact.
- active [*String*]: Whether the DHS Contact is currently active.

### _landing_page_

This is the page that a target will land on after clicking a link. For more information read up on the [GoPhish Documentation](https://docs.getgophish.com/user-guide/documentation/landing-pages).

- landing_page_uuid [*UUID*]: The uuid of the landing page.
- gophish_template_id [*Integer*]: The GoPhish id of the landing page.
- name [*String*]: The name of the landing page.
- is_default_template [*Boolean*]: Whether the landing page is the default page for campaigns.
- html [*String*]: The HTML for the landing page.

### _recommendations_

This collection is needing changes, and so the fields are not going to be listed until all the new requirements have been established for recommendations.

### _subscription_

This is the collection that contains subscriptions. Within a subscription there is linking information to what customer is associated with the subscription, the tasks in a subscription and cycles in a subscription. A cycle is a period of time in which phishing emails are sent out.

- subscription_uuid [*UUID*]: The UUID of the subscription.
- customer_uuid [*UUID*]: The UUID of the customer associated with the subscription.
- tasks [*List(Dictionary)*]: A list of tasks for the subscription.
  - task_uuid [*UUID*]: The UUID of the task.
  - message_type [*String*]: The task to execute.
  - scheduled_date [*DateTime*]: When to execute the task.
  - queued [*Boolean*]: Whether the task has been sent to the SQS queue for processing.
  - executed [*Boolean*]: Whether the task has been executed successfully.
  - executed_date [*DateTime*]: When the task was executed successfully.
  - error [*String*]: The error if the task executed with failure.
- name [*String*]: The name of the subscription.
- url [*String*]: The customer URL associated with a subscription.
- target_domain [*String*]: The domains that all target emails have to be in.
- keywords [*String*]: Words associated with the subscription and customer.
- start_date [*DateTime*]: The start date of the subscription.
- end_date [*DateTime*]: The date the subscription ended.
- primary_contact [*Dictionary*]: The customer primary contact assocated with the subscription.
  - first_name [*String*]: First name of the contact.
  - last_name [*String*]: Last name of the contact.
  - title [*String*]: Title of the contact.
  - office_phone [*String*]: The office phone number of the contact.
  - mobile_phone [*String*]: The mobile phone number of the contact.
  - email [*String*]: The email of the contact.
  - notes [*String*]: Additional notes for the contact.
  - active [*Boolean*]: Whether the contact is currently active.
- dhs_contact_uuid [*UUID*]: The UUID of the DHS Contact.
- status [*String*]: The status of the subscription (Queued, In Progress, Stopped).
- target_email_list [*List(Dictionary)*]: List of targets for the subscription.
  - first_name [*String*]: First name of the target.
  - last_name [*String*]: Last name of the target.
  - position [*String*]: Job position of the target.
  - email [*String*]: Email of the target.
- target_email_list_cached_copy [*List(Dictionary)*]: Copy of the target email list so to change targets for next running cycle.
  - first_name [*String*]: First name of the target.
  - last_name [*String*]: Last name of the target.
  - position [*String*]: Job position of the target.
  - email [*String*]: Email of the target.
- templates_selected_uuid_list [*List(UUID)*]: list of UUIDs of templates used in the subscription.
- sending_profile_name [*String*]: Name of sending profile used in the subscription.
- active [*Boolean*]: Whether the subscription is currently active/running.
- archived [*Boolean*]: Whether the subscription is archived.
- manually_stopped [*Boolean*]: Whether the subscription was manually stopped on the frontend.
- cycles [*List(Dictionary)*]: A list of cycles in a subscription.
  - cycle_uuid [*UUID*]: The UUID for the cycle.
  - start_date [*DateTime*]: The start date of the cycle.
  - end_date [*DateTime*]: The end date of the cycle.
  - active [*Boolean*]: Whether the cycle is currently active.
  - campaigns_in_cycle [*List(Integer)*]: The of GoPhish campaign ids of campaigns in the cycle.
  - phish_results [*Dictionary*]: Phishing results of the cycle.
    - sent [*Integer*]: The amount of emails sent for a campaign.
    - opened [*Integer*]: The amount of emails opened for a campaign.
    - clicked [*Integer*]: The amount of links clicked in a campaign.
    - submitted [*Integer*]: The amount of user that submitted data in a campaign.
    - reported [*Integer*]: The amount of phishing emails reported in a campaign.
  - phish_results_dirty [*Boolean*]: Whether the phish results need to be recalculated on the next pull.
  - override_total_reported [*Integer*]: The number of reported phishing emails to report for the cycle.
  - total_targets [*Integer*]: The total number of targets enrolled in the cycle.
- email_report_history [*List(Dictionary)*]: The history of reports sent out in a subscription.
  - report_type [*String*]: The type of report sent (monthly, cycle, etc.).
  - sent [*DateTime*]: The time when the report was sent.
  - email_to [*String*]: The email the report was sent to.
  - email_from [*String*]: The email the report was sent from.
  - bcc [*String*]: The email that was bcc'd on the report.
  - manual [*Boolean*]: Whether the report was sent manually from the front end.
- stagger_emails [*Boolean*]: Whether the initial campaigns in a subscription should be staggered by an hour.
- continuous_subscription [*Boolean*]: Whether to continue the subscription after the current running cycle.

### _tag_definition_

Tags are substitutions that happen in phishing emails that are sent out to targets.

- tag_definition_uuid [*UUID*]: The UUID of the tag.
- tag [*String*]: The name of the tag (<%TAG_NAME%>).
- description [*String*]: The description of the tag.
- data_source [*String*]: The data source of the tag (faker, customer, etc.).
- tag_type [*String*]: How to generate the tag (eval, literal, gophish).

### _target_

This collection is a history of all the templates that are sent to a target, so the same target doesn't get duplicate phishes each cycle.

- target_uuid [*UUID*]: The UUID of the target.
- email [*String*]: The email of the target.
- history_list [*List(Dictionary)*]: The history of templates sent to a target.
  - template_uuid [*UUID*]: The UUID of the template sent.
  - sent_timestamp [*DateTime*]: The time the template was sent to the target.

### _template_

This collection contains the phishing templates that are sent out to targets. For more information, read up on the [GoPhish Documentation](https://docs.getgophish.com/user-guide/documentation/templates).

- template_uuid [*UUID*]: The UUID of the template.
- name [*String*]: The name of the template.
- landing_page_uuid [*UUID*]: The UUID of the landing page associated with a template.
- deception_score [*Integer*]: The deception score given to a template.
- descriptive_words [*String*]: Descriptive words associated with the template.
- description [*String*]: The template description.
- from_address [*String*]: The display name and sender for the template.
- retired [*Boolean*]: Whether the template is retired and should not be used in future subscriptions.
- retired_description [*String*]: Why the template has been retired.
- subject [*String*]: The email subject for the template.
- text [*String*]: The text attributes for the email.
- html [*String*]: The html for the email.
- appearance [*Dictionary*]: The scores for the appearance section of the template.
  - grammar [*Integer*]: The score for grammar.
  - link_domain [*Integer*]: The score for link_domain.
  - logo_graphics [*Integer*]: The score for logo_graphics.
- sender [*Dictionary*]: The scores for the sender section of the template.
  - external [*Integer*]: Score for an external sender.
  - internal [*Integer*]: Score for an internal sender.
  - authoritative [*Integer*]: Score for authoritative sender.
- relevancy [*Dictionary*]: Scores for relevancy section of the template.
  - organization [*Integer*]: Score for organization.
  - public_news [*Integer*]: Score for public_news.
- behavior [*Dictionary*]: Scores for behavior section of the template.
  - fear [*Integer*]: Score for fear.
  - duty_obligation [*Integer*]: Score for duty_obligation.
  - curiosity [*Integer*]: Score for curiosity.
  - greed [*Integer*]: Score for greed.
