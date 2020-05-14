"""Utils file for api."""
# Standard Python Libraries
from datetime import datetime, timedelta

# Third-Party Libraries
from database.service import Service
from django.conf import settings


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
    customer_full_address = "{} {} {} {} {}".format(
        customer_info["address_1"],
        customer_info["address_2"],
        customer_info["city"],
        customer_info["state"],
        customer_info["zip_code"],
    )
    check_replace = {
        "<%URL%>": "{{.URL}}",
        "<%TARGET_FIRST_NAME%>": "{{.FirstName}}",
        "<%TARGET_LAST_NAME%>": "{{.LastName}}",
        "<%TARGET_FULLL_NAME%>": "{{.FirstName}} {{.LastName}}",
        "<%TARGET_EMAIL%>": "{{.Email}}",
        "<%TARGET_POSITION%>": "{{.Position}}",
        "<%FROM%>": "{{.From}}",
        "<%CUSTOMER_NAME%>": customer_info["name"],
        "<%CUSTOMER_ADDRESS_FULL%>": customer_full_address,
        "<%CUSTOMER_ADDRESS_1%>": customer_info["address_1"],
        "<%CUSTOMER_ADDRESS_2%>": customer_info["address_2"],
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
    personalized_template_data = []
    for template in template_data:
        cleantext = template["html"]
        for key, value in check_replace.items():
            if value != None:
                cleantext = cleantext.replace(key, value)

        template_unique_name = "{}_{}_{}".format(
            "".join(template["name"].split(" ")),
            customer_info["customer_uuid"],
            today.strftime("%Y%m%d%H%M%S"),
        )

        personalized_template_data.append(
            {
                "template_uuid": template["template_uuid"],
                "data": cleantext,
                "name": template_unique_name,
            }
        )

    return personalized_template_data


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


def format_ztime(datetime_string):
    """
    Format Datetime.

    Coming from gophish, we get a datetime in a non-iso format,
    thus we need reformat to iso.
    """
    t = datetime.strptime(datetime_string.split(".")[0], "%Y-%m-%dT%H:%M:%S")
    t = t + timedelta(microseconds=int(datetime_string.split(".")[1][:-1]) / 1000)
    return t
