import discord
from discord.ext import commands
import json

import os
import logging
from random import randint

def read():
    with open('data.txt') as json_file:
        data = json.load(json_file)

def updatejoin(join):
    with open("data.json", "r") as jsonFile:
        data = json.load(jsonFile)

    
    tmp = data[] 
    data["joining"] = join

    
    with open("config.json", "w") as jsonFile:
        json.dump(data, jsonFile)
class Points:
    """The SbK point system, reworked."""

    @commands.command()
    @commands.has_any_role("Staff", "Challenge Approver")
    async def addpoints(self, ctx, user:discord.Member, *points):
        if not points:
            await ctx.send("❌ | You didn't specify what points are required to be added.")
        else:
            points = ' '.join(points)
            points = int(points)
