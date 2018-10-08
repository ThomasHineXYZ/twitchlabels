from urllib.parse import urlencode
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, InvalidURL, ConnectionError
import json
from pathlib import Path

########################
#  User Defined Values #
########################
# If you don't know Python, booleans (yes or no) need to be set as True or
# False (with the first letter as capital)
userSettings = {
    "recent_followers": {
        # How many recent follower's you've had. Leave at zero to load the
        # default amount
        "limit": 0,

        # If the list should be reversed
        "reverse": False
    }
}

##################################################################
#  Unless you know what you're doing, don't touch the code below #
##################################################################
# Checks if the credentials file is present
credentialsFile = Path("creds.json")
if not (credentialsFile.exists()) & (credentialsFile.is_file()):
    print("Please set up the credentials file and then re-run this program")
    exit()

# Load up the credentials file and check if the credentials data is all entered
credJsonFile = json.load(open(credentialsFile, 'r'))
if (credJsonFile["userName"] == ""):
    print("Oops, looks like you forgot to enter in your username")
    exit()

if (credJsonFile["credentials"]["clientId"] == ""):
    print("Oops, looks like you forgot to enter in your client ID")
    exit()

userName = credJsonFile["userName"]
credentials = credJsonFile["credentials"]

def twitchApi(query, parameter, values, limit = 0):
    # Twitch's base API url ("Helix" is essentially v6)
    baseApiUrl = "https://api.twitch.tv/helix/"

    # If it is a single value
    apiQueryUrl = ""
    if (type(values) is str):
        value = values
        apiQueryUrl = baseApiUrl + query + "?" + parameter + "=" + value

    # If it's an array/list
    else:
        arguments = ""
        for value in values:
            arguments = arguments + parameter + "=" + value + "&"

        apiQueryUrl = baseApiUrl + query + "?" + arguments
        apiQueryUrl = apiQueryUrl.rstrip("&")

    # If a limit number is given
    if (limit > 0):
        apiQueryUrl = apiQueryUrl + "&first=" + str(limit)
        print(apiQueryUrl)

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
followerList = twitchApi("users/follows", "to_id", userId, userSettings['recent_followers']['limit'])

# Most recent follower
followerUserId = followerList[0]["from_id"]
displayName = twitchApi("users", "id", followerUserId)[0]['display_name']
nameToFile(displayName, "newest_follower")

if (userSettings['recent_followers']['reverse']):
    followerList = reversed(followerList)

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

