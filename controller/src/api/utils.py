"""Utils file for api."""
# Standard Python Libraries
from datetime import datetime
import json

# Third-Party Libraries
from database.service import Service
from django.conf import settings

CUSTOMER_PARAMS = {
    "customer_name": [
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
        "[UNIVERSITY_NAME]",
        "[AGENCY NAME]",
        "[Organization]",
        "[ORGANIZATION]",
        "[Organization Name]",
    ],
    "acronym": [
        "(ACRONYM)",
        "<Acronym>",
        "[ACRONYM]",
        "[GROUP ACRONYM]",
        "[Acronym]",
        "[Stakeholder Acronym]",
        "[CUSTOMER ACRONYM]",
    ],
    "city": [
        "[Location]",
        "[Location or Customer]",
        "[Insert location]",
        "[Customer Location, ex. Town of...]",
        "[Customer Location ex. Town of...]",
        "[CUST_LOCATION/NETWORK]",
    ],
    "state": ["[State]", "[State or Entity]", "[Entity or State]",],
    "date": [
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
        "[MONTH DAY, YEAR]",
    ],
    "year": ["<year>", "<Year>", "[CAMPAIGN END DATE, YEAR]", "[Year]", "[YEAR]"],
    "month": ["[Month]", "[Month Year of Campaign]", "[MONTH]", "<Month>"],
    "day": ["<day>"],
    "season": ["[Season]", "[Select Summer/Spring/Fall/Winter]",],
    "event": [
        "[list relevant weather event]",
        "[APPLICABLE EVENT]",
        "[CUSTOMER SPECIFIC EVENT]",
    ],
    "logo": ["[LOGO]"],
}

GOPHISH_PARAMS = {
    "link": [
        "<URL%>" "<[%]URL[%]>",
        "<%URL%>",
        "<Spoofed Link>",
        "<link>",
        "<Link>",
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
        "%]URL[%",
    ],
    "spoof_name": [
        "<FAKE NAME>",
        "[SPOOFED NAME]",
        "[NAME]",
        "[GENERIC FIRST NAME]",
        "[GENERIC NAME]",
        "[APPROVED HIGH LEVEL NAME]",
        "[Fake Name]",
        "[fakename]",
        "[MADE UP NAME]",
    ],
    "target": ["%To_Name%", "%To%",],
}


def db_service(collection_name, model, validate_model):
    """
    Db_service.

    This is a method for handling db connection in api.
    Might refactor this into database lib.
    """
    mongo_uri = "mongodb://{}:{}@{}:{}/".format(
        settings.DB_CONFIG["DB_USER"],
        settings.DB_CONFIG["DB_PW"],
        settings.DB_CONFIG["DB_HOST"],
        settings.DB_CONFIG["DB_PORT"],
    )

    service = Service(
        mongo_uri,
        collection_name=collection_name,
        model=model,
        model_validation=validate_model,
    )

    return service


def personalize_template(customer_info, template_data, sub_data):
    """
    Personalize Template.

    This takes costomer info, tempalte data and subscription data
    and genereates custom template text to use in gophosh.
    It also fills in GoPhish usable params.
    """
    today = datetime.today()
    check_replace = {
        "<%URL%>": "{{.URL}}",
        "<%TARGET_FIRST_NAME%>": "{{.FirstName}}",
        "<%TARGET_LAST_NAME%>": "{{.LastName}}",
        "<%TARGET_FULLL_NAME%>": "{{.FirstName}} {{.LastName}}",
        "<%TARGET_EMAIL%>": "{{.Email}}",
        "<%TARGET_POSITION%>": "{{.Position}}",
        "<%CUSTOMER_NAME%>": customer_info["name"],
        "<%CUSTOMER_ADDRESS%>": customer_info["name"],
        "<%CUSTOMER_STATE%>": customer_info["state"],
        "<%CUSTOMER_CITY%>": customer_info["city"],
        "<%CUSTOMER_ZIPCODE%>": customer_info["zip_code"],
        "<%CURRENT_SEASON%>": current_season(today),
        "<%CURRENT_DATE_LONG%>": today.strftime("%B %d, %Y"),
        "<%CURRENT_DATE_SHORT%>": today.strftime("%m/%d/%y"),
        "<%CURRENT_MONTH_NUM%>": today.strftime("%m"),
        "<%CURRENT_MONTH_LONG%>": today.strftime("%B"),
        "<%CURRENT_MONTH_SHORT%>": today.strftime("%b"),
        "<%CURRENT_YEAR_LONG%>": today.strftime("%Y"),
        "<%CURRENT_YEAR_SHORT%>": today.strftime("%y"),
        "<%CURRENT_DAY%>": today.strftime("%d"),
        "<%SPOOF_NAME%>": "FAKE NAME GERNERATOR",
        "<%EVENT%>": "Relevent Event",
        "<%TIMEFRAME%>": "Relevent Timeframe",
    }
    personalized_text = []
    for template in template_data:
        cleantext = template["html"]
        for check, rep in check_replace:
            cleantext = cleantext.replace(check, rep)

        personalized_text.append(
            {"template_uuid": template["template_uuid"], "personalized_text": cleantext}
        )

    print(json.dumps(personalized_text, indent=2, sort_keys=True))


def current_season(today):
    """
    Current Season.

    This returns the current season of given Date.
    """
    Y = today.year
    seasons = [
        ("winter", (datetime(Y, 1, 1), datetime(Y, 3, 20))),
        ("spring", (datetime(Y, 3, 21), datetime(Y, 6, 20))),
        ("summer", (datetime(Y, 6, 21), datetime(Y, 9, 22))),
        ("autumn", (datetime(Y, 9, 23), datetime(Y, 12, 20))),
        ("winter", (datetime(Y, 12, 21), datetime(Y, 12, 31))),
    ]
    return next(season for season, (start, end) in seasons if start <= today <= end)
