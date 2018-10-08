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

def twitchApi(query, parameter, value):
    baseApiUrl = "https://api.twitch.tv/helix/"

    apiQueryUrl = baseApiUrl + query + "?" + parameter + "=" + value

    retryAdapter = HTTPAdapter(max_retries = 2)
    session=Session()
    session.mount('https://', retryAdapter)
    session.mount('http://', retryAdapter)

    #Find the Channel ID
    response = session.get(apiQueryUrl, headers = {
        'Client-ID': credentials['clientId'],
        'Content-Type': 'application/json'
    })

    # Check that the value was fetched and set correctly
    try:
        result = json.loads(response.text)

    except:
        print("Was unable to fetch value. Exiting...")
        exit()

    # If something was set for the result variable, continue. If nothing, exit
    if not (result):
        print("Unable to set value. Exiting...")
        exit()

    if 'status' in result:
        if (result['status'] == 429):
            print("Status ID: 429")
        print("Error Name: " + result["error"])
        print("Error Message: " + result["message"])
        print("")
        print(result)
        exit()

    print(result)

    return result

def nameToFile(userName, fileName):
    file = open(fileName + ".txt","w")
    file.write(userName)
    file.close()

    return

# Grab the user's user_id
userId = twitchApi("users", "login", userName)['data'][0]['id']

# Grab the follower list
followerList = twitchApi("users/follows", "to_id", userId)['data']

# Most recent follower
followerUserId = followerList[0]["from_id"]
displayName = twitchApi("users", "id", followerUserId)['data'][0]['display_name']
nameToFile(displayName, "newest_follower")

# 20 recent followers
for val in followerList:
    followerUserId = val["from_id"]
    displayName = twitchApi("users", "id", followerUserId)['data'][0]['display_name']
    print(displayName)

