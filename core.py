import discord
from discord.ext import commands
import variables
import command




description = '''This may or not be right.'''

if not command.updateConfig():
    print("Configuration could not be loaded")
else:
    bot = commands.Bot(command_prefix='!', description=description, pm_help= True   )


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


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
    await command.list(bot)

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

#@bot.command()
#async def schedule():
#    await command.schedule(bot)

@bot.command(aliases =["Ddt", "DDT"])
async def ddt():
    await command.ddt(bot)

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
    if bot.user in message.mentions:
        await bot.send_message(message.channel, "Who am I banning?")
    if message.author.id != bot.user.id:
        if "block me back" in msg.lower():
            await bot.send_message(message.channel, message.author.mention + " Blocked Back.")
        if command.filterActive and not msg.startswith('!filter') and any(x in msg.lower() for x in variables.contentFilter):
            await bot.delete_message(message)
            await bot.send_message(message.channel, message.author.mention + " you violated our content filter.")
            return
        for cmd in variables.textCommands:
            if msg.startswith('!' + cmd):
                await bot.send_message(message.channel, variables.textCommands[cmd])
                return
        await bot.process_commands(message)

bot.run(variables.token)