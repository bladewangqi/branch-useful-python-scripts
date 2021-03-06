# branch-useful-python-scripts
## Prerequisite

 1. Installed Python3 
 2. Installed requests module
How to install requests module:
`pip install requests`

## bulkCreate.py
### Use case
You want to bulk create branch links regarding to a link information CSV file using branch API
### How to use
`python3 bulkCreate.py`
### Note
In the sample script, assuming input CSV file only has one column which is referrerID, regarding to input CSV file you can modify the script to fulfill your requirement.

## bulkUpdate.py
### Use case
You have a CSV file including all the branch links you want to update, in that CSV file you could have columns for the data you want to update. You need to update all those links.
### How to use
`python3 bulkUpdate.py`
### Note
In the sample script, assuming input CSV file only has one column which is branch link url, regarding to input CSV file you can modify the script to fulfill your requirement. Please be aware based on WeWork wifi, the script can update 10,000 links per hour, so if you have lots of links to update, it won't be a super quick process.

## bulkDeleteFromDashboard.py
### Use case
You accidentally used CSV bulk create to create more than 1k quick links with same criteria(same campaign name, same feature, same channel...), cause for branch dashboard maximum you can load 500 links. You messed up with your dashboard you can't find the quick links you previously created. You want to delete all the accidentally created quick links from branch dashboard, and write all deleted links into a CSV file.
### How to use
There are a few values(not including typical branch key, secret..) you need to provide to run this script:
 - start_link_id (the start point of links you want to delete)
 - branch_app_id (app id you can get this value from branch dashboard)
 - cookie (cookie to load quick links from dashboard)
`python3 bulkDeleteFromDashboard.py`
#### How to get start_link_id & cookie
Go to branch dashboard -> Quick links then go the last page till you see "Load More" button.
Open your chrome debugger, filter Network transaction for https://branch.dashboard.branch.io/v1/link/marketing then you can see start_link_id & Cookie like below image.
![Image description](https://drive.google.com/open?id=1wiTgUzL3y45d1SnaM_6Hct6mfo8brpCM)
### Note
This script is pretty dangerous, since once you deleted a link there is no more for branch to recover the deletion, so please make sure you are aware what you are doing. Tips: provide very restrict matching criteria will help you to delete some links accidentally.
