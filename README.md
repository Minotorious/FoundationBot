# FoundationBot

Bot for the Official Foundation Discord Server

Official Discord Server: https://discord.gg/foundation

Official Developer Website: https://www.polymorph.games/

Steam Store Page: https://store.steampowered.com/app/690830/Foundation/

Available Features:

1. Screenshot Leaderboard
1. Messages Leaderboard
1. Ranking
1. Message Pinning
1. General Help and Utility

## Prerequisites
* 1 Role for the bot with the following permissions:
  * Manage Roles
  * Read Text Channels & See Voice Channels
  * Send Messages
  * Manage Messages
  * Read Message History
  * Mention @everyone, @here, and All Roles
  * Add Reactions

* 1 Custom Emoji to trigger the screenshot leaderboard
* 1 Channel dedicated to the screenshot leaderboard
* 3 Custom Emojis to trigger the ranking estate changes
* 1 Channel with a single message dedicated to the ranking emojis
* 1 Role from which the ranking starts
* 12 Roles, 4 per estate for the ranking to go through
* 1 Role all estate paths lead to
* 1 Channel for the message pinning
* Any number of roles to trigger the message pinning
* 1 Channel for the modding help command

## How to Set-Up & Settings Command Usage
First and foremost once the bot is online use the `/set help` command to see an overview of all the available settings to set before the bot is fully operational. **Note the `/set botActive` command which should be set to `True` only after all other settings have been set!**

All `/set` commands accept the Discord IDs of each respective setting as input, e.g. for a channel the channel ID, for a role the role ID, and for a custom emoji the emoji ID. To obtain the Discord IDs of channels, roles, emojis, etc. simply turn on the developer mode under `User Settings -> Appearance`

Note: the `/set pinsRoles` command accepts a comma separated series of role IDs which will all activate the pin emoji!

You can always use the `/set check` command to see an overview of which settings you have already set and which are still pending before activating the bot!
