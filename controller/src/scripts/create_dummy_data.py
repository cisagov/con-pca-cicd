"""
This is a stript to load dummy data.

Here data is loaded via api call to test both api traffic
load and creation of data.

Steps to create:
First create templates,
then create targets,
then add targets and templates to subscriptions.

ToDo: create delete script to get all uuid's of dummy data and delete.
"""
# Standard Python Libraries
from datetime import datetime
import json
import os


# Third-Party Libraries
import requests


def load_file(data_file):
    """This loads json file of dummy data from data/dummy_data.json."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, data_file)
    with open(data_file, "r") as f:
        data = json.load(f)
    return data

# def clean_up_first
#     """" drop the collections before starting to add data """
#      mongo_uri = "mongodb://{}:{}@{}:{}/".format(
#         settings.DB_CONFIG["DB_USER"],
#         settings.DB_CONFIG["DB_PW"],
#         settings.DB_CONFIG["DB_HOST"],
#         settings.DB_CONFIG["DB_PORT"],
#     )
#     client = MongoClient(mongo_uri)
#     db=client.admin
#     db.


def main():
    """This if the main def that runs creating data."""
    print("loading dummy json data")
    json_data = load_file("data/dummy_data.json")
    print("done loading data")
    print("Step 1/3: create templates...")

    email_templates = load_file("data/reformated_template_data.json")
    laning_page_tempalte = load_file("data/landing_pages.json")
    templates = email_templates + laning_page_tempalte
    created_template_uuids = []

    for template in templates:
        try:
            template["deception_score"] = template["complexity"]
            resp = requests.post(
                "http://localhost:8000/api/v1/templates/", json=template
            )
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err
        rep_json = resp.json()
        created_template_uuids.append(rep_json["template_uuid"])

    print("created templates_list: {}".format(created_template_uuids))

    print("Step 2/3: create customers...")

    customers = json_data["customer_data"]
    created_customer_uuids = []
    for customer in customers:
        try:
            resp = requests.post("http://localhost:8000/api/v1/customers/", json=customer)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err

        resp_json = resp.json()

        created_customer_uuid = resp_json["customer_uuid"]
        print("created customer_uuid: {}".format(created_customer_uuid))
        created_customer_uuids.append(created_customer_uuid)

    print("Step 3/3: create subscriptions...")

    subscriptions = json_data["subscription_data"]
    created_subcription_uuids = []

    for subscription in subscriptions:
        #print(subscription)
        # If testing data (identified by 'testing_customer'), get customer_uuid from db
        if "testing_customer_identifier" in subscription.keys():       
            existing_customers = requests.get("http://localhost:8000/api/v1/customers/")
            #print(existing_customers.json())
            if existing_customers:
                for customer in existing_customers.json():
                    if customer["identifier"] == subscription["testing_customer_identifier"]:
                        subscription["customer_uuid"] = customer["customer_uuid"]
                subscription.pop("testing_customer_identifier", None)

        try:
            resp = requests.post(
                "http://localhost:8000/api/v1/subscriptions/", json=subscription
            )
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err

        resp_json = resp.json()
        created_subcription_uuids.append(resp_json["subscription_uuid"])

    print("created subcription_list: {}".format(created_subcription_uuids))
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(
        current_dir,
        "data/created_dummy_data_{}.json".format(
            datetime.now().strftime("%Y_%m_%d_%H%M%S")
        ),
    )
    print("writing values to file: {}...".format(output_file))

    with open(output_file, "w") as outfile:
        data = {
            "created_customers": created_customer_uuids,
            "created_subcription_uuids": created_subcription_uuids,
            "created_template_uuids": created_template_uuids
        }
        json.dump(data, outfile, indent=2)
    print("Finished.....")


if __name__ == "__main__":
    main()
