import requests
import csv
import json

# Constants
# Insert API key from the Branch dashboard **
branch_key = '[YOUR BRANCH KEY]'
# Branch endpoint for bulk create
endpoint = "https://api2.branch.io/v1/url/bulk/"
# Batch number how many links to create per request
batchNum = 500
# file names
inputFileName = '[input file]'
outputFileName = '[output file]'

# Insert input & output filename for CSV containing the iformation, input file will be the fields you want to include for your generated links, output will include the links created and other information **
inputFile = open(inputFileName, "r")
outputFile = open(outputFileName, "w")

reader = csv.reader(inputFile, delimiter=',')
writer = csv.writer(outputFile)

# Uncomment the next line if you want the script to skip the first line of the CSV
# next(reader)

bulkCreateRequest = endpoint + branch_key

# Function to hit branch endpoint for bulk create
def bulkCreateHandler(jsonObject):
    batchLinkData = requests.post(bulkCreateRequest, json=jsonObject)
    # If request failed
    if batchLinkData.status_code != 200:
        firstElement = jsonObject[0]
        lastElement = jsonObject[len(jsonObject)-1]
        print('Failed: start from {} and end by {}'.format(firstElement, lastElement))
        return

    batchLinkJson = json.loads(batchLinkData.text)
    # Write link into output file
    for element in batchLinkJson:
        link = element['url']
        writer.writerow([link])

jsonBatch = []
num = 0
for row in reader:
    referrerID = row[0]
    # Json object for creating link
    jsonData = {
        "tags": [
            "referral"
        ],
        "campaign": "referral_campaign",
        "feature": "referrals",
        "channel": "web",
        "data": {
            "$marketing_title": "Referrals",
            "$og_description": "Refer your friends",
            "$fallback_url": "https://example.com",
            "$web_only": True,
            "$referrerID": referrerID,
            "$one_time_use": False,
        }
    }
    jsonBatch.append(jsonData)
    num += 1
    # Once reach batchNum, fire the reqeust
    if num >= batchNum:
        bulkCreateHandler(jsonBatch)
        # After fired request, reset num and jsonBatch
        num = 0
        jsonBatch = []

# Any json data left
if num > 0:
    bulkCreateHandler(jsonBatch)

print('Bulk create links finished!!!')

inputFile.close()
outputFile.close()