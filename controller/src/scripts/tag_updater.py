"""
This a script to update all the old template tags.

It reads in a json file containing the old tags, replaces the tags with more uniform tags
and writes the results to a new file.
"""

import json
import sys

# Old tags that still need to be placed in categories for updated tags
#
#       ***DOMAIN TAGS***
#       DOMAIN
#       domain
#       [domain]
#       [DOMAIN]
#       [Spoofed Domain]
#       [SPOOFED_DOMAIN]
#       [UNIVERSITY-DOMAIN]
#       [NCATS_DOMAIN]
#       [NCATS DOMAIN]
#       [WRITTEN OUT SPOOFED CUSTOMER SURVEY DOMAIN]
#       [CUSTOMER-DOMAIN]
#
#       ***ACRONYM TAGS***
#       [Group Acronym]
#       [Acronym]
#       (Acronym)
#       [ACRONYM]
#       <Acronym>
#       <ACRONYM>
#       [GROUP ACRONYM]
#       [CUSTOMER ACRONYM]
#
#       ***SLOGAN TAGS***
#       [CUSTOMER SLOGAN]
#
#       ***SIGNATURE TAGS***
#       [Organization Signature]
#       [Signature]
#
#       ***TOPIC TAGS***
#       [TOPIC]
#
#       ***MISC/SPECIFIC TAGS***
#       [Related User Type]
#       [TimeCardProgram]
#       [CUST_SYSTEM]
#       [Actual Division that Handles Pay]
#       [LOGO]
#       [Related Budget/Finance Department]
#       [CUSTOMER-RELEVENT-JOB-ROLE]
#       [name of parks from opensource gathering]
#       <CUST_IT_Dept_NAME>
#       [System Name]
#       [County Election's Staff, Information Systems personnel across the State]
#       [CUSTOMER LEADERSHIP OFFICE]
#       [CUSTOMER EMAIL]
#       <ORG WEB PLATFORM/SERVICE>

old_target_name_tags = [
    "%To_Name%"
    "%To%"
]

old_from_tags: [

]

old_customer_tags = [
    "<ORG>",
    "<Customer Name>",
    "[CUSTOMER]",
    "[CUSTOMER LONG NAME]",
    "[CUSTOMER NAME]",
    "[Written Out Customer Name]",
    "[Customer]",
    "[CUSTOMER-NAME]",
    "[Customer Name]",
    "[CustomerName]",
    "[CUSTOMER_NAME]",
    "[Stakeholder Long Name]",
    "[Stakeholder]"
    "[UNIVERSITY_NAME]",
    "[AGENCY NAME]",
    "[Organization]",
    "[ORGANIZATION]",
    "[Organization Name]",
    "<CUST_NAME>"
    "[Organization Type]",
    "[ORG/CITY/TOWN/STATE]",
    "[CUSTOMER GROUP FOR PAYMENTS]",
    "[CUSTOMER SPECIFIC GROUP]"
]

old_address_tags = [
    "[Insert Address Here]",
    "[Location]",
    "[RELATED ADDRESS]",
    "[Related Org Address]"
]

old_date_tags = [
    "[DATE]",
    "[CAMPAIGN END DATE, YEAR]",
    "[Date of End of Campaign]",
    "[Date of Start of Campaign]",
    "[DATE AFTER CAMPAIGN]",
    "[Campaign End Date]",
    "[Date of Campaign End]",
    "[Insert Date]",
    "[Insert Date and Time]",
    "[RECENT DATE]",
    "[Upcoming Date]",
    "[MONTH YEAR]",
    "[MONTH DAY, YEAR]"
]

old_link_tags = [
    "<%URL%>",
    "<[%]URL[%]>",
    "<Spoofed Link>",
    "[Spoofed Related Site]",
    "<link>",
    "<Link>",
    "[<%URL%>]",
    "<spoofed link>",
    "<hidden link>",
    "<LINK TO ACTUAL CUST PAYMENT SITE OR SIMILAR>",
    "<[Fake link]>",
    "<HIDDEN>",
    "<HIDDEN LINK>",
    "<[EMBEDDED LINK]>",
    "<LINK>",
    "<embedded link>",
    "[LINK]",
    "[WRITTEN OUT SPOOFED CUSTOMER LINK]",
    "[EMBEDDED LINK]",
    "[Fake link]",
    "[insert spoofed link]",
    "[Insert Fake Link]",
    "[PLAUSIBLE SPOOFED URL]",
    "[insert fake URL]",
    "[spoof fake URL]",
    "[Related URL to State Law or Rule]",
    "[Fake Web Page URL]",
    "%URL%",
    "%]URL[%"
]

old_state_tags = [
    "[State]",
    "[State or Entity]",
    "[Entity or State]",
    "[Entity]",
    "[county or entity]",
]

old_season_tags = [
    "[Season]",
    "[Select Summer/Spring/Fall/Winter]"
]

old_customer_location_tags = [
    "[Customer Location, ex. Town of...]",
    "[Customer Location ex. Town of...]",
    "[Customer City]", "[CUST_LOCATION/NETWORK]",
    "<CITY/ORG NAME>",
    "[Location or Customer]",
    "[Customer Location]"
]

old_month_tags = [
    "[Month]",
    "[Month Year of Campaign]",
    "[MONTH]",
    "<Month>"
]

old_year_tags = [
    "<year>",
    "<Year>",
    "[CAMPAIGN END DATE, YEAR]",
    "[Year]",
    "[YEAR]"
]

old_spoof_name_tags = [
    "<FAKE NAME>",
    "[SPOOFED NAME]",
    "[NAME]",
    "[GENERIC FIRST NAME]",
    "[GENERIC NAME]",
    "[APPROVED HIGH LEVEL NAME]",
    "[Fake Name]",
    "[fakename]",
    "[MADE UP NAME]",
    "[FAKE NAME]"
]

old_event_tags = [
    "[list relevant weather event]"
]

old_time_frame_tags = [
    "[Change time frame as needed]"
]

# New Uniform Tags
#        "<%URL%>": "{{.URL}}",
#        "<%TARGET_FIRST_NAME%>": "{{.FirstName}}",
#        "<%TARGET_LAST_NAME%>": "{{.LastName}}",
#        "<%TARGET_FULLL_NAME%>": "{{.FirstName}} {{.LastName}}",
#        "<%TARGET_EMAIL%>": "{{.Email}}",
#        "<%TARGET_POSITION%>": "{{.Position}}",
#        "<%FROM%>": "{{.From}}",
#        "<%CUSTOMER_NAME%>": customer_info["name"],
#        "<%CUSTOMER_ADDRESS_FULL%>": customer_full_address,
#        "<%CUSTOMER_ADDRESS_1%>": customer_info["address_1"],
#        "<%CUSTOMER_ADDRESS_2%>": customer_info["address_2"],
#        "<%CUSTOMER_STATE%>": customer_info["state"],
#        "<%CUSTOMER_CITY%>": customer_info["city"],
#        "<%CUSTOMER_ZIPCODE%>": customer_info["zip_code"],
#        "<%CURRENT_SEASON%>": current_season(today),
#        "<%CURRENT_DATE_LONG%>": today.strftime("%B %d, %Y"),
#        "<%CURRENT_DATE_SHORT%>": today.strftime("%m/%d/%y"),
#        "<%CURRENT_MONTH_NUM%>": today.strftime("%m"),
#        "<%CURRENT_MONTH_LONG%>": today.strftime("%B"),
#        "<%CURRENT_MONTH_SHORT%>": today.strftime("%b"),
#        "<%CURRENT_YEAR_LONG%>": today.strftime("%Y"),
#        "<%CURRENT_YEAR_SHORT%>": today.strftime("%y"),
#        "<%CURRENT_DAY%>": today.strftime("%d"),
#        "<%SPOOF_NAME%>": "FAKE NAME GERNERATOR",
#        "<%EVENT%>": "Relevent Event",
#        "<%TIMEFRAME%>": "Relevent Timeframe",

def main():
    with open("data/template_old.json") as file:
        data = json.load(file)

    # Update tags in old template data file (template_old.json)
    for template in data:
        text = template['text']

        for tag in old_link_tags:
            text = text.replace(tag, "<%URL%>")

        for tag in old_target_name_tags:
            text = text.replace(tag, "<%TARGET_FULL_NAME%>")

        for tag in old_customer_tags:
            text = text.replace(tag, "<%CUSTOMER_NAME%>")

        for tag in old_address_tags:
            text = text.replace(tag, "<%CUSTOMER_ADDRESS_FULL%>")

        for tag in old_state_tags:
            text = text.replace(tag, "<%CUSTOMER_STATE%>")

        for tag in old_customer_location_tags:
            text = text.replace(tag, "<%CUSTOMER_CITY%>")

        for tag in old_season_tags:
            text = text.replace(tag, "<%CURRENT_SEASON%>")

        for tag in old_date_tags:
            text = text.replace(tag, "<%CURRENT_DATE_LONG%>")

        for tag in old_month_tags:
            text = text.replace(tag, "<%CURRENT_MONTH_LONG%>")

        for tag in old_year_tags:
            text = text.replace(tag, "<%CURRENT_YEAR_LONG%>")

        for tag in old_spoof_name_tags:
            text = text.replace(tag, "<%SPOOF_NAME%>")

        for tag in old_event_tags:
            text = text.replace(tag, "<%EVENT%>")

        for tag in old_time_frame_tags:
            text = text.replace(tag, "<%TIMEFRAME%>")

        template['text'] = text

    with open("data/template_updated_tags.json", "w") as file:
        json.dump(data, file, indent=2)


if __name__ == "__main__":
    main()
