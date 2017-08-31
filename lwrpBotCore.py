#!/usr/local/bin/python3

import discord
import asyncio
from discord.ext.commands import Bot
import math
import random
import sys

from server import *

startup_extensions = ["extensions.charSheets", "extensions.map", "extensions.combat"]

currentState = {'mapType'   :   0}

myBot = Bot(command_prefix="!")
server = discord.Server(id = serverID)

@myBot.command()
async def roll(*args):
    roll = math.floor(random.random() * 10) + 1
    return await myBot.say("Rolling 1d10{0}. Result: {1}{0}={2}".format(args[0], roll, roll + int(args[0])))

@myBot.command()
async def quit(*args):
    await myBot.say("Shutting down")
    sys.exit()
    
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            myBot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
 
    print("Bot ready")
myBot.run(serverToken)