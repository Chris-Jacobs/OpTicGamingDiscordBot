import variables
import command
from discord.ext import commands
import praw

bot = commands.Bot(command_prefix='!', description="", pm_help= True)
bot.run(variables.token)
bot.