import discord
import requests
import re
import variables
regexString = ".*?twitch.tv\/(.*)"
url = variables.keys['StreamsBase']
async def command(bot, ctx):
    msg = ctx.message.content.replace("!twitch", "").strip()
    parts = msg.split(" ")
    perms = ctx.message.channel.permissions_for(ctx.message.author)
    if perms.manage_messages:
        if parts[0] == "follow":
            await follow(bot, parts[1:])
        elif parts[0] == "follows":
            await follows(bot)
        elif parts[0] == "unfollow":
            await unfollow(bot, parts[1:])    
    if parts[0] == "live":
        await live(bot)

async def follow(bot, streams):
    for stream in streams:
        if "twitch.tv" in stream:
            r = re.search(regexString, stream)
            stream = r.groups()[0]
        js = {"username": stream}
        r = requests.post(url + "/follow", json = js)
        if (r.status_code == 200):
            await bot.say("Added " + stream)
        else:
            await bot.say("Couldn't add " + stream)
async def follows(bot):
    r = requests.get(url + '/follow')
    await bot.say(r.json())
async def unfollow(bot, streams):
    for stream in streams:
        if "twitch.tv" in stream:
            r = re.search(regexString, stream)
            stream = r.groups()[0]
        js = {"username": stream}
        r = requests.post(url + "/unfollow", json = js)
        if (r.status_code == 200):
            await bot.say("Deleted " + stream)
        else:
            await bot.say("Couldn't delete " + stream)

async def live(bot):
    r = requests.get(url + '/live').json()
    print(r)
    fields = []
    livestreams = r['streams']
    e = discord.Embed (
        title = "OpTic Live Streams",
        color = 0x789E63
    )
    for stream in livestreams:
        link = "http://twitch.tv/" + stream['name']
        title = "{link} is playing **{game}** for **{viewers}** viewers".format(link = link, game = stream['game'], viewers = stream['viewers'])
        e.add_field(name = title, value = stream['title'], inline = False)
    e.set_footer(text = str(r['total_viewers']) + " total viewers")
    await bot.say(embed = e)