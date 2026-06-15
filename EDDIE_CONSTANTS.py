# DATABASE PATH
DATABASE_PATH = "discordIDsToChannelIDs.json"
RANDOM_WORDS_PATH = "words.txt"

# DATA
CHANNELS_CANT_INCLUDE = ".!$%^&*(){}[]@'\" #~;:,<>/?\|`¬=+QWERTYUIOPASDFGHJKLZXCVBNM"
STORAGE_NOTIFICATION_THRESHOLD = 100

# DISCORD IDs
EDDIE_BOT_KEY = ""
GUILD_ID =
SUPPORT_AND_NEW_CHANNEL_ID =
SUPPORT_NOTIFY_CHANNEL_ID =
STORAGE_NOTIFICATION_CHANNEL_ID =

# CATEGORY NAMES
EDDIE_CHAT_CATEGORY = "Eddie Chats"
AWAITING_CHAT_CHANNELS_CATEGORY_NAME = "Awaiting Chat"

# CHANNEL NAMES
SUPPORT_CHAT_CHANNEL_NAME = "-chat"
EDDIE_CHAT_CHANNEL_NAME = "-introduction"

# ROLES
SUPPORT_ROLE_NAME = "Support"
AWAITING_CHAT_ROLE_NAME = "Awaiting Chat"
CHATTING_WITH_EDDIE_ROLE_NAME = "Chatting with Eddie"
MEMBER_ROLE_NAME = "Member"
EDDIE_IGNORE_ROLE_NAME = "ID ERROR Eddie Ignore"
READ_ACCESS_TO_ALL_ROLE_NAME = "Read Access To All"

# DATABASE KEY
EDDIE_CHAT_DATABASE_KEY = "EDDIE CHAT"
AWAITING_CHAT_DATABASE_KEY = "AWAITING CHAT"

# COMMANDS
MAKE_FULL_MEMBER_COMMAND = "make-full-member"
MAKE_FULL_MEMBER_DESCRIPTION = "Converts this Awaiting Chat Member into a Full Member, and deletes their Chat Channel"

# CHAT
INTRO_MESSAGE = f'''
Hi there!
I'm **Eddie**, the introduction bot.

I'll take you through the basics before your chat with one of the **Support** Roles!

Press **"Start"** when you are ready to begin.

If you have any problems, just message a **Support** role, there is a channel just for new players and them - <#{SUPPORT_AND_NEW_CHANNEL_ID}> or contact one of them directly.
'''

EDDIE_SUPPORT_ROLE_CHAT_MESSAGE_NAME_REPLACE_WORD = "[NAME]"
EDDIE_SUPPORT_ROLE_CHAT_MESSAGE = f'''**Great Job {EDDIE_SUPPORT_ROLE_CHAT_MESSAGE_NAME_REPLACE_WORD}**
Soon you'll be contacted by the Supports in this channel, and they'll introduce you to the server!
It was nice talking to you!
**Have fun!**
'''

PLEASE_READ_RULES = '''**PLEASE READ THE RULES**
There is **NO** option to go back to the rules after pressing "**Next**". (You will be able to read them at any time when you become a full member)'''

RULES_REPLACE_WORD = "REPLACE_ME"
SECRET_WORD_PHRASE = f"Please make a note of the word \"{RULES_REPLACE_WORD}\", it will be relevant in the next question."
GENERAL_RULES = f'''
**General Rules**

Members should be 16 years old or over. 

Respect other members and don't say or do anything harmful to another member.

In game you shouldn’t damage or obstruct anyone else’s creations unless you are given permission by the owner of the creation.

Keep in mind that this is an English Speaking Minecraft Server and although speaking in other languages is not against the rules, it might be difficult for a “Support” role to enforce the rules if it is done in a language that we are not familiar with. 

Do not edit messages with other people to change or remove their meaning. For example, if I gave permission for someone to build next to my house, then edited the message to make it look like I didn't. 

{SECRET_WORD_PHRASE}

Mods that don't affect how the game is played but are helpful are allowed. 
Examples of allowed mods:
      Litematica
      Freecam (for looking at builds)
Mods that aren't allowed would be anything that gives a player an advantage in the game, such as being able to fly. 

Killing the Wither under the centre end island portal is not allowed. We had a problem with Wither skulls going through the portal and damaging spawn.

Duplication of items, whether that is through a bug or mod, is not allowed.

We use the voice chat mod, however this is not a requirement and understand that some people will still prefer text chat even if they have the mod installed. No members should be left out of conversations because they don't use the mod.


Screenshots taken at the time can be useful when enforcing rules as this prevents people from editing/deleting messages. 

'''
YOUTUBE_RULES = '''
**YouTube Rules**
If you want to make videos of the server and upload them to YouTube (or another video sharing service) these are the rules you must follow:
      Do not include anyone in them that has not agreed to it. This includes seeing their username in the background or chat messages.

      Do not show off anyone's creations without their permission. Although their builds can be shown in the background. 

      Do not say anything negative about another player in a video unless they have given permission and there is evidence (screenshot) of their consent. 


Also, previous permission does not justify permission in a future video. Permission should be given each time or stated that it is forever.

It might be beneficial to take screenshots of permission in case the player tries to deny it after. Editing messages to remove previous meaning is not allowed however this would not stop someone from doing it. 

Feel free to display the name of the server within videos or in video titles. 
'''
HELP_MESSAGE_AFTER_RULES = f'''
**Need Help?**
If you need any clarification or help with these rules, please contact a Support.
This can be done by:
• Using <#{SUPPORT_AND_NEW_CHANNEL_ID}>
• Contacting one of them directly 
'''

SUCCESSFUL_END_MESSAGE = '''
**Thank you for reading the rules!**
'''

REASON_MESSAGE = '''
Thanks for that.
Please Provide a reason for your answer: 

(Just type it in as a message and send it here)
'''

END_MESSAGE = f'''
Thanks for that.

This is the end of our chat, I've sent a request to the Support roles and they'll review your answer.
This chat will be deleted when they respond to the request.

Your next step will be a chat with a Support Role, then you'll be allowed on the server!

**Any Problems?**
Just contact a Support through <#{SUPPORT_AND_NEW_CHANNEL_ID}> or by sending them a message directly.
'''

# STORAGE NOTIFICATION
STORAGE_NOTIFICATION_FREE_SPACE_REPLACE_WORD = "[FREE]"
STORAGE_NOTIFICATION_MESSAGE = f"{STORAGE_NOTIFICATION_FREE_SPACE_REPLACE_WORD} GB left! DO SOMETHING!"