# CON-PCA Data Dictionary

This document is the data dictionary for Con-PCA stored in a DocumentDB (MongoDB compatible) database. This information is organized by collection (table). Last updated: 10-03-2022

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
        - templates: list of [templates](#templates)
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

## Report

This collection contains aggregate statistics report data

## Sending Profile

This collection contains sending profile data

## Subscription

This collection contains top level subscription data

## Target

This collection contains phishing target data

## Template

This collection contains email template data
