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
    print("Step 1/3: create templates... (Skipping use template script...)")

    templates = json_data["template_data"]
    created_template_uuids = []
    for template in templates:
        resp = requests.post("http://localhost:8000/api/v1/templates/", json=template)
        rep_json = resp.json()
        created_template_uuids.append(rep_json["template_uuid"])

    print("created tempaltes_list: {}".format(created_template_uuids))
    print("Step 2/3: create targets...(Skipping)")
    # Currently Targets are not being creating into their own collections.
    created_targets_uuids = []

    print("created target_list: {}".format(created_targets_uuids))

    print("Step 3/3: create subscriptions...")

    subscriptions = json_data["subscription_data"]
    created_subcription_uuids = []

    for subscription in subscriptions:
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
