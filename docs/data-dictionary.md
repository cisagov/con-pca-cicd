# CON-PCA Data Dictionary

This document is the data dictionary for Con-PCA stored in Mongo Atlas database cluster. This information is organized by collection (table). Last updated: 10-03-2022

## Collections

- [Customer](#customer)
- [Cycle](#cycle)
- [Landing Page](#landing-page)
- [Recommendation](#recommendation)
- [Report](#report)
- [Sending Profile](#sending-profile)
- [Subscription](#subscription)
- [Target](#target)
- [Template](#template)


## Customer

This collection contains customer data

- name: string
- identifier: string
- address_1: string
- address_2: string
- city: string
- zip_code: string
- customer_type: string = [Federal, State, Local Tribal, Private]
- contact_list: string
    - first_name: string
    - last_name: string
    - title: string
    - office_phone: phone
    - mobile_phone: phone
    - email: email
    - notes: string
    - active: boolean
- industry: string
- sector: string
- domain: url
- appendix_a_date: datetime
- archived: boolean
- archived_description = string

## Cycle

This collection contains cycle data. This data has a many to one relationship with subscription data.

- subscription_id: string
- template_ids: list of strings
- start_date: datetime
- end_date: datetime
- send_by_date: datetime
- active: boolean
- target_count: integer
- dirty_stats: boolean
- stats
    - stats
        - high
            - sent
                - count: integer
                - average: integer
                - ratio: integer
            - opened
                - count: integer
                - average: integer
                - ratio: integer
            - clicked
                - count: integer
                - average: integer
                - ratio: integer
            - reported
                - count: integer
                - average: integer
                - ratio: integer
        - moderate
            - sent
                - count: integer
                - average: integer
                - ratio: integer
            - opened
                - count: integer
                - average: integer
                - ratio: integer
            - clicked
                - count: integer
                - average: integer
                - ratio: integer
            - reported
                - count: integer
                - average: integer
                - ratio: integer
        - low
            - sent
                - count: integer
                - average: integer
                - ratio: integer
            - opened
                - count: integer
                - average: integer
                - ratio: integer
            - clicked
                - count: integer
                - average: integer
                - ratio: integer
            - reported
                - count: integer
                - average: integer
                - ratio: integer
        - all
            - sent
                - count: integer
                - average: integer
                - ratio: integer
            - opened
                - count: integer
                - average: integer
                - ratio: integer
            - clicked
                - count: integer
                - average: integer
                - ratio: integer
            - reported
                - count: integer
                - average: integer
                - ratio: integer
    - template_stats: list
        - template_id: strings
        - deception_level: strings
    - maxmind_stats: list
        - asn_org: strings
        - is_nonhuman: boolean
        - ips: list of strings
        - cities: list of strings
        - opens: integer
        - clicks: integer
    - indicator_stats: list
        - group: string
        - indicator: string
        - value: integer
        - label: string
    - recommendation_stats: list
        - recommendation: string
        - templates: list of [templates](#template)
    - time_stats: list
        - opened: list
            - one_minute
            - three_minutes
            - five_minutes
            - fifteen_minutes
            - thirty_minutes
            - sixty_minutes
            - two_hours
            - three_hours
            - four_hours
            - one_day
        - clicked: list
            - one_minute
            - three_minutes
            - five_minutes
            - fifteen_minutes
            - thirty_minutes
            - sixty_minutes
            - two_hours
            - three_hours
            - four_hours
            - one_day
    - all_customer_stats
        - high
            - sent
                - count: integer
                - average: integer
                - ratio: integer
            - opened
                - count: integer
                - average: integer
                - ratio: integer
            - clicked
                - count: integer
                - average: integer
                - ratio: integer
            - reported
                - count: integer
                - average: integer
                - ratio: integer
        - moderate
            - sent
                - count: integer
                - average: integer
                - ratio: integer
            - opened
                - count: integer
                - average: integer
                - ratio: integer
            - clicked
                - count: integer
                - average: integer
                - ratio: integer
            - reported
                - count: integer
                - average: integer
                - ratio: integer
        - low
            - sent
                - count: integer
                - average: integer
                - ratio: integer
            - opened
                - count: integer
                - average: integer
                - ratio: integer
            - clicked
                - count: integer
                - average: integer
                - ratio: integer
            - reported
                - count: integer
                - average: integer
                - ratio: integer
        - all
            - sent
                - count: integer
                - average: integer
                - ratio: integer
            - opened
                - count: integer
                - average: integer
                - ratio: integer
            - clicked
                - count: integer
                - average: integer
                - ratio: integer
            - reported
                - count: integer
                - average: integer
                - ratio: integer
    - deception_level_stats: list
        - deception_level: integer
        - sent_count: integer
        - unique_clicks: integer
        - total_clicks: integer
        - user_reports: integer
        - unique_user_clicks: list of integers
        - click_percentage_over_time: list of datetimes
    - target_stats
- phish_header: string
- manual_reports: list
    - email: string
    - report_date: datetime

## Landing Page

This collection contains data relating to landing pages.

- name: string
- is_default: boolean
- html: string

## Recommendation

This collection contains recommendation data

- title: string
- type: string = [sophisticated, red flag]
- description: string

## Report

This collection contains aggregate statistics report data

- customers_enrolled: integer
- customers_active: integer
- status_reports_sent: integer
- cycle_reports_sent: integer
- yearly_reports_sent: integer
- new_subscriptions: integer
- ongoing_subscriptions: integer
- stopped_subscriptions: integer
- federal_stats: list
    - subscription_count: integer
    - cycle_count: integer
    - emails_sent: integer
    - emails_clicked: integer
    - emails_clicked_ratio: float
- state_stats: list
    - subscription_count: integer
    - cycle_count: integer
    - emails_sent: integer
    - emails_clicked: integer
    - emails_clicked_ratio: float
- local_stats: list
    - subscription_count: integer
    - cycle_count: integer
    - emails_sent: integer
    - emails_clicked: integer
    - emails_clicked_ratio: float
- tribal_stats: list
    - subscription_count: integer
    - cycle_count: integer
    - emails_sent: integer
    - emails_clicked: integer
    - emails_clicked_ratio: float
- private_stats: list
    - subscription_count: integer
    - cycle_count: integer
    - emails_sent: integer
    - emails_clicked: integer
    - emails_clicked_ratio: float
- all_customer_stats: list
    - high
        - sent
            - count: integer
            - average: integer
            - ratio: integer
        - opened
            - count: integer
            - average: integer
            - ratio: integer
        - clicked
            - count: integer
            - average: integer
            - ratio: integer
        - reported
            - count: integer
            - average: integer
            - ratio: integer
    - moderate
        - sent
            - count: integer
            - average: integer
            - ratio: integer
        - opened
            - count: integer
            - average: integer
            - ratio: integer
        - clicked
            - count: integer
            - average: integer
            - ratio: integer
        - reported
            - count: integer
            - average: integer
            - ratio: integer
    - low
        - sent
            - count: integer
            - average: integer
            - ratio: integer
        - opened
            - count: integer
            - average: integer
            - ratio: integer
        - clicked
            - count: integer
            - average: integer
            - ratio: integer
        - reported
            - count: integer
            - average: integer
            - ratio: integer
    - all
        - sent
            - count: integer
            - average: integer
            - ratio: integer
        - opened
            - count: integer
            - average: integer
            - ratio: integer
        - clicked
            - count: integer
            - average: integer
            - ratio: integer
        - reported
            - count: integer
            - average: integer
            - ratio: integer

## Sending Profile

This collection contains sending profile data

- name: string
- interface_type: string = [SMTP, MAILGUN, SES]
- from_address: string
- sending_ips: string

- smtp_username: string
- smtp_password: string
- smtp_host: string

- mailgun_domain: string
- mailgun_api_key: string

- ses_role_arn: string

## Subscription

This collection contains top level subscription data

- name: string
- customer_id: string
- sending_profile_id: string
- target_domain: string
- start_date = DateTimeField()
- primary_contact: list of [customer](#customer) contacts
- admin_email: string
- operator_email: string
- status: string = [created, queued, running, stopped]
- target_email_list: list of [targets](#target)
- templates_selected: list of strings
- continuous_subscription: boolean
- buffer_time_minutes: integer
- cycle_length_minutes: integer
- cooldown_minutes: integer
- report_frequency_minutes: integer
- tasks: list
    - task_uuid: string
    - task_type: string
    - scheduled_date: datetime
    - executed: boolean
    - executed_date: datetime
    - error: string
- processing: boolean
- archived: boolean
- notification_history: list
    - message_type: string
    - sent: datetime
    - email_to: list of strings
    - emaiL_from: string
- phish_header: string
- reporting_password: string
- test_results: list
    - test_uuid: string
    - email: string
    - template: list of [templates](#template)
    - opened: boolean
    - clicked: boolean
    - timeline: list
        - time: datetime
        - message: string
        - details: string
    - error: string
- landing_page_id: string
- landing_domain: string
- landing_page_url: string

## Target

This collection contains phishing target data

- cycle_id: string
- subscription_id: string
- template_id: string
- email: email
- first_name: string
- last_name: string
- position: string
- deception_level: string = [low, moderate, high]
- deception_level_int: integer
- send_date: datetime
- sent: boolean
- sent_date: datetime
- error: string
- timeline: list
    - time: datetime
    - message: string
    - details: string

## Template

This collection contains email template data

- name: string
- landing_page_id: string
- sending_profile_id: string
- deception_score: integer (1-6)
- from_address: string
- retired: boolean
- retired_description: string
- sophisticated: list of strings
- red_flag: list of strings
- subject: string
- text: string
- html: string
- indicators
    - appearance
        - grammar: integer
        - link_domain: integer
        - logo_graphics: integer
    - sender
        - external: integer
        - internal: integer
        - authoritative: integer
    - relevancy
        - organization: integer
        - public_news: integer
    - behavior
        - fear: integer
        - duty_obligation: integer
        - curiosity: integer
        - greed: integer
