import praw
import variables
import datetime
import Betting
from datetime import timedelta
import json
import discord
import jsonpickle
import datetime
import time
import calendar

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

async def afterdark (bot,ctx):
    perms = ctx.message.channel.permissions_for(ctx.message.author)
    if perms.manage_messages:
        string = ctx.message.content.replace("!afterdark", "").strip()
        if string == "clear":
            variables.purge = []
            variables.dark = False
            await bot.say("Cleared Discord After Dark.")
        else:
            if variables.dark:
                for msg in variables.purge:
                    try:
                        if msg.channel.name ==  'general' or msg.channel.name == 'bot-testing':
                            await bot.delete_message(msg)
                    except Exception:
                        pass
                variables.purge = []
            variables.dark = not variables.dark
            if variables.dark is True:
                await (bot.say("It's that time for Discord After Dark."))
            else:
                await (bot.say("Discord After Dark has ended."))



async def schedule(bot):
    try:
        r = praw.Reddit(client_id=variables.client_id,
                        client_secret=variables.client_secret,
                        user_agent=variables.user_agent,
                        username=variables.username,
                        password=variables.password)
        sidebar = r.subreddit('OpTicGaming').wiki['edit_sidebar'].content_md
        schedule = sidebar[sidebar.index("Schedule") : sidebar.index("*All times are in") - 5]
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
    print(variables.textCommands.keys())
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
    if perms.manage_channels or ctx.message.author.id == '111981607732162560':
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
async def total(bot, ctx):
    user = ctx.message.author
    if user.id not in variables.blacklist:
        num = variables.freq[user.id]
        num2 = variables.monthFreq[user.id]
        num3 = variables.weekFreq[user.id]
        await bot.send_message(ctx.message.channel, user.mention + " " + str(num) + " total messages sent. " + str(num2) + " sent this month. " + str(num3) + " sent this week." )
    else:
        await bot.send_message(ctx.message.channel, user.mention + " you have been blacklisted from the leaderboard feature.")
async def user(bot, ctx):
    string = ctx.message.content.replace("!user", "").strip()
    await bot.say("http://www.reddit.com/u/" + string + '/overview')

async def sub(bot, ctx):
    string = ctx.message.content.replace("!sub", "").strip()
    await bot.say("http://www.reddit.com/r/" + string)
                  
async def blacklist(bot, ctx):
    string = ctx.message.content.replace("!blacklist", "").strip()
    perms = ctx.message.channel.permissions_for(ctx.message.author)
    if perms.manage_channels:
        if string.startswith("add"):
            parts = string.split(' ', 1)
            id = parts[1]
            member = discord.utils.find(lambda m: m.id == id, ctx.message.channel.server.members)
            variables.blacklist[id] = member.name
            await bot.say(member.name + " has been added to the blacklist.")
            saveConfig()
        elif string.startswith("remove"):
            parts = string.split(' ', 1)
            id = parts[1]
            name = variables.blacklist.pop(id, None)
            if name is None:
                  await bot.say("User not found in blacklist")
            else:
                  await bot.say("User removed from blacklist")
            saveConfig()
        elif string.startswith("list"):
            await bot.say(variables.blacklist)
async def logs(bot, ctx):
    string = ctx.message.content.replace("!logs", "").strip()
    today = datetime.datetime.now()
    if string.lower() == "month":
        variables.monthFreq = {}
        delt = timedelta(weeks = -4)
        d = today + delt
        async for message in bot.logs_from(ctx.message.channel, limit=2000000, after = d):
            try:
                variables.monthFreq[message.author.id] = variables.monthFreq[message.author.id] + 1
            except Exception:
                variables.monthFreq[message.author.id] = 0
        print("Done")
    elif string.lower() == "week":
        variables.weekFreq = {}
        delt = timedelta(weeks=-1)
        d = today + delt
        async for message in bot.logs_from(ctx.message.channel, limit=2000000, after=d):
            try:
                variables.weekFreq[message.author.id] = variables.weekFreq[message.author.id] + 1
            except Exception:
                variables.weekFreq[message.author.id] = 0
        print("Done")
    else:
        #variables.freq = {}
        #async for message in bot.logs_from(ctx.message.channel, limit= 2000000):
        #    try:
        #        variables.freq[message.author.id] = variables.freq[message.author.id] + 1
        #    except Exception:
        #        variables.freq[message.author.id] = 0
        print("Done")
    saveConfig()
    await bot.say("Finished Collecting Logs.")

async def leaders(bot, ctx):
    string = ctx.message.content.replace("!leaders", "").strip()
    ret = " #"
    list = []
    if string.lower() == "me":
        id = ctx.message.author.id
        if id in variables.blacklist:
            ret = " you have been blacklisted from the leaderboards feature."
            await bot.send_message(ctx.message.channel, ctx.message.author.mention + ret)
            return
        for key in variables.freq.keys():
            list.append((key, variables.freq[key]))
        list = sorted(list, key=lambda x: x[1], reverse=True)
        counter = 1
        for user in list:
            if user[0] == id:
                ret += str(counter) + " all time. #"
                break
            counter += 1
        list = []
        for key in variables.monthFreq.keys():
            list.append((key, variables.monthFreq[key]))
        list = sorted(list, key=lambda x: x[1], reverse=True)
        counter = 1
        for user in list:
            if user[0] == id:
                ret += str(counter) + " monthly. #"
                break
            counter += 1
        list = []
        for key in variables.weekFreq.keys():
            list.append((key, variables.weekFreq[key]))
        list = sorted(list, key=lambda x: x[1], reverse=True)
        counter = 1
        for user in list:
            if user[0] == id:
                ret += str(counter) + " weekly."
                break
            counter += 1
        await bot.send_message(ctx.message.channel, ctx.message.author.mention + ret)
        return
    elif string.lower() == "month":
        dict = variables.monthFreq
    elif string.lower() == "week":
        dict = variables.weekFreq
    else:
        dict = variables.freq
    for key in dict.keys():
        list.append((key, dict[key]))
    list = sorted(list, key=lambda x: x[1], reverse = True)
    counter = 0
    ten = []
    while len(ten) < 10:
        user = list[counter]
        for member in ctx.message.server.members:
            if member.id == user[0]:
                if member.id not in variables.blacklist:
                    ten.append((member.name,user[1]))
                break
        counter += 1
        #print(counter)
    string = ""
    counter = 1
    for user in ten:
        string += str(counter) + ". " + user[0] + ": " + str(user[1]) + "\n"
        counter += 1
    await bot.say(string)
async def join(bot, ctx):
    user = ctx.message.author
    date = user.joined_at
    await bot.send_message(ctx.message.channel, user.mention + " You last joined this server on " + variables.months[date.month] + str(date.day) + " " + str(date.year) + ".")
async def currency(bot, ctx):
    string = ctx.message.content.replace("!currency", "").strip()
    user = ctx.message.author
    perms = ctx.message.channel.permissions_for(user)
    if string is "":
        if user.id in variables.currency:
            await bot.send_message(ctx.message.channel, user.mention + " You have " + str(variables.currency[user.id]) + " credits.")
        else:
            variables.currency[user.id] = variables.currencyStart
            variables.wagers[user.id] = []
            saveConfig()
            await bot.send_message(ctx.message.channel, user.mention  + " You're a new better! You have been given " + str(variables.currencyStart) + " credits.")
    elif string.startswith("give") and perms.manage_channels:
        parts = string.split(' ', 1)
        val = int(parts[1])
        for key in variables.currency:
            variables.currency[key] += val
        saveConfig()
async def bet(bot, ctx):
    string = ctx.message.content.replace("!bet", "").strip()
    user = ctx.message.author
    perms = ctx.message.channel.permissions_for(user)
    if string is "":
        ret = ""
        counter = 0
        for bet in variables.bets:
            ret += "Event " + str(counter) + " : " + str(bet) + "\n"
            counter += 1
        if ret is "":
            ret = "No Active Bets."
        await bot.say(ret)
    elif string.startswith("add") and perms.manage_channels:
        parts = string.split(' ', 1)
        para = parts[1].split(',', 2)
        bet = Betting.Bet(para[0], para[1].strip(), para[2].strip())
        variables.bets.append(bet)
        saveConfig()
        await bot.say(bet)
    elif string[0].isdigit():
        bet = variables.bets[int(string[0])]
        parts = string.split(' ', 1)
        print(parts)
        para = parts[1].split(',', 2)
        print(para)
        amount = int(para[1].strip())
        if bet.closed:
            await bot.say("Bet is closed.")
            return
        if amount > variables.currency[user.id]:
            wager = None
        else:
            wager = bet.makeWager(user.id,para[0].strip(),amount)
        if wager is None:
            await bot.say(user.mention + " Error setting up wager." )
        else:
            variables.wagers[user.id].append(wager)
            saveConfig()
            await bot.say(user.mention + " Made wager for side " + para[0] + " with the amount " + str(amount) + ". You now have " + str(variables.currency[user.id]) + " credits left.")
    elif string.startswith("me"):
        try:
            list = variables.wagers[user.id]
        except KeyError:
            variables.wagers[user.id] = []
            list = variables.wagers[user.id]
        ret = ""
        for wager in list:
            ret += str(wager) + "\n"
        if ret is "":
            ret = "You have no wagers."
        await bot.say(user.mention + "\n" + ret)
    elif string.startswith("pay"):
        parts = string.split(' ', 1)
        parts = parts[1].split(' ', 1)
        index = int(parts[0])
        paid = variables.bets[index]
        results = paid.payout(parts[1].strip())
        if results is None:
            await bot.say("Error paying out bet.")
        elif results is []:
            await bot.say("Only one side has bets, refunds for all.")
        else:
            for result in results:
                money = variables.currency[result[0]]
                if result[1] is True:
                    money += result[2]
                else:
                    money -= result[2]
                variables.currency[result[0]] = money
            paid.delete()
            variables.bets.remove(paid)
            saveConfig()
            await bot.say("Bet Paid. Congratulations to the winners.")
    elif string.startswith("delete"):
        parts = string.split(' ', 1)
        index = int(parts[1])
        bet = variables.bets[index]
        bet.delete()
        variables.bets.remove(bet)
        saveConfig()
        await bot.say("Bet Deleted.")
    elif string.startswith("close"):
        parts = string.split(' ', 1)
        index = int(parts[1])
        bet = variables.bets[index]
        result = bet.close()
        if result is True:
            string = "Closed"
        else:
            string = "Open"
        await bot.say("Bet is " + string + ".")

async def modmail(bot):
    reddit = praw.Reddit(client_id=variables.client_id,
                client_secret=variables.client_secret,
                user_agent=variables.user_agent,
                username=variables.username,
                password=variables.password)
    mm = reddit.subreddit('OpTicGaming').modmail
    for msg in mm.conversations(state='all'):
        mail = msg.messages[0]
        if str(msg) not in variables.modMail:
            variables.modMail.append(str(msg))
            s  = 'New Modmail from: ' + mail.author.name + '\n'
            s += "ID = '" + str(msg) + "'\n"
            s += '\n'
            s += str(mail.body_markdown)
            await bot.send_message(variables.modMailChannel,s)
async def posts(bot):
    reddit = praw.Reddit(client_id=variables.client_id,client_secret=variables.client_secret,user_agent=variables.user_agent,username=variables.username,password=variables.password)
    subreddit = reddit.subreddit(variables.subreddit)
    temp = int(time.time() - 40)
    for submission in subreddit.submissions(start = variables.retrieveTime, end = temp):
        print(submission.created_utc)
        title = submission.title
        url = submission.url
        user = str(submission.author)
        id = submission.id  
        print(title)
        print(url)
        print(user)
        s = "**" + title + "** *by " + user + "*\n"
        s += "ID = '" + str(id) + "'\n"
        s += "User = http://www.reddit.com/u/" + user + '/overview\n'
        s += url + '\n'
        print(s)
        if id != variables.lastID:
            await bot.send_message(variables.postsChannel, s)
        variables.lastID = id
    variables.retrieveTime = temp
async def remove(bot, ctx):
    print('remove')
    if (ctx.message.channel.id != str(variables.postID)):
        return
    print('right channel')
    id = ctx.message.content.replace("!remove", "").strip()
    r = praw.Reddit(client_id=variables.client_id,
                client_secret=variables.client_secret,
                user_agent=variables.user_agent,
                username=variables.username,
                password=variables.password)
    if not id:
        await bot.say("No ID given.")
        return
    submission = r.submission(id=id)
    if submission.banned_by is not None:
        await bot.say("Thread already removed by: " + submission.banned_by)
        return
    url = submission.url
    try:
        submission.mod.remove()
        await bot.say("Thread Removed: " + url)
    except Exception:
        await bot.say("Error Removing Thread: " + url)
        
async def archive(bot, ctx):
    if (ctx.message.channel.id != str(variables.modMailChannelID)):
        return
    id = ctx.message.content.replace("!archive", "").strip()
    r = praw.Reddit(client_id=variables.client_id,
                client_secret=variables.client_secret,
                user_agent=variables.user_agent,
                username=variables.username,
                password=variables.password)
    if (id.lower() == 'all'):
        try:
            for mail in variables.modMail:
                r.subreddit('OpTicGaming').modmail(mail).archive()
            await bot.say('Archived all messages.')
        except Exception:
            pass
        return
    if len(variables.modMail) == 0:
        await bot.say('Nothing in Mod Mail')
        return
    if not id:
        id = variables.modMail[len(variables.modMail) - 1]
    try:
        r.subreddit('OpTicGaming').modmail(id).archive()
        variables.modMail.remove(id)
        await bot.say(id + ' has been archived.')
    except Exception:
        await bot.say('Invalid ID')


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
        variables.currency = json.loads(config[2])
        variables.counter = json.loads(config[3])
        variables.bets = jsonpickle.decode(config[4])
        variables.wagers = jsonpickle.decode(config[5])
        variables.freq = json.loads(config[6])
        variables.monthFreq = json.loads(config[7])
        variables.weekFreq = json.loads(config[8])
        variables.blacklist = json.loads(config[9])


        return True
    except Exception:
        return False

def saveConfig():
    seperation = "\r\n\r\n"
    try:
        txt = json.dumps(variables.textCommands)
        txt += seperation
        txt += json.dumps(variables.contentFilter)
        txt += seperation
        txt += json.dumps(variables.currency)
        txt += seperation
        txt += json.dumps(variables.counter)
        txt += seperation
        txt += jsonpickle.encode(variables.bets)
        txt += seperation
        txt += json.dumps(variables.blacklist)
        txt += seperation
        txt += json.dumps(variables.freq)
        txt += seperation
        txt += json.dumps(variables.monthFreq)
        txt += seperation
        txt += json.dumps(variables.weekFreq)
        txt += seperation
        txt += json.dumps(variables.blacklist)
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

