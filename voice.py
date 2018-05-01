import discord
import requests
import variables
async def create(bot, ctx, args):
    args = args.replace("create", "").strip()
    size = None
    if len(args) > 0:
        size = int(args)
    
    server = ctx.message.server
    url = "https://discordapp.com/api/v6/guilds/" + server.id + "/channels"
    payload = {
        'name': 'Voice',
        'type': 2,
        'parent_id': str(variables.voiceID),
    }
    print(payload)
    r = requests.post(url, headers = {"Authorization":"Bot " + bot.http.token}, json = payload)
    print(r.json()['id'])
    print(r.status_code)
    channel = discord.utils.get(server.channels, id=r.json()['id'])
    print(channel)
async def delete(bot):
    pass
async def main(bot, ctx):
    args = ctx.message.content.replace("!voice", "").strip()
    #print(discord.http)
    if args == "create":
        await create(bot, ctx, args)

