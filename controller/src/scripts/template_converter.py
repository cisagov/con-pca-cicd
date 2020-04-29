"""
Template Converter.

This script is to take in a json file of tempate data and parse it
into a usable json format for importing into cpa.

"""
# Standard Python Libraries
import getopt
import json
import os
import sys


def load_data(data_file):
    """This loads json file of data_file."""
    with open(data_file, "r") as f:
        data = json.load(f)
    return data


def main(argv):
    """This is the Main method of coverting the json file."""
    inputfile = ""
    outputfile = ""
    try:
        opts, _ = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print("template_converter.py -i <inputfile> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("template_converter.py -i <inputfile> -o <outputfile>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    print("Input file is: {}".format(inputfile))
    print("Output file is: {}".format(outputfile))
    """This if the main def that runs creating data."""
    print("loading {}".format(inputfile))
    print("file is here: {}".format(os.path.exists(inputfile)))
    json_data = load_data(inputfile)
    print("done loading data")
    output_list = []
    for temp in json_data:
        text = temp["text"]
        postString = text.split("\n", 2)
        if "From:" in postString[0]:
            message_from = postString[0].replace("From: ", "")
        if "Subject:" in postString[1]:
            message_subject = postString[1].replace("Subject: ", "")
        message_text = postString[2]
        new_format = {
            "name": temp["name"],
            "deception_score": 0,
            "descriptive_words": {},
            "description": temp["name"],
            "image_list": [],
            "from_address": message_from,
            "retired": False,
            "subject": message_subject,
            "text": message_text,
            "topic_list": [],
            "appearance": {
                "grammar": temp["appearance"]["grammar"],
                "link_domain": temp["appearance"]["link_domain"],
                "logo_graphics": temp["appearance"]["logo_graphics"],
            },
            "sender": {
                "external": temp["sender"]["external"],
                "internal": temp["sender"]["internal"],
                "authoritative": temp["sender"]["authoritative"],
            },
            "relevancy": {
                "organization": temp["relevancy"]["organization"],
                "public_news": temp["relevancy"]["public_news"],
            },
            "behavior": {
                "fear": temp["behavior"]["fear"],
                "duty_obligation": temp["behavior"]["duty_obligation"],
                "curiosity": temp["behavior"]["curiosity"],
                "greed": temp["behavior"]["greed"],
            },
            "complexity": temp["complexity"],
        }
        output_list.append(new_format)
        json_formatted_str = json.dumps(new_format, indent=2)
        print(json_formatted_str)
        print("--------")

    print(len(json_data))
    print(len(output_list))

    print("Now saving new json file...")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, "data/reformated_template_data.json",)
    print("writting values to file: {}...".format(output_file))

    with open(output_file, "w") as outfile:
        data = output_list
        json.dump(data, outfile, indent=2, sort_keys=True)
    print("Finished.....")


if __name__ == "__main__":
    main(sys.argv[1:])
