import os

import discord
import asyncio

from mapgen import *  # Did I set up the module correctly?
from dice import *
from secrets import token


client = discord.Client()

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
        DICEROLL = preparse(message.content[6:])
        RESULTS = "Rolled a " + str(DICEROLL[0]) + ", " +str(DICEROLL[1])
        await client.send_message(message.channel, RESULTS)
    elif message.content.startswith("!map"):  # Example: "!map 400, 800".
        DIMENSIONS = message.content[5:].split(", ")
        save_to_image(delake(blur(walk(build(int(DIMENSIONS[0]), int(DIMENSIONS[1]))))), OUTPUT_LOCATION="C:\\Users\\My Dell\\Desktop\\", OUTPUT_FILE_NAME="Map")  # ! The Pillow module, and by extension mapgen, requires a file destination by default. I'll need help setting it up/changing it to store to a database. Alternatively, the bot could only bother storing one map at a time, long enough to post it, leaving the more long-term storage to Discord and/or a secondary bot.
        # await client.post_image(IMAGE_LOCATION)  # ! Dummy function. I'll be surprised if post_image() is an actual thing.
        
client.run(token)
