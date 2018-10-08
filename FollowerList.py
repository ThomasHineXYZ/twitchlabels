from urllib.parse import urlencode
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, InvalidURL, ConnectionError
import json

# Load up the credentials file
credJsonFile = json.load(open('creds.json', 'r'))
userName = credJsonFile["userName"]
credentials = credJsonFile["credentials"]

def twitchApi(query, parameter, values):
    # Twitch's base API url (Helix is essentially v6)
    baseApiUrl = "https://api.twitch.tv/helix/"

    # If it is a single value
    if (type(values) is str):
        value = values
        apiQueryUrl = baseApiUrl + query + "?" + parameter + "=" + value

    # If it's an array/list
    else:
        arguments = ""
        for value in values:
            arguments = arguments + parameter + "=" + value + "&"

        apiQueryUrl = baseApiUrl + query + "?" + arguments

    retryAdapter = HTTPAdapter(max_retries = 2)
    session = Session()
    session.mount('https://', retryAdapter)
    session.mount('http://', retryAdapter)

    # Run the API request, and store the results
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

    # Checks if an error was returned
    if 'status' in result:
        print("API ERROR OCCURED:")
        print("")
        if (result['status'] == 429):
            print("Status ID: 429")
        print("Error Name: " + result["error"])
        print("Error Message: " + result["message"])
        print("")
        print(result)
        exit()

    return result['data']

def nameToFile(userNames, fileName):
    file = open(fileName + ".txt","w")

    # If it is a single value
    if (type(userNames) is str):
        userName = userNames
        file.write(userName)

    # If it's an array/list
    else:
        for userName in userNames:
            file.write(userName + "\n")

    file.close()

    return

# Grab the user's user_id
userId = twitchApi("users", "login", userName)[0]['id']

# Grab the follower list
followerList = twitchApi("users/follows", "to_id", userId)

# Most recent follower
followerUserId = followerList[0]["from_id"]
displayName = twitchApi("users", "id", followerUserId)[0]['display_name']
nameToFile(displayName, "newest_follower")

# 20 recent followers
followerIds = []
for follower in followerList:
    followerUserId = follower["from_id"]
    followerIds.append(followerUserId)

followersInfo = twitchApi("users", "id", followerIds)
displayNames = []
for follower in followersInfo:
    displayNames.append(follower["display_name"])

nameToFile(displayNames, "recent_followers")

