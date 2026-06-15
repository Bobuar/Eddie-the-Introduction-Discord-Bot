import discord,json,time,warnings,shutil
from random import randint,choice,shuffle
from discord.ext import tasks
from discord import app_commands
from EDDIE_CONSTANTS import *

INTENTS = discord.Intents(messages=True,value=True,message_content=True,members=True)
client = discord.Client(intents=INTENTS)
commandTree = app_commands.CommandTree(client)

class ListeningToChannels:
    channelsToListenTo = {}
    @classmethod
    def addChannel(cls,channel,function,arguments):
        cls.channelsToListenTo[channel] = [function,arguments]
    @classmethod
    def getChannelFrom(cls,message):
        return message.channel
    @classmethod
    def isChannelToListenTo(cls,channel):
        return channel in cls.channelsToListenTo
    @classmethod
    def getFunctionAndArguments(cls,channel):
        return cls.channelsToListenTo[channel]
    @classmethod
    async def runFunction(cls,function,message,arguments):
        await function(message,*arguments)
    @classmethod
    async def messageReceived(cls,message):
        channelFrom = cls.getChannelFrom(message)
        if cls.isChannelToListenTo(channelFrom):
            function, arguments = cls.getFunctionAndArguments(channelFrom)
            await cls.runFunction(function,message,arguments)
            del cls.channelsToListenTo[channelFrom]

@client.event
async def on_message(message):
    channelFrom = message.channel
    categoryName = None
    if channelFrom.category != None:
        categoryName = channelFrom.category.name

    if message.author != client.user and categoryName != AWAITING_CHAT_CHANNELS_CATEGORY_NAME:
        await ListeningToChannels.messageReceived(message)
        try: # The function that is executed above might already delete it
            await message.delete()
        except:
            pass


async def getRole(role_name):
    for role in client.guilds[0].roles:
        if role.name == role_name:
            return role

    return None

def overwriteDiscordIDsToChannelIDsDatabase(category,data):
    databaseRead = readDatabase()
    databaseRead[category] = data

    dataBaseFile = open(DATABASE_PATH,"w")
    json.dump(databaseRead,dataBaseFile, indent=4)
    dataBaseFile.close()

def removeFromDatabase(category,member):
    dataBaseRead = getDiscordIDsToChannelIDs(category)
    del dataBaseRead[member]
    overwriteDiscordIDsToChannelIDsDatabase(category,dataBaseRead)

async def deleteChatChannel(channel,memberID):
    await channel.delete()

    category = ""
    if channel.category.name == EDDIE_CHAT_CATEGORY:
        category = EDDIE_CHAT_DATABASE_KEY
    elif channel.category.name == AWAITING_CHAT_DATABASE_KEY:
        category = AWAITING_CHAT_DATABASE_KEY

    removeFromDatabase(category,memberID)

async def deleteChatChannelsWithNoMemeber():
    discordIDToChannelIDs = getDiscordIDsToChannelIDs(EDDIE_CHAT_DATABASE_KEY)
    for discordID in discordIDToChannelIDs:
        channelID = discordIDToChannelIDs[discordID]
        channel = client.get_channel(channelID)
        member = await getNewMemberByName(discordID)
        memberStillHere = False
        if member in channel.members:
            memberStillHere = True

        if memberStillHere == False:
            await deleteChatChannel(channel,discordID)

@tasks.loop(hours=1)
async def schedule():
    await deleteChatChannelsWithNoMemeber()
    await checkStorage()
def getGuild():
    return discord.Object(id=GUILD_ID)

def getMemberNameFromChannelID(category,channelIDToLookFor):
    discordIDsToChannelIDs = getDiscordIDsToChannelIDs(category)
    for memberName in discordIDsToChannelIDs:
        channelID = discordIDsToChannelIDs[memberName]
        if channelID == channelIDToLookFor:
            return memberName

    return None

@commandTree.command(
    name=MAKE_FULL_MEMBER_COMMAND,
    description=MAKE_FULL_MEMBER_DESCRIPTION,
    guild=getGuild()
)
async def makeFullMember(interaction):
    if await getRole(SUPPORT_ROLE_NAME) in interaction.user.roles:
        if interaction.channel.category.name == AWAITING_CHAT_CHANNELS_CATEGORY_NAME:
            memberName = getMemberNameFromChannelID(AWAITING_CHAT_DATABASE_KEY,interaction.channel.id)
            member = await getNewMemberByName(memberName)
            await member.add_roles(await getRole(MEMBER_ROLE_NAME))
            await member.remove_roles(await getRole(AWAITING_CHAT_ROLE_NAME))

            await interaction.channel.delete()
            removeFromDatabase(AWAITING_CHAT_DATABASE_KEY,memberName)

@client.event
async def on_ready():
        await checkForPeopleWithoutRole()
        await checkForPeopleWithoutChat()
        await deleteChatChannelsWithNoMemeber()
        await restartAllChannels()
        await commandTree.sync(guild=getGuild())
        await schedule.start()

def readDatabase():
    dataBaseFile = open(DATABASE_PATH,"r")
    return json.loads(dataBaseFile.read())

def getDiscordIDsToChannelIDs(category):
    return readDatabase()[category]

async def restartAllChannels():
    '''Restart All channels on start up'''
    discordIDToChannelIDs = getDiscordIDsToChannelIDs(EDDIE_CHAT_DATABASE_KEY)
    for discordID in discordIDToChannelIDs:
        channelID = discordIDToChannelIDs[discordID]
        channel = client.get_channel(channelID)
        await channel.purge(limit=None)
        await newMemberStartChat(channel)

    async for message in client.get_channel(SUPPORT_NOTIFY_CHANNEL_ID).history(limit=None):
        if message.author == client.user:
            oldButtons = getOldNotificationuttons(message)
            newView = discord.ui.View(timeout=None)
            functionsToRun = createNewSendThroughButton, createNewRestartButton, createNewDeleteButton
            for i in range(len(functionsToRun)):
                function = functionsToRun[i]
                if oldButtons[i] != None:
                    newView.add_item(function(oldButtons[i]))
            await message.edit(view=newView)
        else:
            await message.delete()

def cleanLabelForName(label,newButtonClass):
    return label.replace(newButtonClass.LABEL_BEFORE,"").replace(" ","").replace(":","")

def createNewDeleteButton(previousButton):
    name = cleanLabelForName(previousButton.label,DeleteButton)

    return DeleteButton(name)

def getChannelFromMemberName(memberIDLookingFor):
    discordIDsToChannelIDs = getDiscordIDsToChannelIDs(EDDIE_CHAT_DATABASE_KEY)
    for memberID in discordIDsToChannelIDs:
        if memberID == memberIDLookingFor:
            return client.get_channel(discordIDsToChannelIDs[memberID])

    return None

def createNewSendThroughButton(previousButton):
    name = cleanLabelForName(previousButton.label,SendThroughButton)
    return SendThroughButton(name,getChannelFromMemberName(name))

def createNewRestartButton(previousButton):
    name = cleanLabelForName(previousButton.label,RestartUserButton)
    return RestartUserButton(name,getChannelFromMemberName(name))

def getOldNotificationuttons(message):
    deleteButton = None
    restartButton = None
    sendThroughButton = None

    for components in message.components:
        for component in components.children:
            if isinstance(component, discord.components.Button):
                if component.style == discord.ButtonStyle.red:
                    deleteButton = component
                elif component.style == discord.ButtonStyle.green:
                    sendThroughButton = component
                elif component.style == discord.ButtonStyle.blurple:
                    restartButton = component

    return sendThroughButton, restartButton, deleteButton
def getDeleteButton(message):
    for components in message.components:
        for component in components.children:
            if isinstance(component, discord.components.Button) and component.style == discord.ButtonStyle.red:
                return component

    return None

async def purgeEddieIntroChannels():
    discordIDToChannelIDs = getDiscordIDsToChannelIDs(EDDIE_CHAT_DATABASE_KEY)

    for discordID in discordIDToChannelIDs:
        channelID = discordIDToChannelIDs[discordID]
        channel = client.get_channel(channelID)
        await channel.purge(limit=None)

def memberAlreadyHasChannel(member):
    discordIDToChannelIDs = getDiscordIDsToChannelIDs(EDDIE_CHAT_DATABASE_KEY)
    for discordID in discordIDToChannelIDs:
        if discordID == member.name:
            return client.get_channel(discordIDToChannelIDs[member.name])

    return None

@client.event
async def on_member_join(member):
    #await memberNeedsIgnoring(member)
    if not await getRole(EDDIE_IGNORE_ROLE_NAME) in member.roles: # Keep just in case Eddie breaks for someone
        potentialChannel = memberAlreadyHasChannel(member)
        if potentialChannel:
            await potentialChannel.delete()
        await giveMemberRole(member,await getRole(CHATTING_WITH_EDDIE_ROLE_NAME))
        membersChannel = await createNewChat(member)
        await newMemberStartChat(membersChannel)

def addChatToDataBase(category,member,channelID):
    databaseRead = getDiscordIDsToChannelIDs(category)
    databaseRead[member] = channelID
    overwriteDiscordIDsToChannelIDsDatabase(category,databaseRead)

async def memberGotRole(member,roleName):
    if await getRole(roleName) in member.roles:
        return True

    return False

async def memberGotRoles(member,roleNames):
    hasAllRoless = True
    for roleName in roleNames:
        if not await memberGotRole(member,roleName):
            hasAllRoless = False
            break

    return hasAllRoless

async def memberGotOneOF(member,roleNames):
    for roleName in roleNames:
        if await memberGotRole(member,roleName):
            return True

    return False

async def giveMemberRole(member,role):
    await member.add_roles(role)

async def checkForPeopleWithoutRole():
    '''Get all members, if one exists without a role, give them the role "Chatting with Eddie"'''
    for member in client.get_all_members():
        if member.bot == False and not await memberGotOneOF(member,[CHATTING_WITH_EDDIE_ROLE_NAME,MEMBER_ROLE_NAME,AWAITING_CHAT_ROLE_NAME,EDDIE_IGNORE_ROLE_NAME]):
            #print(member)
            await giveMemberRole(member,await getRole(CHATTING_WITH_EDDIE_ROLE_NAME))

async def getAllMembersWithRole(role):
    members = []

    for member in client.get_all_members():
        if await getRole(role) in member.roles:
            members.append(member)

    return members

def getAllChannels():
    channels = []
    for channel in client.get_all_channels():
        if not isinstance(channel,discord.CategoryChannel):
            channels.append(channel)

    return channels

def getChannelFromName(name):
    for channel in getAllChannels():
        if channel.name == name:
            return channel

    return None
def memberHasChatChannel(member):
    discordIDsToChannelIDs = getDiscordIDsToChannelIDs(EDDIE_CHAT_DATABASE_KEY)

    for memberName in discordIDsToChannelIDs:
        if member.name == memberName:
            return True

    return False

async def checkForPeopleWithoutChat():
    for member in await getAllMembersWithRole(CHATTING_WITH_EDDIE_ROLE_NAME):
       if not memberHasChatChannel(member):
           await createNewChat(member)

def removeFrom(string,toRemove):
    return string.replace(toRemove, "")

def cleanMemberName(memberName):
    for unwanted in CHANNELS_CANT_INCLUDE:
        memberName = removeFrom(memberName,unwanted)

    return memberName

def channelNameInUse(channelName):
    return discord.utils.get(client.guilds[0].channels, name=channelName) != None

def makeUnusedChatName(chatName):
    numberToAdd = 0
    while channelNameInUse(f"{chatName}{numberToAdd}"):
        numberToAdd += 1

    return f"{chatName}{numberToAdd}"

def makeChannelName(memberName,channelNameAdd):
    memberName = cleanMemberName(memberName)
    if memberName == "":
        memberName = "member_name"

    idealChatName = f"{memberName}{channelNameAdd}"
    if channelNameInUse(idealChatName):
        chatName = makeUnusedChatName(idealChatName)
    else:
        chatName = idealChatName

    return chatName

async def makeChatChannel(member,channelNameAdd,permissions,category):
    chatName = makeChannelName(member.name, channelNameAdd)

    await client.guilds[0].create_text_channel(chatName, overwrites=permissions, category=category)
    channel = getChannelFromName(chatName)

    return channel

async def createNewChat(member):
    '''
    :return channel: - the channel that has been created
    '''
    permissions = {
        client.guilds[0].default_role: discord.PermissionOverwrite(view_channel=False),
        member: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        client.guilds[0].me: discord.PermissionOverwrite(view_channel=True,send_messages=True),
        await getRole(READ_ACCESS_TO_ALL_ROLE_NAME) : discord.PermissionOverwrite(view_channel=True)
    }
    category = discord.utils.get(client.guilds[0].categories, name=EDDIE_CHAT_CATEGORY)

    channel = await makeChatChannel(member,EDDIE_CHAT_CHANNEL_NAME,permissions,category)

    addChatToDataBase(EDDIE_CHAT_DATABASE_KEY,member.name,channel.id)

    return channel

async def newMemberStartChat(channel):
    view = discord.ui.View(timeout=None)
    view.add_item(StartButton(channel))
    await channel.send(INTRO_MESSAGE,view=view)

class forChannel:
    def __init__(self,channel):
        self.channel = channel
    def getChannel(self):
        return self.channel

class NewMemberProfile:
    def __init__(self,name,startTimeStamp):
        self.name = name
        self.reason = None
        self.correctOrIncorrect = None
        self.startTimeStamp = startTimeStamp
        self.endTimeStamp = None
        self.actualCorrectAnswer = None
    def addReason(self,reason):
        self.reason = reason
    def setCorrectOrIncorrect(self,isIt):
        self.correctOrIncorrect = isIt
    def setEndTimeStamp(self,endTimeStamp):
        self.endTimeStamp = endTimeStamp
    def setActualCorrectWord(self,correctWord):
        self.actualCorrectAnswer = correctWord
    def getSecondsToRead(self):
        return self.endTimeStamp - self.startTimeStamp
    def getActualCorrectAnswer(self):
        return self.actualCorrectAnswer
async def getReason(profile,channel):
    await channel.send(REASON_MESSAGE)
    ListeningToChannels.addChannel(channel,gotReason,(profile,channel))
async def gotReason(message,profile,channel):
    #print(message.content)
    reason = message.content
    profile.addReason(reason)
    await channel.purge(limit=None)
    await channel.send(END_MESSAGE)
    await notifySupportOfProfile(profile,channel)

class OptionButton(discord.ui.Button,forChannel):
    def __init__(self,label,channel,profile):
        discord.ui.Button.__init__(self,label=label, style=discord.ButtonStyle.blurple)
        forChannel.__init__(self,channel)
        self.profile = profile
    async def callback(self, interaction):
        await getReason(self.profile,self.channel)

class WrongOptionButton(OptionButton):
    def __init__(self,label,channel,profile):
        OptionButton.__init__(self,label,channel,profile)
    async def callback(self, interaction):
        channel = self.getChannel()
        await channel.purge(limit=None)
        self.profile.setCorrectOrIncorrect(False)
        await OptionButton.callback(self,interaction)

class RightOptionButton(OptionButton):
    def __init__(self,label,channel,profile):
        OptionButton.__init__(self,label,channel,profile)
    async def callback(self, interaction):
        channel = self.getChannel()
        await channel.purge(limit=None)
        self.profile.setCorrectOrIncorrect(True)
        await OptionButton.callback(self,interaction)

class NextButton(discord.ui.Button,forChannel):
    def __init__(self,channel,choices,profile):
        discord.ui.Button.__init__(self,label="Next", style=discord.ButtonStyle.green)
        forChannel.__init__(self, channel)
        self.choices = choices
        self.profile = profile
    async def callback(self, interaction):
        channel = self.getChannel()
        self.profile.setEndTimeStamp(getCurrentTimeStamp())
        await channel.purge(limit=None)
        view = discord.ui.View(timeout=None)

        rightWord = self.choices.getCorrect()
        incorrectWords = self.choices.getIncorrect()
        buttons = [
            RightOptionButton(rightWord,channel,self.profile),
            WrongOptionButton(incorrectWords[0],channel,self.profile),
            WrongOptionButton(incorrectWords[1],channel,self.profile)
        ]
        shuffle(buttons)
        for button in buttons:
            view.add_item(button)
        await channel.send("Pick one of the following:",view=view)

class Choices:
    def __init__(self):
        self.incorrect = []
        self.correct = None
        wordsFile = open(RANDOM_WORDS_PATH, "r")
        words = self.cleanWords(wordsFile.readlines())
        wordsFile.close()

        correctIndex = randint(0,2)
        for i in range(3):
            pickedWord = choice(words)
            if i == correctIndex:
                self.correct = pickedWord
            else:
                self.incorrect.append(pickedWord)
            words.remove(pickedWord)
    def cleanWords(self,words):
        cleanWords = []
        for word in words:
            cleanWords.append(word.replace("\n",""))

        return cleanWords
    def getCorrect(self):
        return self.correct
    def getIncorrect(self):
        return self.incorrect

def makeGeneralRules(choices):
    return GENERAL_RULES.replace(RULES_REPLACE_WORD,choices.getCorrect())

def getCurrentTimeStamp():
    return time.time()

class StartButton(discord.ui.Button,forChannel):
    def __init__(self,channel):
        discord.ui.Button.__init__(self,label="Start", style=discord.ButtonStyle.green)
        forChannel.__init__(self,channel)
    async def callback(self, interaction):
        channel = self.getChannel()
        profile = NewMemberProfile(interaction.user.name,getCurrentTimeStamp())
        await channel.purge(limit=None)
        view = discord.ui.View(timeout=None)
        choices = Choices()
        profile.setActualCorrectWord(choices.getCorrect())
        generalRules = makeGeneralRules(choices)
        view.add_item(NextButton(channel,choices,profile))
        await channel.send(PLEASE_READ_RULES)
        await channel.send(generalRules)
        await channel.send(YOUTUBE_RULES)
        #await channel.send(PLEASE_READ_RULES)
        await channel.send(HELP_MESSAGE_AFTER_RULES)
        await channel.send(view=view)

class NotificationButton(discord.ui.Button,forChannel):
    def __init__(self,playerName,style,userChannel=None):
        discord.ui.Button.__init__(self,label=f"{self.LABEL_BEFORE}: {playerName}",style=style)
        forChannel.__init__(self,userChannel)
    async def callback(self, interaction):
        await interaction.message.delete()

class DeleteButton(NotificationButton):
    #LABEL_AFTER = "MESSAGE DELETE"
    LABEL_BEFORE = "DELETE NOTIFICATION FOR"
    def __init__(self,playerName):
        NotificationButton.__init__(self,playerName,discord.ButtonStyle.red)

class RestartUserButton(NotificationButton):
    LABEL_BEFORE = "RESTART"
    def __init__(self,playerName,userChannel):
        NotificationButton.__init__(self,playerName,discord.ButtonStyle.blurple,userChannel=userChannel)
    async def callback(self, interaction):
        await NotificationButton.callback(self,interaction)

        channel = self.getChannel()
        await channel.purge(limit=None)
        await newMemberStartChat(channel)

async def getNewMemberByName(memberName):
    for member in await getAllMembersWithRole(CHATTING_WITH_EDDIE_ROLE_NAME) + await getAllMembersWithRole(AWAITING_CHAT_ROLE_NAME):
        if member.name == memberName:
            return member

    return None

class SendThroughButton(NotificationButton):
    LABEL_BEFORE = "SEND TO NEXT STAGE"
    def __init__(self,playerName,userChannel):
        NotificationButton.__init__(self,playerName,discord.ButtonStyle.green,userChannel=userChannel)
        self.memberName = playerName
    async def callback(self, interaction):
        await NotificationButton.callback(self,interaction)
        member = await getNewMemberByName(self.memberName)
        await member.add_roles(await getRole(AWAITING_CHAT_ROLE_NAME))
        await member.remove_roles(await getRole(CHATTING_WITH_EDDIE_ROLE_NAME))
        userChannel = self.getChannel()
        await deleteChatChannel(userChannel,member.name)
        await createSupportChatChannel(member)

def createNotificationTimePhrase(secondsToRead):
    TIME_REPLACE_WORD = "[TIME]"
    TIME_PHRASE = "**[TIME] TAKEN TO READ RULES: **"

    if secondsToRead < 60:
        replaceWith = "❌ SECONDS"
        divide = 1
    else:
        replaceWith = "✅ MINUTES"
        divide = 60

    timePhrase = TIME_PHRASE.replace(TIME_REPLACE_WORD,replaceWith)
    timePhrase += str(round(secondsToRead / divide))

    return timePhrase
async def notifySupportOfProfile(profile,userChannel):
    channel = client.get_channel(SUPPORT_NOTIFY_CHANNEL_ID)
    name = profile.name
    reason = profile.reason
    isCorrectAnswer = "Yes" if profile.correctOrIncorrect else "No"
    correctAnswer = ""
    if not profile.correctOrIncorrect:
        correctAnswer = f"\n**CORRECT ANSWER:** {profile.getActualCorrectAnswer()}\n"
    secondsToRead = profile.getSecondsToRead()
    timePhrase = createNotificationTimePhrase(secondsToRead)


    message = f'''
**{name}**

{timePhrase}
    
**PICKED CORRECT ANSWER:** {isCorrectAnswer}
{correctAnswer}
**REASON:** {reason}
'''
    view = discord.ui.View(timeout=None)
    view.add_item(SendThroughButton(name, userChannel))
    view.add_item(RestartUserButton(name, userChannel))
    view.add_item(DeleteButton(name))
    await channel.send(message,view=view)
    # Should store all notfications in a log file, that also contains the time the notification was sent, just in case.
async def createSupportChatChannel(member):
    permissions = {
        client.guilds[0].default_role: discord.PermissionOverwrite(view_channel=False),
        member: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        client.guilds[0].me: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        await getRole(SUPPORT_ROLE_NAME): discord.PermissionOverwrite(view_channel=True, send_messages=True),
        await getRole(READ_ACCESS_TO_ALL_ROLE_NAME) : discord.PermissionOverwrite(view_channel=True)
    }
    category = discord.utils.get(client.guilds[0].categories, name=AWAITING_CHAT_CHANNELS_CATEGORY_NAME)

    channel = await makeChatChannel(member, SUPPORT_CHAT_CHANNEL_NAME, permissions, category)

    addChatToDataBase(AWAITING_CHAT_DATABASE_KEY,member.name,channel.id)

    await channel.send(EDDIE_SUPPORT_ROLE_CHAT_MESSAGE.replace(EDDIE_SUPPORT_ROLE_CHAT_MESSAGE_NAME_REPLACE_WORD,member.name))

    return channel

async def sendStorageNotification(freeSpace):
    channel = client.get_channel(STORAGE_NOTIFICATION_CHANNEL_ID)
    freeSpace = str(round(freeSpace))
    await channel.send(STORAGE_NOTIFICATION_MESSAGE.replace(STORAGE_NOTIFICATION_FREE_SPACE_REPLACE_WORD,str(freeSpace)))
async def checkStorage():
    freeSpace = shutil.disk_usage("/").free / (2**30)
    print(freeSpace)
    if freeSpace < STORAGE_NOTIFICATION_THRESHOLD:
        await sendStorageNotification(freeSpace)

client.run(EDDIE_BOT_KEY)
