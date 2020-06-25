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
import time

# Third-Party Libraries
import requests


def load_file(data_file):
    """This loads json file of dummy data from data/dummy_data.json."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, data_file)
    with open(data_file, "r") as f:
        data = json.load(f)
    return data


# def clean_up_first():
# """" drop the collections before starting to add data """
#  mongo_uri = "mongodb://{}:{}@{}:{}/".format(
#     settings.DB_CONFIG["DB_USER"],
#     settings.DB_CONFIG["DB_PW"],
#     settings.DB_CONFIG["DB_HOST"],
#     settings.DB_CONFIG["DB_PORT"],
# )
# client = MongoClient(mongo_uri)


def main():
    """This if the main def that runs creating data."""
    print("loading dummy json data")
    json_data = load_file("data/dummy_data.json")
    print("done loading data")
    print("Step 1/3: create templates...")

    email_templates = load_file("data/reformatted_template_data.json")
    landing_page_template = load_file("data/landing_pages.json")
    templates = email_templates + landing_page_template
    created_template_uuids = []

    existing_templates = requests.get("http://localhost:8000/api/v1/templates")

    if not existing_templates.json():
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
            if "error" in rep_json:
                print("Template Creation error: {}".format(rep_json))
            else:
                created_template_uuids.append(rep_json["template_uuid"])

    print("created templates_list: {}".format(created_template_uuids))

    print("Step 2/3: create customers...")

    customers = json_data["customer_data"]
    created_customer_uuids = []
    for customer in customers:
        try:
            resp = requests.post(
                "http://localhost:8000/api/v1/customers/", json=customer
            )
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err

        try:
            resp_json = resp.json()
            created_customer_uuid = resp_json["customer_uuid"]
            print("created customer_uuid: {}".format(created_customer_uuid))
            created_customer_uuids.append(created_customer_uuid)
        except Exception as err:
            print(err)
            pass

    print("Creating dhs contacts")
    dhs_contacts = json_data["dhs_contacts_data"]
    created_dhs_contacts_uuids = []
    for c in dhs_contacts:
        resp = requests.post("http://localhost:8000/api/v1/dhscontacts/", json=c)
        resp.raise_for_status()

        try:
            resp_json = resp.json()
            uuid = resp_json["dhs_contact_uuid"]
            print(f"created dhs contact uuid: {uuid}")
        except Exception as e:
            print(e)
            pass

        try:
            resp_json = resp.json()
            created_dhs_contact_uuid = resp_json["dhs_contact_uuid"]
            print("created customer_uuid: {}".format(created_dhs_contact_uuid))
            created_dhs_contacts_uuids.append(created_dhs_contact_uuid)
        except Exception as err:
            print(err)
            pass

    print("Step 3/3: create subscriptions...")

    subscriptions = json_data["subscription_data"]
    if not created_customer_uuids:
        print("customers already exist.. skipping")
        try:
            resp = requests.get("http://localhost:8000/api/v1/customers/")
            customers = resp.json()
            created_customer_uuids = [
                customer["customer_uuid"] for customer in customers
            ]
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err

    if not created_dhs_contacts_uuids:
        print("dhs contacts already exist.. skipping")
        try:
            resp = requests.get("http://localhost:8000/api/v1/dhscontacts/")
            dhs_contacts = resp.json()
            created_dhs_contacts_uuids = [
                contact["dhs_contact_uuid"] for contact in dhs_contacts
            ]
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err

    customer = created_customer_uuids[0]
    dhs_contact = created_dhs_contacts_uuids[0]
    created_subcription_uuids = []

    for subscription in subscriptions:
        subscription["customer_uuid"] = customer
        subscription["dhs_contact_uuid"] = dhs_contact
        subscription["start_date"] = datetime.today().strftime(
            "%Y-%m-%dT%H:%M:%S"
        )  # 2020-03-10T09:30:25"
        try:
            print(subscription)

            resp = requests.post(
                "http://localhost:8000/api/v1/subscriptions/", json=subscription
            )
            resp.raise_for_status()
            resp_json = resp.json()
            created_subcription_uuids.append(resp_json["subscription_uuid"])
        except requests.exceptions.HTTPError as err:
            print(err)

        time.sleep(5)

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
            "created_template_uuids": created_template_uuids,
        }
        json.dump(data, outfile, indent=2)
    print("Finished.....")


if __name__ == "__main__":
    main()
