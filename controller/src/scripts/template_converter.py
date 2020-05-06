"""
Template Converter.

This script is to take in a json file of tempate data and parse it
into a usable json format for importing into pca.

"""
# Standard Python Libraries
import getopt
import json
import os
import re
import sys

# Third-Party Libraries
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def load_data(data_file):
    """This loads json file of data_file."""
    with open(data_file, "r") as f:
        data = json.load(f)
    return data


def main(argv):
    """This is the Main method of coverting the json file."""
    inputfile = ""
    try:
        opts, _ = getopt.getopt(argv, "hi:o:", ["ifile="])
    except getopt.GetoptError:
        print("template_converter.py -i <inputfile> ")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("template_converter.py -i <inputfile> ")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg

    print("Input file is: {}".format(inputfile))
    """This if the main def that runs creating data."""
    print("loading {}".format(inputfile))
    json_data = load_data(inputfile)
    print("done loading data")
    output_list = []
    stop_words = set(stopwords.words("english"))

    all_possible_tags = {
        "brackets": [],
        "glet": [],
        "percent": []
    }

    for temp in json_data:
        text = temp["text"]
        postString = text.split("\n", 2)
        if "From:" in postString[0]:
            message_from = postString[0].replace("From: ", "")
        if "Subject:" in postString[1]:
            message_subject = postString[1].replace("Subject: ", "")
        message_text = postString[2]
        message_html = "<br>".join(message_text.split("\n"))
        message_cleaned = " ".join(message_text.split("\n"))

        message_cleaned_more = re.sub(r"[^A-Za-z]+", " ", message_cleaned.lower())
        word_tokens = word_tokenize(message_cleaned_more)
        filtered_sentence = [w for w in word_tokens if w not in stop_words]
        descriptive_words = " ".join(filtered_sentence)
        # calc all old scores
        scores = []
        for  item in temp["appearance"]:
            scores.append(temp["appearance"][item])
        for  item in temp["sender"]:
            scores.append(temp["sender"][item])
        for  item in temp["relevancy"]:
            scores.append(temp["relevancy"][item])
        for  item in temp["behavior"]:
            scores.append(temp["behavior"][item])
        scores.append(temp["complexity"])

        bracket_tags = re.findall(r'\[.*?\]',message_cleaned)
        percent_tags = re.findall(r'\%.*?\%',message_cleaned)
        gtlt_tags = re.findall(r'\<.*?\>',message_cleaned)
        
        all_possible_tags["brackets"].extend(bracket_tags) 
        all_possible_tags["percent"].extend(percent_tags) 
        all_possible_tags["glet"].extend(gtlt_tags)

        template = {
            "name": temp["name"],
            "gophish_template_id": 0,
            "template_type": "Email",
            "deception_score": sum(scores),
            "descriptive_words": descriptive_words,
            "description": temp["name"],
            "image_list": [],
            "from_address": message_from,
            "retired": False,
            "subject": message_subject,
            "text": message_text,
            "html": message_html,
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
        output_list.append(template)

    print("Now compile all possble tags to parse...")
    all_possible_tags["brackets"] = list(dict.fromkeys(all_possible_tags["brackets"]))
    all_possible_tags["percent"] = list(dict.fromkeys(all_possible_tags["percent"]))
    all_possible_tags["glet"] = list(dict.fromkeys(all_possible_tags["glet"]))

    print("now walk over created templates in ../templetes/emails")
    current_dir = os.path.dirname(os.path.abspath(__file__)).rsplit("/", 1)[0]
    template_dir = os.path.join(current_dir, "templates/emails")
    for (_, _, filenames) in os.walk(template_dir):
        print(filenames)
        break

    for file in filenames:
        template_file = os.path.join(template_dir, file)
        with open(template_file, "r") as f:
            html_string = f.read()
            soup = BeautifulSoup(html_string, "html.parser")
            cleantext = re.sub(r"[^A-Za-z]+", " ", soup.get_text().lower())

            word_tokens = word_tokenize(cleantext)
            filtered_sentence = [w for w in word_tokens if w not in stop_words]
            descriptive_words = " ".join(filtered_sentence)

            template_name = file.split(".")[0]
            template = {
                "name": template_name,
                "gophish_template_id": 0,
                "template_type": "Email",
                "deception_score": 0,
                "descriptive_words": descriptive_words,
                "description": "GoPhish formated {}".format(file),
                "image_list": [],
                "from_address": "",
                "retired": False,
                "subject": "",
                "text": "",
                "html": html_string,
                "topic_list": [],
                "appearance": {"grammar": 0, "link_domain": 0, "logo_graphics": 0},
                "sender": {"external": 0, "internal": 0, "authoritative": 0},
                "relevancy": {"organization": 0, "public_news": 0},
                "behavior": {
                    "fear": 0,
                    "duty_obligation": 0,
                    "curiosity": 0,
                    "greed": 0,
                },
                "complexity": 0,
            }
        output_list.append(template)

    print("Now saving new json file...")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, "data/reformated_template_data.json",)
    tag_file = os.path.join(current_dir, "data/tag_file.json",)

    print("writting values to file: {}...".format(output_file))

    with open(tag_file, "w") as outfile:
        json.dump(all_possible_tags, outfile, indent=2, sort_keys=True)
    print("Finished tagfile.....")

    with open(output_file, "w") as outfile:
        data = output_list
        json.dump(data, outfile, indent=2, sort_keys=True)
    print("Finished.....")


if __name__ == "__main__":
    main(sys.argv[1:])
