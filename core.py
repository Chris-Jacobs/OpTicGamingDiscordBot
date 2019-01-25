import discord
from discord.ext import commands
import variables
import command
import logging
import asyncio
import datetime
import queue
import time
import voice as v
import random
import db
import streams
#logger = logging.getLogger('discord')
#logger.setLevel(logging.DEBUG)
#handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
#handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#logger.addHandler(handler)

description = '''This may or not be right.'''

if not command.updateConfig():
    print("Configuration could not be loaded")
else:
    bot = commands.Bot(command_prefix='!', description=description, pm_help= True)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    if not variables.test:
        results = await db.getMaxes()
        for id, channelID in results:
            channel = bot.get_channel(channelID)
            if channel is None:
                continue
            msg = None
            while msg is None:
                try:
                    msg = await bot.get_message(channel, id)
                except discord.errors.NotFound:
                    print('found deleted message')
                    id = await db.getNew(id, channelID)
            async for message in bot.logs_from(channel, limit = 10000000000, after = msg.timestamp):
                data = (message.id, message.author.id, channel.id, message.content, message.timestamp)
                await db.addLog(data)
    print('done loading')
    server = discord.utils.get(bot.servers, id = str(variables.serverID))
    variables.modMailChannel = discord.utils.get(server.channels, id=str(variables.modMailChannelID))
    variables.postsChannel = discord.utils.get(server.channels, id=str(variables.postID))
    asyncio.ensure_future(modMail())
    if not variables.test:
        asyncio.ensure_future(posts())

@bot.command(pass_context= True, aliases =["Clear", "CLEAR"])
async def clear(ctx, num : int):
    await command.clear(bot, ctx, num)

@bot.command()
async def match():
    await command.match(bot)

@bot.command(pass_context = True, aliases = ["filter"])
async def contentFilter(ctx):
    await command.contentFilter(bot, ctx)

@bot.command(pass_context=True)
async def add(ctx):
    await command.add(bot, ctx)

@bot.command(aliases=["list"])
async def cmdlist():
    await command.commands(bot)

@bot.command(pass_context = True)
async def leaders(ctx):
    await command.leaders(bot, ctx)

@bot.command(pass_context = True)
async def commands(ctx):
    await command.help(bot, ctx)
@bot.command(pass_context = True)
async def edit(ctx):
    await command.edit(bot, ctx)

@bot.command(pass_context = True)
async def delete(ctx):
    await command.delete(bot, ctx)

@bot.command(pass_context = True)
async def update(ctx):
    await command.update(bot, ctx)

@bot.command(pass_context = True)
async def currency(ctx):
    await command.currency(bot, ctx)

@bot.command(pass_context = True)
async def bet(ctx):
    await command.bet(bot, ctx)
@bot.command(aliases =["Ddt", "DDT"])
async def ddt():
    await command.ddt(bot)
@bot.command(pass_context = True)
async def remove(ctx):
    await command.remove(bot, ctx)
@bot.command(pass_context = True)
async def post(ctx):
    await command.post(bot, ctx)
@bot.command(pass_context = True)
async def postmatch(ctx):
    await command.postmatch(bot, ctx)
@bot.command(pass_context = True)
async def posttournament(ctx):
    await command.posttournament(bot, ctx)
@bot.command(pass_context = True)
async def archive(ctx):
    await command.archive(bot, ctx)
@bot.command(pass_context = True)
async def blacklist(ctx):
    await command.blacklist(bot, ctx)
@bot.command(pass_context = True)
async def total(ctx):
    await command.total(bot, ctx)

@bot.command(pass_context = True)
async def twitch (ctx):
    await streams.command(bot, ctx)
@bot.command(pass_context = True)
async def user(ctx):
    await command.user(bot, ctx)

@bot.command(pass_context = True)
async def sub(ctx):
    await command.sub(bot, ctx)
@bot.command(pass_context = True)
async def joined(ctx):
    await command.join(bot, ctx)
@bot.command(pass_context = True, aliases=['wdop', 'WDOP'])
async def whendoesopticplay(ctx):
    await command.when(bot, ctx)
@bot.command(pass_context = True)
async def voice(ctx):
    await v.main(bot, ctx)
async def modMail():
     await bot.wait_until_ready()
     while not bot.is_closed:
         try:
             await command.modmail(bot)
         except Exception:
             pass
         await asyncio.sleep(60)
async def posts():
    await bot.wait_until_ready()
    while not bot.is_closed:
        try:
            await command.posts(bot)
        except Exception:
            pass
        await asyncio.sleep(60)
     
@bot.event
async def on_member_join(member):
    server = member.server
    #fmt = variables.textCommands['welcome']
    #fmt = fmt.replace("user", '0.mention')
    #fmt = fmt.strip("\"\"")
    saying = random.choice(variables.sayings).replace("\r", "")
    if saying[-1] == 's':
        saying = saying[:-1]
    s = member.mention + ", " + saying  + ". Make sure to read the rules of the server in <#155854416816242688>"
    await bot.send_message(server, s)
@bot.event
async def on_member_remove(member):
    server = member.server
    fmt = variables.textCommands['goodbye']
    fmt = fmt.replace("user", '0.mention')
    fmt = fmt.strip("\"\"")
    await bot.send_message(server, fmt.format(member))


@bot.event
async def on_message(message):
    msg = message.content
    data = (message.id, message.author.id, message.channel.id, message.content, message.timestamp)
    if message.server.id == "138430437637881856":
        await db.addLog(data)
    if bot.user in message.mentions:
        await bot.send_message(message.channel, "Go away.")
    if message.author.id != bot.user.id:
        if "block me back" in msg.lower():
            await bot.send_message(message.channel, message.author.mention + " Blocked Back.")
        if command.filterActive and not msg.startswith('!filter') and any(x in msg.lower() for x in variables.contentFilter) and "clips.twitch.tv" not in msg:
            variables.counter += 1
            await bot.delete_message(message)
            await bot.send_message(message.channel, message.author.mention + " you violated our content filter.")
            return
        if variables.dark:
            variables.purge.append(message)
        for cmd in variables.textCommands:
            if msg.rstrip() == ('!' + cmd):
                await bot.send_message(message.channel, variables.textCommands[cmd])
                return
        await bot.process_commands(message)

#@bot.event
#async def on_voice_state_update(before, after):
#    await v.change(bot, before, after)

bot.run(variables.token)
