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
import asyncio
try:
    import uvloop
except Exception:
    loop = None
    pass
else:
    if platform.system() == 'Windows':
        loop = asyncio.new_event_loop()
    else:
        loop = uvloop.new_event_loop()

logging.basicConfig(level=logging.INFO)

test = True if platform.system() == 'Windows' or \
 sys.argv == ['sbk.py', '-test'] else None

key = "150qKj9o0BzYp1M5XzpyEuwQ7lkMJF-_9tWm0rnK5T8w" if test else \
 "1UHXrqeaapyCXv-xJV7YmA9r5c_6tjjS9t_55YJhIFVc"

try:
    uri = '127.0.0.1'
    client = MongoClient(uri)
    dbs = client['sinbot']
except Exception:
    print("Cannot connect to MongoDB, DataManager.db will NOT be supported.")


class CollectionNotFound(Exception):
    pass


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
            :param db: The collection in which you choose. Currently supported is hopefully all of them.
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

        def find(db, key, value):
            for collection in collections.__dict__['attrs']:
                if db == collection:
                    return(collections.__dict__[db].find_one({key: value}))
                else:
                    continue
            return('The db paramater isn\'t any collection in the database!')

        def save(db, toSave):
            for collection in collections.__dict__['attrs']:
                if db == collection:
                    return(collections.__dict__[db].save(toSave))
                else:
                    continue
            return("The DB paramater isn't any collection in the Database!")

        def delete(db, key, value):
            for collection in collections.__dict__['attrs']:
                if db == collection:
                    return(collections.__dict__[db].delete_one({key: value}))
                else:
                    continue
            return("The db paramater isn't any collection in the database!")

    def update(filename, a, b):
        with open(filename, "r", encoding="utf8") as jsonFile:
            data = json.load(jsonFile)
        data[a] = b
        with open(filename, "w", encoding="utf8") as jsonFile:
            json.dump(data, jsonFile)
        print(f"INFO:sbk.DataManager: Written {b} to {a}")

    def write(filename, a, b):
        with open(filename, "r", encoding="utf8") as jsonFile:
            data = json.load(jsonFile)
        data[a] = b
        with open(filename, "w", encoding="utf8") as jsonFile:
            json.dump(data, jsonFile)
        print(f"INFO:sbk.DataManager: Written {b} to {a}")

    def list_update(filename, a, b):
        with open(filename, "r", encoding="utf8") as jsonFile:
            data = json.load(jsonFile)
        if isinstance(a, int):
            a = str(a)
        data[a].append(b)
        with open(filename, "w", encoding="utf8") as jsonFile:
            json.dump(data, jsonFile)
        print(f"INFO:sbk.DataManager: Written {b} to {a} as a list")

    def list_remove(filename, a, b):
        with open(filename, "r", encoding="utf8") as jsonFile:
            data = json.load(jsonFile)
        if isinstance(a, int):
            a = str(a)
        data[a].remove(b)
        with open(filename, "w", encoding="utf8") as jsonFile:
            json.dump(data, jsonFile)
        print(f"INFO:sbk.DataManager: Deleted {b} from {a} as a list")

    def delete(filename, a):
        with open(filename, "r", encoding="utf8") as jsonFile:
            data = json.load(jsonFile)
        del data[str(a)]
        with open(filename, "w", encoding="utf8") as jsonFile:
            json.dump(data, jsonFile)
        print(f"INFO:sbk.DataManager: Deleted {a}")

    def read(filename):
        with open(filename, encoding="utf8") as f:
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


class Formatter:
    """Credits to Red for this formatter. Modified just the tiniest bit."""

    async def warning(ctx, text):
        await ctx.send(f"⚠ | {text}")

    async def error(ctx, text):
        await ctx.send(f"<:error:436279057416585217> | {text}")

    async def success(ctx, text):
        await ctx.send(f"<a:success:439322665568960512> | {text}")

    def bold(text):
        return f"**{text}**"

    def box(text, lang=""):
        ret = f"```{lang}\n{text}\n```"
        return ret

    def inline(text):
        return f"`{text}`"

    def italics(text):
        return f"*{text}*"

    def pagify(text, delims=["\n"], *, escape=True, shorten_by=8,
               page_length=2000):
        """DOES NOT RESPECT MARKDOWN BOXES OR INLINE CODE"""
        in_text = text
        if escape:
            num_mentions = text.count("@here") + text.count("@everyone")
            shorten_by += num_mentions
        page_length -= shorten_by
        while len(in_text) > page_length:
            closest_delim = max([in_text.rfind(d, 0, page_length)
                                 for d in delims])
            closest_delim = closest_delim if closest_delim != -1 else page_length
            if escape:
                to_send = escape_mass_mentions(in_text[:closest_delim])
            else:
                to_send = in_text[:closest_delim]
            yield to_send
            in_text = in_text[closest_delim:]

        if escape:
            yield escape_mass_mentions(in_text)
        else:
            yield in_text

    def strikethrough(text):
        return f"~~{text}~~"

    def underline(text):
        return f"__{text}__"


def escape(text, *, mass_mentions=False, formatting=False):
    if mass_mentions:
        text = text.replace("@everyone", "@\u200beveryone")
        text = text.replace("@here", "@\u200bhere")
    if formatting:
        text = (text.replace("`", "\\`")
                    .replace("*", "\\*")
                    .replace("_", "\\_")
                    .replace("~", "\\~"))
    return text


def escape_mass_mentions(text):
    return escape(text, mass_mentions=True)


class Bot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_exception = None
        self.logger = logging.getLogger(__name__)

    def restart(self):

        """Restarts the current program.

        Note: this function does not return. Any cleanup action (like

        saving data) must be done before calling this function."""

        python = sys.executable

        os.execl(python, python, * sys.argv)

    async def on_ready(self):
        modules = os.listdir('modules')
        modules.remove('__pycache__')
        for b in modules:
            try:
                b = "modules." + str(b.replace('.py', ''))
                if b == "modules.movies":
                    pass
                elif b == 'modules.votereact':
                    pass
                elif b == 'modules.music':
                    if test:
                        bot.load_extension(b)
                    else:
                        pass
                elif b == 'modules.activity':
                    if test:
                        pass
                    else:
                        bot.load_extension(b)
                else:
                    bot.load_extension(b)
            except Exception as error:
                log = (f"Exception in module '{b}'\n")
                log += "".join(traceback.format_exception(type(error), error,
                                                          error.__traceback__))
                self._last_exception = log
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
            return await Formatter.error(ctx, f"{ctx.command} has been disabled.")

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await Formatter.error(ctx, f"""❌ | {ctx.command}
                cannot be used in Private Messages.""")
            except Exception as e:
                pass
        elif isinstance(error, discord.errors.Forbidden):
            await Formatter.error(ctx, "I lack the required permissions "
                                  "to execute this command properly.")

        else:
            # if ctx.author.id in DataManager.read('data/bot.json')['OWNERS']:
            #    await ctx.author.send('Ignoring exception in command {}:'
            #                          .format(ctx.command), file=sys.stderr)
            log = ("Exception in command '{}'\n"
                   "".format(ctx.command.qualified_name))
            log += "".join(traceback.format_exception(type(error), error,
                                                      error.__traceback__))
            self._last_exception = log
            print('Ignoring exception in command {}:'
                  .format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__,
                                  file=sys.stderr)


if test:
    bot = Bot(command_prefix=">>>", loop=loop)
else:
    bot = Bot(command_prefix=">", loop=loop)

if test:
    print("--- Testing mode active! ----")


if __name__ == '__main__':
    bot.run('')
