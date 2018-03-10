import discord
import os
import sys
from discord.ext.commands import AutoShardedBot

class Bot(AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print("Ready!")

bot = Bot(command_prefix=">")

for file in os.listdir("modules"):
    if file.endswith(".py"):
        name = file[:-3]
bot.load_extension(f"modules.{name}")
bot.load_extension("modules.artchannel")
bot.run('NDIxNzk5MTA1ODU0MTc3Mjkw.DYSgdA.6yePajnmegaatmvhB9_9jn8-vmI')