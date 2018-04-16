import os
import traceback
import sys
import json
from pymongo import MongoClient
import discord
import threading
from discord.ext import commands
import logging
import platform

logging.basicConfig(level=logging.INFO)

test = True if platform.system() == 'Windows' or \
 sys.argv == ['sbk.py', '-test'] else None

key = "150qKj9o0BzYp1M5XzpyEuwQ7lkMJF-_9tWm0rnK5T8w" if test else \
 "1UHXrqeaapyCXv-xJV7YmA9r5c_6tjjS9t_55YJhIFVc"

try:
    uri = '127.0.0.1'
    client = MongoClient(uri)
    dbs = client['Sinbot']
except:
    print("Cannot connect to MongoDB, DataManager.db will NOT be supported.")


class collections():
    attrs = dbs.collection_names()
    for attr in attrs:
        value = getattr(dbs, attr)
        locals()[attr] = value


class DataManager:

    class db():
        """Database class.
        Currently supports only certain data inputs.
        """
        def __init__(self):
            threading.Thread.__init__(self)

        def insert(types, db, key=None, value=None, **kwargs):
            """Insert a document into the mongodb collection of your choosing.
            :param types: The type of document you are trying to insert. Currently supported is str, int, array and object.
            :param db: The collection in which you choose. Currently supported is guilds, settings and eco.
            :param key: A paramater only used in object.
            :param value: Also only used in object.
            :param kwargs: The name of the document you choose to insert. Like name="name-of-document" or home="way-to-home."
            """

            if types == "str":
                for k, v in kwargs.items():
                    str(k)
                    str(v)
                    for collection in collections.__dict__['attrs']:
                        if db == collection:
                            return(collections.__dict__[db].insert_one({k: v}))
                        else:
                            continue
                    return('The db paramater isn\'t any collection in the database!')

            elif types == "int":
                for k, v in kwargs.items():
                    str(k)
                    int(v)
                    for collection in collections.__dict__['attrs']:
                        if db == collection:
                            return(collections.__dict__[db].insert_one({k: v}))
                        else:
                            continue
                return('The db paramater isn\'t any collection in the database!')

            elif types == "array":
                for k, v in kwargs.items():
                    if isinstance(v, list):
                        for collection in collections.__dict__['attrs']:
                            if db == collection:
                                return(collections.__dict__[db].insert_one({k: v}))
                            else:
                                continue
                        return('The db paramater isn\'t any collection in the database!')
                    else:
                        arr = []
                        arr.append(v)
                        for collection in collections.__dict__['attrs']:
                            if db == collection:
                                return(collections.__dict__[db].insert_one({k: arr}))
                            else:
                                continue
                        return('The db paramater isn\'t any collection in the database!')

            elif types == "object":
                for k, v in kwargs.items():

                    for collection in collections.__dict__['attrs']:
                        if db == collection:
                            return(collections.__dict__[db].insert_one({k: create_object(key, value)}))
                        else:
                            continue
                    return('The db paramater isn\'t any collection in the database!')

            else:
                return("Oops, that's not a type.")

        def find(db, name):
            for collection in collections.__dict__['attrs']:
                if db == collection:
                    return(collections.__dict__[db].find_one({'name': name}))
                else:
                    continue
            return('The db paramater isn\'t any collection in the database!')

        def delete(db, name):
            for collection in collections.__dict__['attrs']:
                if db == collection:
                    return(collections.__dict__[db].delete_one({'name': name}))
                else:
                    continue
            return("The db paramater isn't any collection in the database!")

    def update(filename, a, b):
        with open(filename, "r") as jsonFile:
            data = json.load(jsonFile)
        data[a] = b
        with open(filename, "w") as jsonFile:
            json.dump(data, jsonFile)
        print(f"INFO:sbk.DataManager: Written {b} to {a}")

    def write(filename, a, b):
        with open(filename, "r") as jsonFile:
            data = json.load(jsonFile)
        data[a] = b
        with open(filename, "w") as jsonFile:
            json.dump(data, jsonFile)
        print(f"INFO:sbk.DataManager: Written {b} to {a}")

    def list_update(filename, a, b):
        with open(filename, "r") as jsonFile:
            data = json.load(jsonFile)
        if isinstance(a, int):
            a = str(a)
        data[a].append(b)
        with open(filename, "w") as jsonFile:
            json.dump(data, jsonFile)
        print(f"INFO:sbk.DataManager: Written {b} to {a} as a list")

    def delete(filename, a):
        with open(filename, "r") as jsonFile:
            data = json.load(jsonFile)
        del data[str(a)]
        with open(filename, "w") as jsonFile:
            json.dump(data, jsonFile)
    print(f"INFO:sbk.DataManager: Deleted {a}")

    def read(filename):
        with open(filename) as f:
            stuff = json.load(f)
        return stuff
        print(f"INFO:sbk.DataManager: Read {filename}")


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
        after = message
        x = DataManager.read('data/bot.json')['OWNERS']
        y = DataManager.read('data/bot.json')['SERVER']
        if not message.guild:
            if message.author.id in x:
                await self.process_commands(message)
            print(f"{str(message.author)}: {message.content}")
            return
        else:
            try:
                role = discord.utils.get(after.author.roles, name='Sinbot fan club')
                s = discord.utils.get(after.author.roles, name='Staff')
            except AttributeError:
                return

            if (after.guild.id == y) or (role is not None) or (s is not None):
                    if after.author.bot:
                        return
                    else:
                        await self.process_commands(after)

    async def on_message_edit(self, before, after):
        try:
            role = discord.utils.get(after.author.roles, name='Sinbot fan club')
            s = discord.utils.get(after.author.roles, name='Staff')
        except AttributeError:
            return
        x = DataManager.read('data/bot.json')['OWNERS']
        y = DataManager.read('data/bot.json')['SERVER']
        if (not after.guild) and (after.author.id not in x):
            return

        elif (after.guild.id == y) or (role is not None) or (s is not None):
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
bot.load_extension("modules.movie")
if test:
    bot.load_extension(f"modules.activity")
    print("--- Testing mode active! ----")


if __name__ == '__main__':
    bot.run('NDIxNzk5MTA1ODU0MTc3Mjkw.DbOkLQ.RSly_UvQGU8zrhofWN8gC6EBx6U')
