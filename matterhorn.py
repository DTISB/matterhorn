import requests
import base64
import pprint
import pandas as pd
import time
import track
import re
import datetime

## Enter user's API key, secret, and Stubhub login
app_token = '3e9b99d1adcb38d09407cdd0f35bb4f5'
consumer_key = 'chb8GUauQvckFXI0lqjJ1y1oNG4a'
consumer_secret = '1udkFXv1hwTZtvHuhBw5DKs0_5Ma'
stubhub_username = 'levittdj@gmail.com'
stubhub_password = 'Zxcvbnm4!'

combo = consumer_key + ':' + consumer_secret
basic_authorization_token = base64.b64encode(combo.encode('utf-8'))

url = 'https://api.stubhub.com/login'
headers = {
        'Content-Type':'application/x-www-form-urlencoded',
        'Authorization':'Basic '+basic_authorization_token,}
body = {
        'grant_type':'password',
        'username':stubhub_username,
        'password':stubhub_password,
        'scope':'PRODUCTION'}

r = requests.post(url, headers=headers, data=body)
print r
print r.text

tag = None
tracks = track.tags

token_respoonse = r.json()
access_token = token_respoonse['access_token']
user_GUID = r.headers['X-StubHub-User-GUID']

for x in range(len(tracks)):
	tag = tracks[x]
	if tag == tracks[x]:
		inventory_url = 'https://api.stubhub.com/search/inventory/v2'
		eventid = tag
		data = {'eventid':tag, 'rows':1000}
		headers['Authorization'] = 'Bearer ' + access_token
		headers['Accept'] = 'application/json'
		headers['Accept-Encoding'] = 'application/json'

		inventory = requests.get(inventory_url, headers=headers, params=data)
		inv = inventory.json()
		snapshot_time = time.strftime("%Y-%m-%d-%H")
		pprint.pprint(inv['listing'])
		listing_df = pd.DataFrame(inv['listing'])
		listing_df['amount'] = listing_df.apply(
			lambda x: x['currentPrice']['amount'], axis=1)
		listing_df['snapshot time'] = snapshot_time
		listing_df.to_csv(tag + '.csv', index=False)
		
		#info_url = 'https://api.stubhub.com/catalog/events/v2/103138868'
		#info = requests.get(info_url, headers=headers)
		#info_dict = info.json()
		#pprint.pprint(info.json())
		#event_date = datetime.datetime.strptime(info_dict['eventDateLocal'][:10], '%Y-%m-%d')
		#event_name = inv['title']
		#event_date = inv['eventDateLocal'][:10]
		#venue = inv['venue']['name']

		#listing_df['datetime'] = snapshot_time
		#listing_df['eventName'] = event_name
		#listing_df['eventDate'] = event_date
		#listing_df['venue'] = venue

		#listing_df.to_csv(event_name + '.csv', index=False)





