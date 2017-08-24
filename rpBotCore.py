#!/usr/local/bin/python3

import discord
import asyncio
from discord.ext.commands import Bot

myBot = Bot(command_prefix="!")
server = discord.Server(id = 0)

myBot.run('')