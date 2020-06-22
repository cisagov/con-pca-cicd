"""
This is a stript to load tag data.

Here data is loaded via api call to test both api traffic
load and creation of data.

Steps to create:
loads in tag data from data/tags_info.json

sends to api

if tag does not exist, create, else ignore.

"""
# Standard Python Libraries
import json
import os

# Third-Party Libraries
import requests


def load_file(data_file):
    """This loads json file of tag data from filepath."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, data_file)
    with open(data_file, "r") as f:
        data = json.load(f)
    return data


def main():
    """This if the main def that runs creating data."""
    print("Step 1/1: loading tag data from tags_info.json ...")
    tags = load_file("data/tags_info.json")
    print("done loading data")
    for tag in tags:
        try:
            resp = requests.post("http://localhost:8000/api/v1/tags/", json=tag)
            status = resp.status_code
            if status == 400:
                resp_json = resp.json()
                if resp_json["error"] != "Tag already exists":
                    print(resp_json)
                    resp.raise_for_status()

        except requests.exceptions.HTTPError as err:
            raise err

    print("Finished Loading Tag data.")


if __name__ == "__main__":
    main()
