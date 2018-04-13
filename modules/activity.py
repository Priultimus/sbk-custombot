from discord.ext import commands
from __main__ import DataManager
import discord
# import time as t
import datetime
from datetime import datetime as time
from functools import wraps
import asyncio

last_author = {}


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
    async def xp_calc(author):
        """Adds the XP to the author."""
        a = DataManager.read('data/activity.json')['done']
        try:
            global last_author
            if a is False and last_author[author.id] == 0:
                messages = DataManager.read('data/xp.json')[str(author.id)]
                messages += 15
                DataManager.delete('data/xp.json', author.id)
                DataManager.write('data/xp.json', author.id, messages)
                last_author[author.id] = 60
                asyncio.sleep(60)
                last_author[author.id] = 0
            else:
                return None
        except KeyError:
            if a is False:
                messages = 15
                DataManager.write('data/xp.json', author.id, messages)
                return messages
            else:
                return None

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
    async def ignore(self, ctx, channel: discord.TextChannel):
        DataManager.list_update('data/activity.json', 'ignore-list', channel.id)
        await ctx.send("Updated ignore list!")

    @commands.command()
    async def leaderboard(self, ctx):
        users = Manager.leaderboard()
        sbk = discord.utils.get(ctx.bot.guilds, id=257889450850254848)
        c = 0
        embed = discord.Embed(title='Sinbad Knights top three!',
                              color=ctx.author.color)
        for user in users:
            c += 1
            member = discord.utils.get(sbk.members, id=int(user))
            if not c >= 4:
                z = Manager.get_xp(member)
                zz = DataManager.read('data/activity.json')['last-week']
                if zz and user in zz:
                    embed.add_field(name=member.name, value=f"XP: **{z}**🔥")
                else:
                    embed.add_field(name=member.name, value=f"XP: **{z}**")

        await ctx.send(embed=embed)

    @commands.command()
    async def announce(self, ctx):
        DataManager.delete('data/activity.json', 'done')
        DataManager.write('data/activity.json', 'done', False)
        users = Manager.leaderboard()
        sbk = discord.utils.get(ctx.bot.guilds, id=257889450850254848)
        c = 0
        embed = discord.Embed(title='And here are the final results!',
                              color=ctx.author.color)
        for user in users:
            c += 1
            member = discord.utils.get(sbk.members, id=int(user))
            if not c >= 11:
                z = Manager.get_xp(member)
                embed.add_field(name=f"{c}." + member.name,
                                value=f"XP: **{z}**",
                                inline=False)
        await ctx.send(embed=embed)
        await ctx.send("Remember, only the top three get a custom!")

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id in DataManager.read('data/activity.json')['ignore-list']:
            return
        cooldown = datetime.timedelta(minutes=1)
        if message.author == last_author:
            if (time.now() - Manager.xp_calc._last_use_time) >= cooldown:
                await Manager.xp_calc(message.author)
            else:
                return
        else:
            await Manager.xp_calc(message.author)


def setup(bot):
    print("Loaded Activity Tracker.")
    bot.add_cog(Tracker())