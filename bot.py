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
    await ctx.send('Starting the server')
    await asyncio.sleep(3)
    if os_utils.get_process():
        await ctx.send('Server is online')
    else:
        await ctx.send('Server failed to start')


@bot.command()
async def server_shutdown(ctx):
    if not permissions.authorized(ctx):
        await ctx.send('You are not authorized to use this command'.format(ctx.author))
        return
    if not os_utils.get_process():
        await ctx.send('Server is already offline')
        return

    os_utils.run_script('server_shutdown.sh')
    await ctx.send('Shutting down the server')
    await asyncio.sleep(3)
    if os_utils.get_process():
        await ctx.send('Server is online')
    else:
        await ctx.send('Server is offline')


@bot.command()
async def server_restart(ctx):
    if not permissions.authorized(ctx):
        await ctx.send('You are not authorized to use this command'.format(ctx.author))
        return

    if os_utils.get_process():
        os_utils.run_script('server_shutdown.sh')
        await ctx.send('Shutting down the server')
        await asyncio.sleep(3)
    if not os_utils.get_process():
        os_utils.run_script('server_start.sh')
        await ctx.send('Starting the server')
        await asyncio.sleep(3)
    if os_utils.get_process():
        await ctx.send('Server is online')
    else:
        await ctx.send('Server is offline')


@bot.command()
async def map_list(ctx):
    lines = os_utils.get_file('/home/steam/pavlovserver/Pavlov/Saved/Config/LinuxServer/Game.ini')
    # Keep all lines that start with MapRotation
    lines = [line for line in lines if line.startswith('MapRotation')]
    # TODO: Add html fetching and parsing for beautiful presentation
    msg = _create_map_list(lines)
    await ctx.send(msg)


@bot.command()
async def test(ctx):
    if not permissions.authorized(ctx):
        await ctx.send('You are not authorized to use this command'.format(ctx.author))
        return
    await ctx.send('I heard you! {0}'.format(ctx.author))


def _create_map_list(lines):
    url = 'https://steamcommunity.com/sharedfiles/filedetails/?id='
    msg = []
    for line in lines:
        try:
            ugc = line.split('UGC')[1].split('"')[0]
        except IndexError:
            ugc = None
        if ugc:
            msg.append('{line} | {url}{ugc}'.format(line=line, url=url, ugc=ugc))
        else:
            msg.append('{line}'.format(line=line))
    return '\n'.join(msg)

bot.run(os_utils.get_env('DISCORD_TOKEN'))
