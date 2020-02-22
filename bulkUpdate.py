import requests
import csv
import urllib
import json

# Insert API key & App Secret from the Branch dashboard, and the Link data key you want to change in each link **
branch_key = "[YOUR BRANCH KEY]"
branch_secret = "[YOUR BRANCH SECRECT]"
file_name = '[CSV FILE NAME]'
# EndPoint
endpoint = "https://api2.branch.io/v1/url?url="

# Insert filename for CSV containing links to update in first column, and values to add in second column **
ifile = open(file_name, "r")

reader = csv.reader(ifile, delimiter=',')

# Uncomment the next line if you want the script to skip the first line of the CSV
next(reader)

# Loop through CSV
for row in reader:

    # Retrieve link data for link being updated
    # Assuming the input CSV file, first column is the link url to be updated
    url = urllib.parse.quote_plus(row[0])
    getrequest = endpoint + url + "&branch_key=" + branch_key
    linkdata = requests.get(getrequest)
    jsonData = json.loads(linkdata.text)

    if linkdata.status_code != 200:
        print('Failed: {}'.format( getrequest))
        continue

    # Set credentials for update API
    jsonData["branch_key"] = branch_key
    jsonData["branch_secret"] = branch_secret

    jsonData["data"]["$web_only"] = True
    jsonData["data"]["$fallback_url"] = "https://example.com"

    # for key_to_update in jsonData.get("data", "no_data"):
    #     # Update specified data key
    #     if key_to_update == "$web_only":
    #         # print jsonData["data"]["utm_campaign"]
    #         jsonData["data"]["$web_only"] = true
    #         # print jsonData["data"]["~campaign"]
    #         # del jsonData["data"]["utm_campaign"]

    #     if key_to_update == "$fallback_url":
    #         jsonData["data"]["$fallback_url"] = "https://zip.co/create-an-account"
            # del jsonData["data"]["utm_source"]

        # if key_to_update == "utm_medium":
        #     jsonData["data"]["~feature"] = jsonData["data"]["utm_medium"]
        #     del jsonData["data"]["utm_medium"]
    # Delete type & alias otherwise update request won't be successful
    if jsonData.get('type', None) is not None:
        del jsonData['type']
    if jsonData.get('alias', None):
        del jsonData['alias']
    payload = json.dumps(jsonData)
    putrequest = endpoint + url

    print(putrequest)
    print("\n")
    r = requests.put(putrequest, json=jsonData)

ifile.close()