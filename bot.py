import asyncio

from discord.ext import commands

from tools import os_utils, permissions


bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def server_status(ctx):
    if os_utils.get_process():
        await ctx.send('Server is currently online')
    else:
        await ctx.send('Server is currently offline')

@bot.command()
async def server_start(ctx):
    if not permissions.authorized(ctx):
        await ctx.send('You are not authorized to use this command'.format(ctx.author))
        return
    if os_utils.get_process():
        await ctx.send('Server is already online')
        return

    os_utils.run_script('server_start.sh')
    await ctx.send('Starting the server'.format(ctx.author))
    await asyncio.sleep(3)
    if os_utils.get_process():
        await ctx.send('Server is online')
    else:
        await ctx.send('Server failed to start')



@bot.command()
async def test(ctx):
    if not permissions.authorized(ctx):
        await ctx.send('You are not authorized to use this command'.format(ctx.author))
        return
    await ctx.send('I heard you! {0}'.format(ctx.author))

bot.run(os_utils.get_env('DISCORD_TOKEN'))
