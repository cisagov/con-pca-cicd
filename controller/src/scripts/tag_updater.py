"""
This a script to update all the old template tags.

It reads in a json file containing the old tags, replaces the tags with more uniform tags
and writes the results to a new file.
"""

import json

with open("data/template_old.json") as file:
    data = json.load(file)

# Update tags in old template data file (template_old.json)
for template in data:
    text = template['text']
    print(text) # for easier reading while developing

    text = text.replace("[SPOOFED NAME]", "<%SPOOF_NAME%>")

    # replace all the old customer name tags
    text = text.replace("[CUSTOMER NAME]", "<%CUSTOMER_NAME%>")
    text = text.replace("[CUSTOMER_NAME]", "<%CUSTOMER_NAME%>")
    text = text.replace("[Customer Name]", "<%CUSTOMER_NAME%>")
    text = text.replace("[CustomerName]", "<%CUSTOMER_NAME%>")
    text = text.replace("[CUSTOMER-NAME]", "<%CUSTOMER_NAME%>")

    # replace all the old web page url tags
    text = text.replace("[Fake Web Page URL]", "<%URL%>")

    # replace all the old season tags
    text = text.replace("[Select Summer/Spring/Fall/Winter]", "<%CURRENT_SEASON%>")

    # replace all the old year tags
    text = text.replace("[YEAR]", "<%CURRENT_YEAR_LONG%>")

    template['text'] = text

with open("data/template_updated_tags.json", "w") as file:
    json.dump(data, file, indent=2)
