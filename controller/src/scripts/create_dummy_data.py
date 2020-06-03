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

    print("Step 3/3: create subscriptions...")

    subscriptions = json_data["subscription_data"]
    customer = created_customer_uuids[0]
    created_subcription_uuids = []

    for subscription in subscriptions:
        subscription["customer_uuid"] = customer
        subscription["start_date"] = datetime.today()
        try:
            resp = requests.post(
                "http://localhost:8000/api/v1/subscriptions/", json=subscription
            )
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
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
            "created_template_uuids": created_template_uuids,
        }
        json.dump(data, outfile, indent=2)
    print("Finished.....")


if __name__ == "__main__":
    main()
