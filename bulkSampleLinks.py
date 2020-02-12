# Bulk links generate into csv file from bulk_link_creation_sample.csv
import csv
import json

# Define how many links you want to generate
numOfLinks = 100
with open('bulk_link_creation.csv', 'w') as csvfile:
	fieldnames = ['campaign', 'channel', 'feature', 'stage', 'tags', 'alias', 'data']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for i in range(numOfLinks):
		title = f"Share with Friends {i}"
		description = f"This is test {i}"
		alias = f"share-with-friends-{i}"
		tags = json.dumps(['tag1', 'tag2'])
		data = json.dumps({'$marketing_title': title, '$og_description': description})
		writer.writerow({'campaign': 'share-with-friends', 'channel': 'Facebook', 'feature': 'share', 'stage': 'home-page', 'tags': tags, 'alias': alias, 'data': data})