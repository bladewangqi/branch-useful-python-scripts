import requests
import csv
import urllib
import json

# Constants
# Insert API key from the Branch dashboard **
branch_key = 'key_live_hbSHp4Ukk6L07eE9sRSTYjdkwAcDbpoG'
branch_secret = 'secret_live_mgJEGlwjgt7Or6R8mRd1uoSi1XTAKTyW'
# Branch endpoint for bulk delete from dashboard
load_links_end_point = "https://branch.dashboard.branch.io/v1/link/marketing"
deleted_num = 0
stop_unmatch_num = 3
unmatch_num = 0

start_link_id = 748320410454022603

output_file_name = 'deleted_links.csv'
# Insert input & output filename for CSV containing the iformation, input file will be the fields you want to include for your generated links, output will include the links created and other information **
output_file = open(output_file_name, "w")
writer = csv.writer(output_file)

def bulkDeleteQuickLinks(jsonObject):
    global deleted_num
    global unmatch_num
    for element in jsonObject:
        url = element['url']
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
    'x-app-id': '736404266750595330',
    'Cookie': '_ga=GA1.2.1018144627.1575933178; _fbp=fb.1.1575933179700.1108143412; cto_lwid=31be3188-6cd1-4493-ab0e-e7bc01e44db7; _mkto_trk=id:315-FTT-121&token:_mch-branch.io-1575998659565-86947; _biz_uid=fc70209c13e1447aecaafa8bd69aced5; ajs_group_id=null; ajs_anonymous_id=%22f8b666aa-b97b-414a-99fe-05484eb3258c%22; bnc_returning_visitor=1; _biz_flagsA=%7B%22Version%22%3A1%2C%22XDomain%22%3A%221%22%2C%22Mkto%22%3A%221%22%7D; _gcl_au=1.1.1808704966.1580265675; _gcl_aw=GCL.1580426969.EAIaIQobChMIkr24nL2s5wIVDhWPCh21pA8_EAAYASAAEgLeWfD_BwE; _gac_UA-53307642-1=1.1580426969.EAIaIQobChMIkr24nL2s5wIVDhWPCh21pA8_EAAYASAAEgLeWfD_BwE; dashboard_external_referrer=; _gid=GA1.2.734348532.1581332790; ei_client_id=5e426c779e5bf50010b5816c; _csrf=H4-8rwDKQEF4PMTjM0cohCOj; branch.domain=branch; mp_47ec8ea9ac102b1370221dcda476091c_mixpanel=%7B%22distinct_id%22%3A%20%2217031768c08f58-03a24638a58467-39637b0f-1ea000-17031768c09ee0%22%2C%22%24device_id%22%3A%20%2217031768c08f58-03a24638a58467-39637b0f-1ea000-17031768c09ee0%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22%24search_engine%22%3A%20%22google%22%7D; _biz_nA=81; _biz_pendingA=%5B%5D; branch.id=23898697-2834-47D4-BA71-E7F031A4DB6B; dash_oauth_state=84fefa6925c5aa78016499ff37853f4a27278353559e10fc52; mp_fe56094950973706fe3ca9d10adc2586_mixpanel=%7B%22distinct_id%22%3A%20%22726144112452981191%22%2C%22%24device_id%22%3A%20%2216eeceff221155-02282fd0ea27a8-3964720e-1ea000-16eeceff222afc%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22app%22%3A%20%22736404266750595330%22%2C%22org%22%3A%20null%2C%22bmp%22%3A%20%22%22%2C%22permissions%22%3A%20%7B%22sensitive_data%22%3A%202%2C%22aggregate_data%22%3A%201%2C%22link_level_settings%22%3A%202%2C%22app_level_settings%22%3A%202%2C%22channel_level_settings%22%3A%202%2C%22export%22%3A%201%2C%22revenue_data%22%3A%201%2C%22agency_tagged_data%22%3A%201%2C%22ad_networks%22%3A%201%2C%22location%22%3A%201%2C%22team_access%22%3A%202%2C%22fraud_settings_and_data%22%3A%202%7D%2C%22%24user_id%22%3A%20%22726144112452981191%22%7D; _gat=1; intercom-session-a5ol7px4=aUU1cXA4REFDalNVRkdicjZ4bGlkNWxkU2I3NmZpaFpZb2c2UE83aXg5NG1EOUJDc1E4MWl2TEE2eTNFUEd6di0tSVZjYzZPaEIvcTV3M2xjZDlreWpuQT09--4159f73684c4217a55ba9aec7bbadea874cd953c'
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