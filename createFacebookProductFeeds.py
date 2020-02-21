# qi.wang@branch.io, this python script is just for Branch Metrics internal usage.
import requests
import csv
import urllib

# Source file's name
input_file_name = '[input file name]'
# File name of generated product feed links
output_file_name = '[output file name]]'
# Link domain for your Branch dashboard
link_domain = 'https://[link domain]'

input_file = open(input_file_name, "r")
reader = csv.DictReader(input_file, delimiter=',')

output_file = open(output_file_name, "w")
writer = csv.writer(output_file)

# Generate the query parameters string which doesn't need encode
def generateQueryStrings(dict):
    query_str = "&".join("%s=%s" % (k,v) for k,v in dict.items())
    return query_str


# Uncomment the next line if you want the script to skip the first line of the CSV
next(reader)

campaign_name = 'DPAtrial' # or {{campaign.name}} if you want this field to be populate by Facebook

# Loop through CSV
for row in reader:
    # pickup the product link
    target_link = row['link']
    # Query parameters which don't need to be encoded
    plain_params = {
    '$3p': 'a_facebook',
    '~ad_id': '{{ad.id}}',
    '~ad_name': '{{ad.name}}',
    '~ad_set_id': '{{adset.id}}',
    '~ad_set_name': '{{adset.name}}',
    '~campaign': campaign_name,
    '~campaign_id': '{{campaign.id}}',
    'utm_campaign': campaign_name,
    'utm_content': '{{ad.name}}',
    'feature': 'paid+advertising',
    'branch_ad_format': 'Product',
    'channel': 'Facebook'
    }
    # Query parameters which need to be encoded
    encoded_params = {
    '$fallback_method': 'app_wide',
    '$original_url': target_link,
    '$ios_deeplink_path': target_link,
    '$android_deeplink_path': target_link,
    '$fallback_url': target_link,
    '$canonical_url': target_link
    }

    encoded_str = urllib.parse.urlencode(encoded_params)
    plain_query_strs = generateQueryStrings(plain_params)
    long_link = link_domain + '?' + plain_query_strs + '&' + encoded_str

    # Write the long link into output_file
    print(long_link)
    writer.writerow([long_link])

input_file.close()
output_file.close()