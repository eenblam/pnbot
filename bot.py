import os  # Pycharm says this import isn't doing anything.

import discord
import asyncio

from mapgen.mapgen import *
from dice.dice import *
from sneakrets.sneakrets import *
from auction.auction import *
from secrets import token

client = discord.Client()

LOCAL_STORAGE = "C:\\Users\\My Dell\\Desktop\\MAP.png"  # When running pnbot locally, set this to desired file location.


MESSAGE_LOGS = {}
GOLD = {"pnbot#0050": 0}
BUSY = False


@client.event
async def on_ready():
    s = 'Logged in as {} with {}'.format(client.user.name, client.user.id)
    print(s)


@client.event
async def on_message(message):
    global BUSY
    if str(message.author) not in GOLD.keys():
        GOLD[str(message.author)] = 100
        await client.send_message(message.author, "You've been allocated 100 Gold to spend on auctions.\nYou can check your current balance at any time with **!bank**.")
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
        if BUSY:
            await client.send_message(message.channel, "I am currently busy. Please try again in a moment.")
        else:
            BUSY = True
            dimensions = message.content[5:].split(", ")
            await client.send_message(message.channel, "Building map, please wait...")
            generate(dimensions, LOCAL_STORAGE)
            await client.send_file(message.channel, LOCAL_STORAGE)
            BUSY = False
    elif message.content.startswith("!secret"):
        await client.send_message(message.author, sneakret())
    elif message.content.startswith("!eval"):
        try:
            await client.send_message(message.channel, str(eval(message.content[6:])))
        except:
            await client.send_message(message.channel, "Could not evaluate")
    elif message.content.startswith("!bank"):
        await client.send_message(message.author, "Your current balance is:\t**" + str(GOLD[str(message.author)]) + " Gold**.")
    elif message.content.startswith("!wager"):
        if str(message.author) not in MESSAGE_LOGS.keys() or MESSAGE_LOGS[str(message.author)] == 0:
            await client.send_message(message.author, "No wager found.\n*Your current balance is " + str(GOLD[str(message.author)]) + " Gold.*")
        else:
            await client.send_message(message.author, "Your current wager is " + str(MESSAGE_LOGS[str(message.author)]) + " out of " + str(GOLD[str(message.author)]) + " Gold.")
    elif message.content.startswith("!auction") and message.channel not in client.private_channels:
        if BUSY:
            await client.send_message(message.channel, "I am currently busy. Please try again in a moment.")
        else:
            BUSY = True
            try:
                for i in MESSAGE_LOGS:
                    MESSAGE_LOGS[i] = 0

                await client.send_message(message.channel, "**BEGINNING SECRET AUCTION!**\nPlease send me a direct message with your wager.")
                await asyncio.sleep(30)
                await client.send_message(message.channel, "30 seconds remaining.")
                await asyncio.sleep(20)
                await client.send_message(message.channel, "Auction closing in 10 seconds...")
                await asyncio.sleep(5)
                await client.send_message(message.channel, "5")
                await asyncio.sleep(1)
                await client.send_message(message.channel, "4")
                await asyncio.sleep(1)
                await client.send_message(message.channel, "3")
                await asyncio.sleep(1)
                await client.send_message(message.channel, "2")
                await asyncio.sleep(1)
                await client.send_message(message.channel, "1")
                await asyncio.sleep(1)
                result = find_winner(MESSAGE_LOGS)
                todo = redist(MESSAGE_LOGS, GOLD["pnbot#0050"])
                if len(result) != 1:
                    GOLD[result[1]] -= result[2]
                    GOLD["pnbot#0050"] = todo[1]
                    for x in todo[0]:
                        GOLD[x[0]] += x[1]
                else:
                    GOLD["pnbot#0050"] += result[2]
                for i in MESSAGE_LOGS.keys():
                    MESSAGE_LOGS[i] = 0
                await client.send_message(message.channel, result[0])
            finally:
                BUSY = False
    elif str(message.author) != "pnbot#0050" and message.channel in client.private_channels:
        try:
            author = str(message.author)
            balance = GOLD[author]
            requested_wager = int(message.content)
        except KeyError:
            await client.send_message(message.author, "Sorry, I couldn't find your balance.")
            return
        except ValueError:
            # Couldn't coerce content to int
            await client.send_message(message.author, "Sorry, I didn't undestand that. To participate in an auction, send a nonnegative integer as your wager.")
            return

        if requested_wager < 0:
            # Negative wagers are ignored.
            await client.send_message(message.author, "Sorry, I can't do much with a negative wager.")
            return
        if requested_wager > balance:
            MESSAGE_LOGS[author] = balance
            await client.send_message(message.author, "Sorry, you don't have enough for that. Using your available balance ({}). To cancel, send a \"0\"".format(balance))
            return

        #TODO kinda hairy having "MESSAGE_LOGS" that log something other than what was said
        MESSAGE_LOGS[author] = requested_wager
        await client.send_message(message.author, "Accepted wager of {}".format(requested_wager))


client.run(token)
