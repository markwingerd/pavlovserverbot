import asyncio

import discord

from tools import os_utils, permissions
from logparser import log_parser, current_players

GAME_INI = '/home/steam/pavlovserver/Pavlov/Saved/Config/LinuxServer/Game.ini'


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.log_parser = self.loop.create_task(log_parser())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.author.id == self.user.id or not message.content.startswith('!'):
            return
        elif message.content.startswith('!server'):
            await self.server_commands(message)
        elif message.content.startswith('!map'):
            await self.map_commands(message)
        elif message.content.startswith('!user'):
            await self.user_commands(message)

    async def server_commands(self, message):
        if message.content.startswith('!server status'):
            await self.server_status(message)
        elif message.content.startswith('!server start'):
            await self.server_start(message)
        elif message.content.startswith('!server shutdown'):
            await self.server_shutdown(message)
        elif message.content.startswith('!server restart'):
            await self.server_restart(message)

    async def map_commands(self, message):
        if message.content.startswith('!map list'):
            await self.map_list(message)
        elif message.content.startswith('!map remove'):
            # TODO: Add robust arg finder
            _, _, map_ = message.content.split(' ')
            await self.map_remove(message, map_)
        elif message.content.startswith('!map add'):
            # TODO: Add robust arg finder
            _, _, map_, mode = message.content.split(' ')
            await self.map_remove(message, map_, mode)

    async def user_commands(self, message):
        if message.content.startswith('!user report'):
            # TODO: Add robust arg finder
            _, _, minutes = message.content.split(' ')
            await self.user_report(message, minutes)


    async def server_status(self, message):
        if os_utils.get_process():
            await message.channel.send('Server is currently online')
        else:
            await message.channel.send('Server is currently offline')

    async def server_start(self, message):
        if not permissions.authorized(message.author):
            await message.channel.send('You are not authorized to use this command')
            return
        if os_utils.get_process():
            await message.channel.send('Server is already online')
            return

        os_utils.run_script('server_start.sh')
        await message.channel.send('Starting the server')

        await asyncio.sleep(3)
        if os_utils.get_process():
            await message.channel.send('Server is online')
        else:
            await message.channel.send('Server failed to start')

    async def server_shutdown(self, message):
        if not permissions.authorized(message):
            await message.channel.send('You are not authorized to use this command'.format(message.author))
            return
        if not os_utils.get_process():
            await message.channel.send('Server is already offline')
            return

        os_utils.run_script('server_shutdown.sh')
        await message.channel.send('Shutting down the server')
        await asyncio.sleep(3)
        if os_utils.get_process():
            await message.channel.send('Server is online')
        else:
            await message.channel.send('Server is offline')

    async def server_restart(self, message):
        if not permissions.authorized(message):
            await message.channel.send('You are not authorized to use this command'.format(message.author))
            return

        if os_utils.get_process():
            os_utils.run_script('server_shutdown.sh')
            await message.channel.send('Shutting down the server')
            await asyncio.sleep(3)
        if not os_utils.get_process():
            os_utils.run_script('server_start.sh')
            await message.channel.send('Starting the server')
            await asyncio.sleep(3)
        if os_utils.get_process():
            await message.channel.send('Server is online')
        else:
            await message.channel.send('Server is offline')

    async def map_list(self, message):
        lines = os_utils.get_file(GAME_INI)
        # Keep all lines that start with MapRotation
        lines = [line for line in lines if line.startswith('MapRotation')]
        # TODO: Add html fetching and parsing for beautiful presentation
        msg = _create_maps_string(lines)
        await message.channel.send(msg)

    async def map_remove(self, message, map_):
        if not permissions.authorized(message):
            await message.channel.send('You are not authorized to use this command'.format(message.author))
            return

        lines = os_utils.get_file(GAME_INI)
        lines = (l for l in lines if not (l.startswith('MapRotation') and map_ in l))
        os_utils.save_file(GAME_INI, lines)

    async def map_add(self, message, map_, mode='SND'):
        if not permissions.authorized(message):
            await message.channel.send('You are not authorized to use this command'.format(message.author))
            return

        lines = os_utils.get_file(GAME_INI)
        lines.append('MapRotation=(MapId="{map_}", GameMode="{mode}")'.format(map_=map_, mode=mode))
        os_utils.save_file(GAME_INI, lines)

    async def user_report(self, message, minutes):
        await message.channel.send('Reporting server users for the next {} minutes'.format(minutes))
        for i in range(int(minutes)):
            await asyncio.sleep(60)
            if len(current_players) > 1:
                await message.channel.send('{} are currently playing'.format(', '.join(p[0] for p in current_players)))
            elif len(current_players) == 1:
                await message.channel.send('{} is currently playing. PLZ JOIN HIM!!!11'.format(current_players[0][0]))
            else:
                await message.channel.send('No one is playing. please get Dave to support community servers')
        await message.channel.send('Reporting has ended')




    async def my_background_task(self):
        await self.wait_until_ready()
        counter = 0
        channel = self.get_channel(598643936290013237) # channel ID goes here
        while not self.is_closed():
            counter += 1
            await channel.send(counter)
            print(counter)
            await asyncio.sleep(1) # task runs every 60 seconds


client = MyClient()
client.run(os_utils.get_env('DISCORD_TOKEN'))
