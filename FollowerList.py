from urllib.parse import urlencode
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, InvalidURL, ConnectionError
import json

# Load up the credentials file
credJsonFile = json.load(open('creds.json', 'r'))
userName = credJsonFile["userName"]
credentials = credJsonFile["credentials"]

# Location where the filled text file will go
saveLocation = "subscriberList.txt" #Put the location you'd like to save your list here

# Twitch's base API url (Helix is essentially v6)
baseApiUrl = "https://api.twitch.tv/helix/"

def getUserName(userId):
    # Grabs the user's `user_id` from the Twitch API
    queryUrl = "users"
    parameter = "id"

    fullUrl = baseApiUrl + queryUrl + "?" + parameter + "=" + userId

    retryAdapter = HTTPAdapter(max_retries = 2)
    session=Session()
    session.mount('https://', retryAdapter)
    session.mount('http://', retryAdapter)

    #Find the Channel ID
    response = session.get(fullUrl, headers = {
        'Client-ID': credentials['clientId'],
        'Content-Type': 'application/json'
    })

    try:
        result = json.loads(response.text)
        resultData = result['data'][0]

    except:
        print("Unable to fetch user name. Exiting...")
        exit()

    # If something was set for the result variable, continue. If nothing, exit
    userId = 0
    if not (result):
        print("Unable to set user name. Exiting...")
        exit()

    return resultData["display_name"]

# Grabs the user's `user_id` from the Twitch API
queryUrl = "users"
parameter = "login"

fullUrl = baseApiUrl + queryUrl + "?" + parameter + "=" + userName

retryAdapter = HTTPAdapter(max_retries = 2)
session=Session()
session.mount('https://', retryAdapter)
session.mount('http://', retryAdapter)

#Find the Channel ID
response = session.get(fullUrl, headers = {
    'Client-ID': credentials['clientId'],
    'Content-Type': 'application/json'
})

try:
    result = json.loads(response.text)
    resultData = result['data'][0]

except:
    print("Unable to fetch user ID. Exiting...")
    exit()

# If something was set for the result variable, continue. If nothing, exit
userId = 0
if not (result):
    print("Unable to set user ID. Exiting...")
    exit()

userId = resultData['id']


##########################################################
#              Grab the user_id for the user             #
##########################################################

# Grabs the user's `user_id` from the Twitch API
queryUrl = "users/follows"
parameter = "to_id"

fullUrl = baseApiUrl + queryUrl + "?" + parameter + "=" + userId

retryAdapter = HTTPAdapter(max_retries = 2)
session = Session()
session.mount('https://', retryAdapter)
session.mount('http://', retryAdapter)

#Find the Channel ID
response = session.get(fullUrl, headers = {
    'Client-ID': credentials['clientId'],
    'Content-Type': 'application/json'
})

try:
    result = json.loads(response.text)
    resultData = result['data']

except:
    print("Unable to fetch follower list. Exiting...")
    exit()

# If something was set for the result variable, continue. If nothing, exit
if not (resultData):
    print("Unable to set user ID. Exiting...")
    exit()

userId = resultData[0]["from_id"]
print(getUserName(userId))
