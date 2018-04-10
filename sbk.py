import os
import traceback
import sys
import json
import discord
from discord.ext import commands
import logging
import platform

logging.basicConfig(level=logging.INFO)

test = True if platform.system() == 'Windows' or \
 sys.argv == ['sbk.py', '-test'] else None

key = "150qKj9o0BzYp1M5XzpyEuwQ7lkMJF-_9tWm0rnK5T8w" if test else \
 "1UHXrqeaapyCXv-xJV7YmA9r5c_6tjjS9t_55YJhIFVc"


class DataManager:
    def update(filename, a, b):
        with open(filename, "r") as jsonFile:
            data = json.load(jsonFile)
        data[a] = b
        with open(filename, "w") as jsonFile:
            json.dump(data, jsonFile)

    def write(filename, a, b):
        with open(filename, "r") as jsonFile:
            data = json.load(jsonFile)
        data[a] = b
        with open(filename, "w") as jsonFile:
            json.dump(data, jsonFile)

    def list_update(filename, a, b):
        with open(filename, "r") as jsonFile:
            data = json.load(jsonFile)
        data[a].append(b)
        with open(filename, "w") as jsonFile:
            json.dump(data, jsonFile)

    def delete(filename, a):
        with open(filename, "r") as jsonFile:
            data = json.load(jsonFile)
        del data[str(a)]
        with open(filename, "w") as jsonFile:
            json.dump(data, jsonFile)

    def read(filename):
        with open(filename) as f:
            stuff = json.load(f)
        return stuff


if sys.argv == ['sbk.py', '-test']:
    test = True
    DataManager.update('data/bot.json', 'SERVER', 402197486317338625)
else:
    test = None
    DataManager.update('data/bot.json', 'SERVER', 257889450850254848)


class Checks:
    def is_owner():
        async def pred(ctx):
            if ctx.author.id in DataManager.read('data/bot.json')['OWNERS']:
                return True
            else:
                return False
        return commands.check(pred)

    def is_staff():
        async def pred(ctx):
            role = discord.utils.get(ctx.author.roles, name='Staff')
            if role is not None:
                return True
            elif ctx.author.id in DataManager.read('data/bot.json')['OWNERS']:
                return True
            else:
                return False
        return commands.check(pred)

    def is_ca():
        async def pred(ctx):
            role = discord.utils.get(ctx.author.roles, name='Challenge Approver')
            if role is not None:
                return True
            elif ctx.author.id in DataManager.read('data/bot.json')['OWNERS']:
                return True
            else:
                return False
        return commands.check(pred)


class Bot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def restart(self):

        """Restarts the current program.

        Note: this function does not return. Any cleanup action (like

        saving data) must be done before calling this function."""

        python = sys.executable

        os.execl(python, python, * sys.argv)

    async def on_ready(self):
        print("Ready!")

    async def on_message(self, message):
        id = message.author.id
        try:
            if message.guild.id == DataManager.read('data/bot.json')['SERVER']:
                if message.author.bot:
                    return
                await self.process_commands(message)
        except AttributeError:
            if id in DataManager.read('data/bot.json')['OWNERS']:
                await self.process_commands(message)

    async def on_message_edit(self, before, after):
        if after.guild.id == DataManager.read('data/bot.json')['SERVER']:
                if after.author.bot:
                    return
            await self.process_commands(after)

    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, 'on_error'):
            return
        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'❌ | {ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f"""❌ | {ctx.command}
                cannot be used in Private Messages.""")
            except Exception as e:
                pass
        elif isinstance(error, discord.errors.Forbidden):
            await ctx.send(f"❌ | I lack the required permissions "
                           "to execute this command properly.")

        else:
            # if ctx.author.id in DataManager.read('data/bot.json')['OWNERS']:
            #    await ctx.author.send('Ignoring exception in command {}:'
            #                          .format(ctx.command), file=sys.stderr)
            print('Ignoring exception in command {}:'
                  .format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__,
                                  file=sys.stderr)


if test:
    bot = Bot(command_prefix=">>", owner_id=286246724270555136)
else:
    bot = Bot(command_prefix=">", owner_id=286246724270555136)

bot.load_extension(f"modules.dev")
bot.load_extension(f"modules.roles")
bot.load_extension(f"modules.verification")
bot.load_extension("modules.artchannel")
bot.load_extension("modules.challenges")
bot.load_extension("modules.help")
if test:
    print("--- Testing mode active! ----")


if __name__ == '__main__':
    bot.run('NDIxNzk5MTA1ODU0MTc3Mjkw.Davr_Q.xi9bDPK7vwUeS-JNugUM9c5oNyA')
