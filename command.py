import praw
import variables
import datetime
from datetime import timedelta
import json

filterActive = True

async def clear(bot, ctx, num : int):
    perms = ctx.message.channel.permissions_for(ctx.message.author)
    if perms.manage_messages:
        messsages = bot.messages
        if num > 0:
            temp = []
            while num >= 0:
                try:
                    temp.append(messsages.pop())
                    num = num - 1
                except Exception:
                    num = 0
            await bot.delete_messages(temp)


async def schedule(bot):
    try:
        r = praw.Reddit(client_id=variables.client_id,
                        client_secret=variables.client_secret,
                        user_agent=variables.user_agent,
                        username=variables.username,
                        password=variables.password)
        sidebar = r.subreddit(variables.subreddit).wiki['edit_sidebar'].content_md
        schedule = sidebar[sidebar.index("Schedule") + 37 : sidebar.index("Upcoming Events") - 36]
        await bot.say(schedule)
        await (bot.say("All Times in Eastern"))
        print('Done')
    except Exception:
        print ('Failure')
        pass

async def contentFilter (bot, ctx):
    global filterActive
    perms = ctx.message.channel.permissions_for(ctx.message.author)
    if perms.manage_channels:
        str = ctx.message.content.replace("!filter", "").strip()
        if str is "":
            filterActive = not filterActive
            status = "On" if filterActive else "Off"
            await bot.say("Content Filter is " + status)
        elif str.lower() == "off":
            filterActive = False
            await bot.say("Content Filter is Off")
        elif str.lower() == "on":
            filterActive = True
            await bot.say("Content Filter is On")
        elif str.startswith("add"):
            parts = str.split(' ', 1)
            parts[1] = parts[1].lower()
            if parts[1] in variables.contentFilter:
                await bot.say("\"" + parts[1] + "\" already is in the content filter.")
                return
            else:
                variables.contentFilter.append(parts[1])
                saveConfig()
                await bot.say("\"" + parts[1] + "\" has been added to the content filter.")
        elif str.startswith("list"):
                await bot.say(variables.contentFilter)
        elif str.startswith("remove"):
            parts = str.split(' ', 1)
            parts[1] = parts[1].lower()
            if parts[1] in variables.contentFilter:
                variables.contentFilter.remove(parts[1])
                saveConfig()
                await bot.say("\"" + parts[1] + "\" has been removed from the content filter.")
            else:
                await bot.say("\"" + parts[1] + "\" is not in the content filter.")

async def help(bot, ctx):
    author = ctx.message.author
    help = open('help.txt', 'w').read()
    bot.send_message(author, help)

async def update(bot, ctx):
    perms = ctx.message.channel.permissions_for(ctx.message.author)
    if perms.manage_channels:
        result = updateConfig()
        if result:
            await bot.say('Updated Config.')
        else:
            await bot.say('Config failed to Update.')

async def list(bot):
    await(bot.say(variables.textCommands.keys()))

async def add(bot, ctx):
    perms = ctx.message.channel.permissions_for(ctx.message.author)
    if perms.manage_channels:
        str = ctx.message.content.replace("!add", "").strip()
        parts = str.split(' ', 1)
        if parts[0] in variables.textCommands:
            await bot.say("\"" + parts[0] + "\" already has a pairing.")
        else:
            variables.textCommands[parts[0]] = parts[1]
            saveConfig()
            await bot.say("\"" + parts[0] + "\" has been paired with \"" + parts[1] + "\".")

async def edit(bot, ctx):
    perms = ctx.message.channel.permissions_for(ctx.message.author)
    if perms.manage_channels:
        str = ctx.message.content.replace("!edit", "").strip()
        parts = str.split(' ', 1)
        if parts[0] in variables.textCommands:
            variables.textCommands[parts[0]] = parts[1]
            saveConfig()
            await bot.say("\"" + parts[0] + "\" has been edited and is now paired with \"" + parts[1] + "\".")
        else:
            await bot.say("\"" + parts[0] + "\" has no command to edit.")

async def delete(bot, ctx):
    perms = ctx.message.channel.permissions_for(ctx.message.author)
    if perms.manage_channels:
        str = ctx.message.content.replace("!delete", "").strip()
        if str in variables.textCommands:
            variables.textCommands.pop(str)
            saveConfig()
            await bot.say("\"" + str + "\" command has been deleted.")
        else :
            await bot.say("\"" + str + "\" has no command to delete.")

async def ddt(bot):
    now = datetime.datetime.now()
    if not hasattr(ddt, "link") or not hasattr(ddt, "time") or ddt.time + timedelta(minutes= variables.timeout) < now:
        r = praw.Reddit(client_id=variables.client_id,
                        client_secret=variables.client_secret,
                        user_agent=variables.user_agent,
                        username=variables.username,
                        password=variables.password)
        for submission in r.subreddit(variables.subreddit).search(query= '[MISC] Daily Discussion Thread ('  + variables.months[now.month] + str(now.day).zfill(2) + ', ' + str(now.year) + ')', sort= 'new', time_filter = 'week'):
            ddt.link = submission.url
            ddt.time = now
            break #only want the first result
    await bot.say(ddt.link)

async def match(bot):
    r = praw.Reddit(client_id=variables.client_id,
                    client_secret=variables.client_secret,
                    user_agent=variables.user_agent,
                    username=variables.username,
                    password=variables.password)
    top = r.subreddit(variables.subreddit).sticky(1)
    bottom = r.subreddit(variables.subreddit).sticky(2)
    found = False
    if "] Match Thread:" in top.title:
        await bot.say(top.url)
        found = True
    if "] Match Thread:" in bottom.title:
        await bot.say(bottom.url)
        found = True
    if not found:
        await bot.say("No Current Match Thread Found")

def updateConfig():
    try:
        r = praw.Reddit(client_id=variables.client_id,
                        client_secret=variables.client_secret,
                        user_agent=variables.user_agent,
                        username=variables.username,
                        password=variables.password)
        config = r.subreddit(variables.subreddit).wiki['discord'].content_md
        config = config.split("\r\n\r\n")
        variables.textCommands = json.loads(config[0])
        variables.contentFilter = json.loads(config[1])
        return True
    except Exception:
        return False

def saveConfig():
    try:
        txt = json.dumps(variables.textCommands)
        txt += "\r\n\r\n"
        txt += json.dumps(variables.contentFilter)
        r = praw.Reddit(client_id=variables.client_id,
                        client_secret=variables.client_secret,
                        user_agent=variables.user_agent,
                        username=variables.username,
                        password=variables.password)
        r.subreddit(variables.subreddit).wiki['discord'].edit(txt)
        return True
    except Exception:
        print("Error Saving Config")
        return False

