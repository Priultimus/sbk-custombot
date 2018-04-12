from discord.ext import commands
from __main__ import DataManager
import discord
# import time as t
import datetime
from datetime import datetime as time
from functools import wraps

last_author = None


class Manager:
    """Management for activity tracker."""

    def log_time_of_use(fn):
        """Time of use decorator."""
        @wraps(fn)
        def callback(*args, **kwargs):
            callback._last_use_time = time.now()
            return fn(*args, **kwargs)
        callback._last_use_time = time.now()
        return callback

    @log_time_of_use
    def xp_calc(author):
        """Adds the XP to the author."""
        try:
            messages = DataManager.read('data/xp.json')[str(author.id)]
            print(messages)
            messages += 15
            DataManager.delete('data/xp.json', author.id)
            print("Deleted.")
            DataManager.write('data/xp.json', author.id, messages)
            print("Written.")
        except KeyError:
            print("KeyError.")
            messages = 15
            DataManager.write('data/xp.json', author.id, messages)
            return messages

    def get_xp(author):
        """Returns the XP of the author. Returns None if not avavilble."""
        try:
            xp = DataManager.read('data/xp.json')[str(author.id)]
            return xp
        except KeyError:
            return None

    def leaderboard():
        """Returns a list of the highest achievers this week."""
        x = DataManager.read('data/xp.json')
        return sorted(x, key=x.get, reverse=True)


class Tracker:
    """Activity tracking system."""

    @commands.command()
    async def xp(self, ctx):
        """Gets the XP of a user."""
        if Manager.get_xp(ctx.author) is not None:
            await ctx.send(Manager.get_xp(ctx.author))
        else:
            await ctx.send("No XP!")

    @commands.command()
    async def leaderboard(self, ctx):
        users = Manager.leaderboard()
        sbk = discord.utils.get(ctx.bot.guilds, id=257889450850254848)
        c = 0
        embed = discord.Embed(title='Sinbad Knights top three!',
                              color=ctx.author.color)
        for user in users:
            c += 1
            print(user)
            member = discord.utils.get(sbk.members, id=int(user))
            if not c >= 4:
                z = Manager.get_xp(member)
                embed.add_field(name=member.name, value=f"XP: **{z}**")
        await ctx.send(embed=embed)

    async def on_message(self, message):
        global last_author
        cooldown = datetime.timedelta(seconds=30)
        print("Message: " + str(message.author.id))
        print((time.now() - Manager.xp_calc._last_use_time) >= cooldown)
        if message.author == last_author:
            if (time.now() - Manager.xp_calc._last_use_time) >= cooldown:
                print("Writing!")
                Manager.xp_calc(message.author)
                last_author = message.author
        else:
            Manager.xp_calc(message.author)
            last_author = message.author


def setup(bot):
    print("Loaded Activity Tracker.")
    bot.add_cog(Tracker())
