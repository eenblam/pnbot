import os  # Pycharm says this import isn't doing anything.

import discord
import asyncio

from mapgen.mapgen import *
from dice.dice import *
from sneakrets.sneakrets import *
from secrets import token


client = discord.Client()

LOCAL_STORAGE = "C:\\Users\\My Dell\\Google Drive\\MAP.png"
# Used for temporarily storing randomly generated maps. When running pnbot locally, set this to your desired file location.

# TODO: v Set this up as a module v
def find_winner(bids):
    if len(bids) == 0:
        successful = False
        reason = "No bids were placed."
    else:
        best_bid = max([bids[x] for x in bids])
        winners = [x for x in bids if bids[x] == best_bid]
        if len(winners) == 1:
            successful = True
            reason = "The winner is **" + str(winners[0])[:-5] + "**, with a bid of " + str(best_bid) + "!"
        else:
            successful = False
            reason = "There was a tie.\n**" + str(winners[0])[:-5]
            for i in winners[1:]:
                reason += "**, **" + str(i)[:-5]
            reason += "** each bet *" + str(best_bid) + "*!"
    if successful:
        return [reason, winners[0], best_bid]
    else:
        return ["Auction failed: " + reason, 0]


MESSAGE_LOGS = {}
GOLD = {"Extra": 0, "pnbot#0050": 0}
# TODO: ^ All that, too ^


@client.event
async def on_ready():
    s = 'Logged in as {} with {}'.format(client.user.name, client.user.id)
    print(s)


@client.event
async def on_message(message):
    if str(message.author) not in GOLD.keys():
        GOLD[str(message.author)] = 100
        await client.send_message(message.author, "You've been allocated 100 Gold to spend on auctions.\nYou can check your current balance at any time with **!bank**.")
    if message.content.startswith("!help"):
        await client.send_message(message.channel, "Current commands include:\n\t!test\n\t!sleep\n\t!secret\n\t!roll\n\t!map")
    elif message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    elif message.content.startswith("!secret"):
        await client.send_message(message.author, sneakret())
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
    elif message.content.startswith("!bank"):
        await client.send_message(message.author, "Your current balance is:\t**" + str(GOLD[str(message.author)]) + " Gold**.")
    elif message.content.startswith("!wager"):
        if str(message.author) not in MESSAGE_LOGS.keys() or MESSAGE_LOGS[str(message.author)] == 0:
            await client.send_message(message.author, "No wager found.\n*Your current balance is " + str(GOLD[str(message.author)]) + " Gold.*")
        else:
            await client.send_message(message.author, "Your current wager is " + str(MESSAGE_LOGS[str(message.author)]) + " out of " + str(GOLD[str(message.author)]) + " Gold.")
    elif message.content.startswith("!eval"):
        try:
            await client.send_message(message.channel, str(eval(message.content[6:])))
        except:
            await client.send_message(message.channel, "Could not evaluate")
    elif message.content.startswith("!auction") and message.channel not in client.private_channels:
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
        if len(result) != 1:
            GOLD[result[1]] -= result[2]
            members = len(GOLD.keys()) - 3
            if members < 1:
                GOLD["Extra"] += result[2]
            else:
                spare = result[2] + GOLD["Extra"]
                GOLD["Extra"] = spare % members
                spare -= GOLD["Extra"]
                for i in GOLD.keys():
                    if i not in [result[1], "Extra", "pnbot#0050"]:
                        GOLD[i] += int(spare/members)
        for i in MESSAGE_LOGS.keys():
            MESSAGE_LOGS[i] = 0
        await client.send_message(message.channel, result[0])
    elif str(message.author) != "pnbot#0050" and message.channel in client.private_channels:
        try:
            MESSAGE_LOGS[str(message.author)] = min(GOLD[str(message.author)], max(0, int(message.content)))
        except:
            pass
        

client.run(token)
