import requests
import csv
import urllib
import json

# Constants
# Insert API key from the Branch dashboard **
branch_key = '[YOUR BRANCH KEY]'
branch_secret = '[YOUR BRANCH SECRET]'
# Branch endpoint for bulk delete from dashboard
load_links_end_point = "https://branch.dashboard.branch.io/v1/link/marketing"
# In the end display how many links you deleted
deleted_num = 0
# Once unmahc number exceeds below value stop deletion
stop_unmatch_num = 3
# How many links can't match delete critera so far
unmatch_num = 0
# The link id of your start point, int
start_link_id = 1234567890
# Branch app id, can find from your branch dashboard
branch_app_id = '[YOUR APP ID]'
# Cookie to successfully load your dashboard quick links
cookie = '[COOKIE ID FOUND BY CHROME DEBUGGER]'

output_file_name = '[YOUR DELETED LINKS OUTPOUT FILE].csv'
# Insert input & output filename for CSV containing the iformation, input file will be the fields you want to include for your generated links, output will include the links created and other information **
output_file = open(output_file_name, "w")
writer = csv.writer(output_file)

def bulkDeleteQuickLinks(jsonObject):
    global deleted_num
    global unmatch_num
    for element in jsonObject:
        url = element['url']
        # Matching criterias to do bulk delete
        if element.get('campaign', None) is not None:
            if element['campaign'] != 'share-with-friends':
                unmatch_num += 1
                continue
        if element.get('channel', None) is not None:
            if element['channel'] != 'Facebook':
                unmatch_num += 1
                continue
        if element.get('feature', None) is not None:
            if element['feature'] != 'share':
                unmatch_num += 1
                continue
        encoded_url = urllib.parse.quote_plus(url)
        delete_endpoint = 'https://api2.branch.io/v1/url?url=' + encoded_url
        delete_data = {
        'branch_key': branch_key,
        'branch_secret': branch_secret
        }
        payload = json.dumps(delete_data)
        delete_response_data = requests.delete(delete_endpoint, data=payload, verify=False)
        if delete_response_data.status_code != 200:
            print('Failed: delete link {}'.format(url))
        deleted_num += 1
        writer.writerow([url])

link_id = start_link_id
while unmatch_num < stop_unmatch_num:
    load_params = {'start': link_id}
    load_headers = {
    'x-app-id': branch_app_id,
    'Cookie': cookie
    }
    link_data = requests.get(load_links_end_point, params=load_params, headers=load_headers, verify=False)
    json_data = json.loads(link_data.text)

    if link_data.status_code != 200:
        print('Failed: load quick links start at {}'.format(link_id))
        break
    if len(json_data) == 0:
        break
    last_element = json_data[len(json_data)-1]
    link_id = int(last_element['id'])+1
    bulkDeleteQuickLinks(json_data)

print('Bulk delete {} quick links from dashboard finished!!!'.format(deleted_num))

output_file.close()