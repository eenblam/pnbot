import os  # Pycharm says this import isn't doing anything.

import discord
import asyncio

from mapgen.mapgen import *
from dice.dice import *
from secrets import token


client = discord.Client()

LOCAL_STORAGE = "C:\\Users\\My Dell\\Google Drive\\MAP.png"  # When running pnbot locally, set this to desired file location.


@client.event
async def on_ready():
    s = 'Logged in as {} with {}'.format(client.user.name, client.user.id)
    print(s)


@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    elif message.content.startswith("!roll"):  # Example: "!roll 3d6".
        await client.send_message(message.channel, prepreparse(message.content[6:]))
    elif message.content.startswith("!map"):  # Example: "!map 400, 800".
        dimensions = message.content[5:].split(", ")
        await client.send_message(message.channel, "Building map, please wait...")
        save_to_image(
            delake(
                blur(
                    walk(
                        build(
                            map_parse(dimensions)
                        )
                    )
                )
            ), LOCAL_STORAGE
        )
        await client.send_file(message.channel, LOCAL_STORAGE)


client.run(token)
