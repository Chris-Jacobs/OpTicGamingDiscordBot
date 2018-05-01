import discord
from discord.ext import commands
import variables
import command
import logging
import asyncio
import chatlogs
import datetime
import queue
import time
import voice as v
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
    server = discord.utils.get(bot.servers, id = str(variables.serverID))
    variables.modMailChannel = discord.utils.get(server.channels, id=str(variables.modMailChannelID))
    variables.postsChannel = discord.utils.get(server.channels, id=str(variables.postID))
    #asyncio.ensure_future(logging())
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

@bot.command()
async def list():
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
async def archive(ctx):
    await command.archive(bot, ctx)
@bot.command(pass_context = True)
async def blacklist(ctx):
    await command.blacklist(bot, ctx)
@bot.command(pass_context = True)
async def logs(ctx):
    await command.logs(bot, ctx)

@bot.command(pass_context = True)
async def total(ctx):
    await command.total(bot, ctx)

@bot.command(pass_context = True)
async def user(ctx):
    await command.user(bot, ctx)

@bot.command(pass_context = True)
async def sub(ctx):
    await command.sub(bot, ctx)
@bot.command(pass_context = True)
async def join(ctx):
    await command.join(bot, ctx)
@bot.command(pass_context = True)
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
async def logging():
     await bot.wait_until_ready()
     current = datetime.date.today()
     while(True):
         counter = 0
         while counter < 3:
             counter += 1
             date = datetime.date.today()
             if(current.day != date.day):
                 for log in logs:
                     await variables.logs[log].writeToFile()
                     await variables.logs[log].uploadFile()
                 variables.logs = {}
                 current = date
                 break
             await asyncio.sleep(10)
             for log in variables.logs:
                 print("Writing to Files")
                 await variables.logs[log].writeToFile()
         for log in variables.logs:
             pass
             #await variables.logs[log].uploadFile()
     #google drive upload
     
@bot.event
async def on_member_join(member):
    server = member.server
    fmt = variables.textCommands['welcome']
    fmt = fmt.replace("user", '0.mention')
    fmt = fmt.strip("\"\"")
    await bot.send_message(server, fmt.format(member))

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
    #if message.author.id == '186866281465643008':
        #await bot.add_reaction(message,'🇱')
    #variables.messages.put(message)
    #if variables.logging is False:
        #asyncio.ensure_future(chatlogs.log())
    try:
        variables.freq[message.author.id] = variables.freq[message.author.id] + 1
    except KeyError:
        variables.freq[message.author.id] = 0
    try:
        variables.monthFreq[message.author.id] = variables.monthFreq[message.author.id] + 1
    except KeyError:
        variables.monthFreq[message.author.id] = 0
    try:
        variables.weekFreq[message.author.id] = variables.weekFreq[message.author.id] + 1
    except KeyError:
        variables.weekFreq[message.author.id] = 0
    if bot.user in message.mentions:
        await bot.send_message(message.channel, "You tryna start something?")
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
            if msg.startswith('!' + cmd):
                await bot.send_message(message.channel, variables.textCommands[cmd])
                return
        await bot.process_commands(message)

bot.run(variables.token)
