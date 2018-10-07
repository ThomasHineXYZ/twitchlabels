from urllib.parse import urlencode
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, InvalidURL, ConnectionError
import json

####################################################################
# Load up the credentials file
data = json.load(open('creds.json', 'r'))
credentials = data["credentials"]

# Location where the filled text file will go
saveLocation = "subscriberList.txt" #Put the location you'd like to save your list here

# Twitch's base API url (Helix is essentially v6)
baseApiUrl = "https://api.twitch.tv/helix/"

# Grabs the user's `user_id` from the Twitch API
queryUrl = "users"
parameter = "login"

fullUrl = baseApiUrl + queryUrl + "?" + parameter + "=" + data["userName"]

retryAdapter = HTTPAdapter(max_retries = 2)
session=Session()
session.mount('https://', retryAdapter)
session.mount('http://', retryAdapter)

#Find the Channel ID
response = session.get(fullUrl, headers = {
    'Client-ID': credentials['clientId'],
})

try:
    result = json.loads(response.text)
    data = result['data'][0]
except:
    print("Unable to fetch user ID. Exiting...")
    exit()

# If something was set for the result variable, continue. If nothing, exit
userId = 0
if (result):
    userId = data['id']
else:
    print("Unable to set user ID. Exiting...")
    exit()

print(userId)
