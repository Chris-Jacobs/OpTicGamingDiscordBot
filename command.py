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
import twitter
import db
from collections import deque
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

async def commands(bot):
    keys = list(variables.textCommands.keys())
    first = keys[:int(len(keys)/2)]
    second = keys[int(len(keys)/2):]
    await(bot.say(first))
    await(bot.say(second))

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
def twitterHelper(api, game, id = None, depth = 0):
    if depth == 3:
        return "Tweet not found or too old"
    tweets = api.GetUserTimeline(2303682049, max_id = id)
    for tweet in tweets:
        lower = tweet.text.lower()
        if("#whendoesopticplay" in lower and game.lower() in lower):
            link = "<https://twitter.com/OpTicUpdate/status/" + tweet.id_str + ">"
            date = tweet.created_at
            s = "```" + tweet.text + "```\n"
            s += date + "\n"
            s += link
            return s
    return twitterHelper(api, game, tweet.id, depth + 1)
async def when(bot, ctx):
    game = ctx.message.content.replace("!whendoesopticplay", "").strip()
    print(game)
    api = twitter.Api(consumer_key=variables.twitterKey,
                  consumer_secret=variables.twitterSecret,
                  access_token_key=variables.twitterToken,
                  access_token_secret=variables.twitterTokenSecret)
    await(bot.say(twitterHelper(api, game)))
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

async def leaders(bot, ctx):
    string = ctx.message.content.replace("!leaders", "").strip()
    me = False
    if string.startswith("me"):
        me = True
        string = string.replace("me", "").strip()
    date = "2016-01-01"
    now = datetime.datetime.now()
    if string.startswith("month"):
        td = timedelta(days = -30)
        date = (now + td).strftime("%Y-%m-%d %H:%M")
    elif string.startswith("week"):
        td = timedelta(days = -7)
        date = (now + td).strftime("%Y-%m-%d %H:%M")
    elif string.startswith("day"):
        td = timedelta(days = -1)
        date = (now + td).strftime("%Y-%m-%d %H:%M")
    elif string.startswith("year"):
        td = timedelta(days = -365)
        date = (now + td).strftime("%Y-%m-%d %H:%M")
    channels = ctx.message.channel_mentions
    if len(channels) == 0:
        channels = ctx.message.server.channels
    returnString = ""
    if not me:
        rankings = await db.getRankings(channels, date)
        i = 1
        for ranking in rankings:
            try:
                user = await bot.get_user_info(ranking[0])
                name = user.name
            except discord.NotFound:
                name = "Deleted User"
            s = "{rank}. {name}: {total}\n".format(rank = str(i), name = name, total = str(ranking[1]))
            returnString += s
            i += 1
    else:
        info = await db.getUserInfo(channels, date, ctx.message.author.id)
        returnString = ctx.message.author.mention + " you are currently rank {num} with {messages}".format(num=info[0], messages=info[1])
    await bot.say(returnString)
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
        mail = msg.messages[-1]
        if str(msg) not in variables.modMail:
            s  = 'New Modmail from: ' + mail.author.name + '\n'
            s += "ID = '" + str(msg) + "'\n"
            s += '\n'
            s += str(mail.body_markdown)
            if "Some dumbass didn't tag his thread." in mail.body_markdown:
                print('Not tagged')
                reddit.subreddit('OpTicGaming').modmail(str(msg)).archive()
                await bot.send_message(variables.postsChannel,s)
            else:
                variables.modMail.append(str(msg))
                await bot.send_message(variables.modMailChannel,s)
async def posts(bot):
    reddit = praw.Reddit(client_id=variables.client_id,client_secret=variables.client_secret,user_agent=variables.user_agent,username=variables.username,password=variables.password)
    subreddit = reddit.subreddit(variables.subreddit)
    d = deque()
    tempID = None
    for submission in subreddit.new(limit=15):
        title = submission.title
        url = submission.url
        user = str(submission.author)
        id = submission.id
        if tempID is None:
            tempID = id
        if id > variables.lastID:
            e = discord.Embed(
                title=title,
                url=url,
                description=submission.selftext,
                color=0x789E63)
            e.set_footer(text='/u/' + user + " - " + str(id))
            d.appendleft(e)
        else:
            break
    variables.lastID = tempID
    with open('id.txt', 'w') as f:
        f.write(variables.lastID)
    for e in d:
        await bot.send_message(variables.postsChannel, embed = e)
async def remove(bot, ctx):
    if (ctx.message.server.id != str(variables.serverID)):
        return
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
async def getThread(content, r):
    print(content)
    if len(content) == 6:
        try:
            submission = r.submission(id = content)
        except Exception:
            submission = None
    elif "reddit" in content or "redd.it" in content:
        try:
            submission = r.submission(url = content)
        except Exception:
            submission = None
    else:
        submission = None
    return submission
async def post(bot, ctx):
    if (ctx.message.server.id != str(variables.serverID)):
        return
    content = ctx.message.content.replace("!post", "").strip()
    r = praw.Reddit(client_id=variables.modClient,
                client_secret=variables.modSecret,
                user_agent=variables.user_agent,
                username=variables.modUsername,
                password=variables.modPassword)
    #get reddit
    submission = getThread(content, r)
    if submission is not None:
        title = submission.title
        body = submission.selftext
        print(title)
        try:
            newSubmission = r.subreddit(variables.subreddit).submit(title = title, selftext = body, send_replies = False)
            s = newSubmission.url + "\n"
            s += "ID = '" + newSubmission.id + "'"
            await bot.say(s)
        except Exception:
            await bot.say("Error Posting Thread")
        newSubmission.mod.sticky(state = True, bottom = True)
    else:
        await bot.say("Error Finding Thread")
async def postmatch(bot, ctx):
    if (ctx.message.server.id != str(variables.serverID)):
        return
    content = ctx.message.content.replace("!postmatch", "").strip()
    r = praw.Reddit(client_id=variables.modClient,
                client_secret=variables.modSecret,
                user_agent=variables.user_agent,
                username=variables.modUsername,
                password=variables.modPassword)
    submission = await getThread(content, r)
    print(submission)
    if submission is not None:
        title = submission.title.replace("Match", "Post-Match")
        newSubmission = r.subreddit('OpTicGamingSandbox').submit(title = title, selftext = "", send_replies = False)
        s = newSubmission.url + "\n"
        s += "ID = '" + newSubmission.id + "'"
        await bot.say(s)
        submission.mod.lock()
        
async def posttournament(bot,ctx):
    if (ctx.message.server.id != str(variables.serverID)):
        return
    content = ctx.message.content.replace("!posttournament", "").strip()
    
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
        wiki = r.subreddit(variables.subreddit).wiki['freetalk'].content_md
        variables.sayings =  wiki.split('\n')
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

