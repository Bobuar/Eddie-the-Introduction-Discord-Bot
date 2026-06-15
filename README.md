# Eddie the Introduction Discord Bot
The introduction bot used on the TDT server. This is supposed to be (although this is not yet the case) one bot that handles every user interaction on the server, not just introductions (although it mostly does that at the moment😆).

## Key
I will refer to moderators of the TDT server as "Support" or "Support Roles" throughout this document and in the code of any of the bots that run there· 

## Reason For creation
It was originally designed in response to a lot of rule breaking we were getting on the TDT server. Rule breaking is now rare due to this and a few other changes we've made to our introduction process. As is the case with all TDT member related Discord bots I make, it was designed with the input and approval of all the Supports on the TDT server.

## How to use
This bot has been designed specifically for the TDT server so direct use on other servers is not recommended. This repository is intended as a learning tool where I can show what I have done and you are free to take that and use it in your own projects.
### Setup
Make sure that these parts (found in the EDDIE_CONSTANTS.py file) are setup for your server: 

- EDDIE_BOT_KEY = Your bot's key
- GUILD_ID = Your server's ID
- SUPPORT_AND_NEW_CHANNEL_ID = ID for the channel for new members and moderators
- SUPPORT_NOTIFY_CHANNEL_ID = ID for channel where moderators will see new member reports
- STORAGE_NOTIFICATION_CHANNEL_ID = ID for channel where storage warnings will be sent

Everything else in EDDIE_CONSTANTS.py should be changed to meet your specific server needs. More comments in the code for what each component does coming soon-ish, in the mean time, Good Luck!

## Current Features
### New member introduction
The process:
- New member joins the server
- New members are restricted to two channels:
   - Support and New members - in case there is a problem with Eddie
   - A "Chat" with Eddie
- The Eddie chat is activated through a start button in the chat channel.
- The new member is shown and asked to read the rules
- The rules contain a random word with a sentence asking them to make note of it
- They press the next button
- The rules are hidden
- They are provided with a multiple choice (Two random words and the random word they had in their rules)
- They pick a word and are asked to enter a reason for their selection
- A message is then sent to the Supports containing:
  - How long it took the new member to read the rules
  - If they got the question right
  - The reason they gave for their answer (ensures they know why they got it right)
- The Support reviewing the application can then decide if they would like to:
  - Send the member to the next stage
  - Restart Eddie's chat for that member, giving them another chance to read the rules
  - Remove the member from the server (Eddie does NOT and will NEVER have the ability to remove people from the server himself, this action will always be decided by a human through the Discord GUI to prevent human or machine error)
- The next stage is a chat with the Supports (at least one, and whoever else's around) to get to know the new member and introduce them to the server.
- A command to Eddie by a Support then deletes the chat channel and gives the new member access to more of the Discord server 

### Storage Notifications
If the storage of the server goes below 100GB, a notification is sent to Bobuar to sort it out. 
Because our members like to play Minecraft so much 😆, our backups for the Survival server are quite large. Before this feature of Eddie and before we setup offsite backups, this caused the server to run out of storage on multiple occasions, causing players work to not be saved, which is very frustrating. So with this warning it shouldn't run out of storage again 🥳. 

## Known Issues
### Deleting Chat channels when members leave
Eddie does not delete chat channels if new members leave the server, these are only deleted after the process is complete. The problem is that if these are deleted manually, Eddie will error because he can't find one of his channels so they have to be deleted in his database (json file) as well.

## Bobuar's Wishlist
These are the things Bobuar wishes Eddie could do (and maybe one day he will)
### Log
It would be great if there was a log of everything that happened with Eddie for each new member. Sometimes it would be nice to check back through the chat with the new member and read what was talked about but this is deleted when they become a full member. Maybe it could be that the channel permissions are removed for everyone and re-added when a Support wants to check it, just for that specific Support that requested it. Eddie could even end the channel with a copy of the new members hidden word report (the member would never see this), just in case Supports needed to review it again. 

### Timezone table bot should be done by Eddie instead
There is a bot on the server that stores everyone's timezones in a table. This is done with another bot but it would be great if Eddie did it. 

### Eddie deletes chats where members have left the server
