from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
import requests



client = MongoClient("mongodb://localhost:27017")
db=client["CISA_CPA"]
# Issue the serverStatus command and print the results

mycol = db["Campaigns"]

x = mycol.find_one()

print(x["created_date"])
#[name for name,thing in x.getmembers([])]
for y in x:
    print (y)    
    print ("\n")

f = open("importExamples/test.json","r")



#response = requests.get("https://127.0.0.1:3333/api/campaigns/?api_key=b4183824dad2f43a8479425181e6b9fbfe9777d0d48e113fee2e11c38703c2df", verify=False)
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'
steps = requests.post("https://127.0.0.1:3333/api/campaigns/?api_key=b4183824dad2f43a8479425181e6b9fbfe9777d0d48e113fee2e11c38703c2df",json=f.read(),headers)
f.close()