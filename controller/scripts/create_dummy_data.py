"""
This is a stript to load dummy data.

Here data is loaded via api call to test both api traffic
load and creation of data.

Steps to create:
First create templates,
then create targets,
then add targets and templates to subscriptions.

"""
# Standard Python Libraries
from datetime import datetime
import json
import os
import random

# Third-Party Libraries
import requests


def load_data():
    """This loads json file of dummy data from data/dummy_data.json."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, "data/dummy_data.json")
    with open(data_file, "r") as f:
        data = json.load(f)
    return data


def main():
    """This if the main def that runs creating data."""
    print("loading dummy json data")
    json_data = load_data()
    print("done loading data")
    print("Step 1/3: create templates...")

    templates = json_data["template_data"]
    created_template_uuids = []
    for template in templates:
        resp = requests.post("http://localhost:8000/api/v1/templates/", json=template)
        rep_json = resp.json()
        created_template_uuids.append(rep_json["template_uuid"])

    print("created tempaltes_list: {}".format(created_template_uuids))
    print("Step 2/3: create targets...")

    targets = json_data["target_data"]
    created_targets_uuids = []
    for target in targets:
        resp = requests.post("http://localhost:8000/api/v1/targets/", json=target)
        rep_json = resp.json()
        created_targets_uuids.append(rep_json["target_uuid"])

    print("created target_list: {}".format(created_targets_uuids))

    print("Step 3/3: create subscriptions...")

    subscriptions = json_data["subscription_data"]
    created_subcription_uuids = []
    secure_random = random.SystemRandom()
    target_1 = secure_random.choice(created_targets_uuids)
    target_2 = secure_random.choice(created_targets_uuids)

    gophish_campaign_list = {
        "template_email_uuid": created_template_uuids[1],
        "template_landing_page_uuid": created_template_uuids[0],
        "start_date": "2020-03-19T09:30:25",
        "end_date": "2020-03-29T00:00:00",
        "target_email_list": [
            {
                "target_uuid": target_1,
                "status": "sent",
                "sent_date": "2020-03-20T09:30:25",
            },
            {
                "target_uuid": target_2,
                "status": "sent",
                "sent_date": "2020-03-25T09:30:25",
            },
        ],
    }

    for subscription in subscriptions:
        subscription["templates_selected"] = created_template_uuids
        subscription["target_email_list"] = created_targets_uuids
        subscription["gophish_campaign_list"] = [gophish_campaign_list]
        resp = requests.post(
            "http://localhost:8000/api/v1/subscriptions/", json=subscription
        )
        rep_json = resp.json()
        created_subcription_uuids.append(rep_json["subscription_uuid"])

    print("created subcription_list: {}".format(created_subcription_uuids))
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(
        current_dir,
        "data/created_dummy_data_{}.json".format(
            datetime.now().strftime("%Y_%m_%d_%H%M%S")
        ),
    )
    print("writting values to file: {}...".format(output_file))

    with open(output_file, "w") as outfile:
        data = {
            "created_targets_uuids": created_targets_uuids,
            "created_subcription_uuids": created_subcription_uuids,
            "created_template_uuids": created_template_uuids,
        }
        json.dump(data, outfile, indent=2)
    print("Finished.....")


if __name__ == "__main__":
    main()
