from urllib.parse import urlencode
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, InvalidURL, ConnectionError
import json

##########################################################
#                Configure your stuff here               #
##########################################################

# Load up the credentials file
data = json.load(open('creds.json', 'r'))
credentials = data["credentials"]

# Sets up the client ID and token
clientId=""  #Register a Twitch Developer application and put its client ID here
accessToken="" #Generate an OAuth token with channel_subscriptions scope and insert your token here

channelName=""  #Put your channel name here
saveLocation = "subscriberList.txt" #Put the location you'd like to save your list here

#################################
# Grab the user_id for the user #
#################################
session=Session()
channelId=""

channelIdUrl="https://api.twitch.tv/kraken/users?login=" + data['userName']

retryAdapter = HTTPAdapter(max_retries=2)
session.mount('https://',retryAdapter)
session.mount('http://',retryAdapter)

#Find the Channel ID
response = session.get(channelIdUrl, headers={
    'Client-ID': clientId,
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Content-Type': 'application/json'
})

print(json.dump(response))
try:
    result = json.loads(response.text)
except:
    result = None

if (result):
    channelId = result["users"][0]["_id"]

print(channelId)

result = None
response = None

apiRequestUrl="https://api.twitch.tv/kraken/channels/"+channelId+"/subscriptions?limit=100"

#Do the API Lookup
response = session.get(apiRequestUrl, headers={
'Client-ID': clientId,
'Accept': 'application/vnd.twitchtv.v5+json',
'Authorization': 'OAuth '+accessToken,
'Content-Type': 'application/json'
})
try:
    result = json.loads(response.text)
except:
    result = None

if (result):
    subList=[]
    for sub in result["subscriptions"]:
        name=sub['user']['display_name']
        if name!=channelName:
            print(name)
            subList.append(sub['user']['display_name'])

    f = open(saveLocation,'w')
    for sub in subList:
        f.write(sub+"\n")
    f.close()
