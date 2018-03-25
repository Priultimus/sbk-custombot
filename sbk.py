import discord
import os
import traceback
import sys
from discord.ext import commands
import logging

logging.basicConfig(level=logging.INFO)

if sys.argv == ['sbk.py', '-test']:
    set = None
else:
    set = True

def update(a, b):
    with open("data.json", "r") as jsonFile:
        data = json.load(jsonFile)
    data[a] = b
    with open("data.json", "w") as jsonFile:
        json.dump(data, jsonFile)

def list_update(a, b):
    with open("data.json", "r") as jsonFile:
        data = json.load(jsonFile)
    data[a].append(b)
    with open("data.json", "w") as jsonFile:
        json.dump(data, jsonFile)

def delete(a):
    with open("data.json", "r") as jsonFile:
        data = json.load(jsonFile)
    del data[str(a)]
    with open("data.json", "w") as jsonFile:
        json.dump(data, jsonFile)

def read():
    with open("config.json") as f:
        stuff = json.load(f)
        return stuff

class Bot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print("Ready!")

    async def on_message(self, message):
        global set
        if set:
            try:
                if message.guild.id == 257889450850254848:
                    await self.process_commands(message)
                else:
                    pass
            except AttributeError:
                pass
        else:
            try:
                if message.guild.id == 409830718169022475:
                    await self.process_commands(message)
                else:
                    pass
            except AttributeError:
                pass
    async def on_command_error(self, ctx, error):

        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'❌ | {ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'❌ | {ctx.command} can not be used in Private Messages.')
            except:
                pass

        # For this error example we check to see where it came from...
     #   elif isinstance(error, commands.BadArgument):
     #       if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
     #           return await ctx.send('I could not find that member. Please try again.')

        # All other Errors not returned come here... And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

if not set:
    bot = Bot(command_prefix=">>", owner_id=286246724270555136)
else:
    bot = Bot(command_prefix=">", owner_id=286246724270555136)

bot.load_extension(f"modules.developer")
bot.load_extension(f"modules.roles")
bot.load_extension(f"modules.verification")
bot.load_extension("modules.artchannel")

if not set:
    print("--- Testing mode active! ----")
    print(os.environ)
bot.run('NNDIxNzk5MTA1ODU0MTc3Mjkw.DZlZ2A.S133LOSIrqi8iagpQoW6kFxT4mo')
