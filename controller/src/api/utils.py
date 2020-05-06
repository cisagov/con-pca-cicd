"""Utils file for api."""
from django.conf import settings
from datetime import date, datetime

# Third-Party Libraries
from database.service import Service


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
    relevent_info = {
        "current_date": current_date(), 
        "current_season": current_season(),
        "name": customer_info["name"],
        "city": customer_info["city"],
        "state": customer_info["state"],
        "zip": customer_info["zip"]
        }    
    print(relevent_info)

def current_date():
    today = datetime.today()
    return {
        "day": today.day,
        "month": today.month,
        "year": today.year
    }

def current_season():
    today = datetime.today()
    Y = today.year 
    seasons = [('winter', (datetime(Y,  1,  1),  datetime(Y,  3, 20))),
            ('spring', (datetime(Y,  3, 21),  datetime(Y,  6, 20))),
            ('summer', (datetime(Y,  6, 21),  datetime(Y,  9, 22))),
            ('autumn', (datetime(Y,  9, 23),  datetime(Y, 12, 20))),
            ('winter', (datetime(Y, 12, 21),  datetime(Y, 12, 31)))]

    now = datetime.today()
    return next(season for season, (start, end) in seasons
                if start <= now <= end)

