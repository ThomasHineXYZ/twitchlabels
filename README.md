# Twitch Labels
What I've noticed over the last bit is that "Stream Labels" isn't available for Linux, however with me just hitting "Affiliate" on the platform I thought I should up the quality of my stream by adding some of these labels to it.

This project will work on more then just Linux, but Linux is the main demographic for it and the reason for creating it.

## What are Steam Labels
"Stream labels" are the name that is given to the little bits of text that are added to scenes in the streaming software of choice. Usually "most recent subscriber", "most recent follower", and so on.

## Install Process
* Make sure you have Python installed, set up, and working correctly.
* Clone this repo in to a folder somewhere on your computer.
* Go to the [Twitch Developers](https://dev.twitch.tv) page and sign in using your Twitch account.
* Open up the `Dashboard`, and go to the `Apps` section. On that screen press the `+ Register Your Application` button
* Add in a `name` for this program. Under `OAuth Redirect URL` you can put anything, I tend to put `http://localhost`. For the category choose `Broadcaster Suite`.
* Copy `creds.example.json` to `creds.json`, and fill in the `userName` with your Twitch Username and "clientId" with the Client ID that is given to you in the Twitch Developers page for the project.
* Run your desired tool, and taadaa. You're all done.
