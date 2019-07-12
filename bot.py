from discord.ext import commands

from tools import os_utils


bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def server_online(ctx):
    if os_utils.get_process():
        await ctx.send('Server is currently online')
    else:
        await ctx.send('Server is currently offline')

@bot.command()
async def test(ctx):
    await ctx.send('I heard you! {0}'.format(ctx.author))

bot.run(os_utils.get_env('DISCORD_TOKEN'))
