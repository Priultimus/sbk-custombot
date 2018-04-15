from discord.ext import commands
from __main__ import DataManager, Checks
import discord
# import time as t
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
                await asyncio.sleep(60)
                last_author[author.id] = 0
            else:
                return None
        except KeyError:
            if a is False:
                last_author[author.id] = 60
                messages = 15
                DataManager.write('data/xp.json', author.id, messages)
                asyncio.sleep(60)
                last_author[author.id] = 0
                return messages
            else:
                return None

    def get_xp(author):
        """Returns the XP of the author. Returns None if not avavilble."""
        try:
            xp = DataManager.read('data/xp.json')[str(author)]
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
    async def xp(self, ctx, user: discord.Member=None):
        """Gets the XP of a user."""
        if user is None:
            user = ctx.author
        if Manager.get_xp(user.id) is not None:
            if not user == ctx.author:
                await ctx.send(f"✅ | {user.mention}'s XP is: **{Manager.get_xp(user)}!**")
            else:
                await ctx.send(f"✅ | Your XP is: **{Manager.get_xp(user)}!**")
        else:
            await ctx.send("❌ | No XP!")

    @Checks.is_staff()
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
            print(sbk)
            member = discord.utils.get(sbk.members, id=int(user))
            print(member)
            if not c >= 4:
                z = Manager.get_xp(user)
                zz = DataManager.read('data/activity.json')['last-week']
                if zz and user in zz:
                    embed.add_field(name=member.name, value=f"🔥 XP: **{z}**")
                else:
                    embed.add_field(name=member.name, value=f"XP: **{z}**")

        await ctx.send(embed=embed)

    @commands.command()
    @Checks.is_staff()
    async def announce(self, ctx):
        DataManager.delete('data/activity.json', 'done')
        DataManager.write('data/activity.json', 'timeleft', 604800)
        DataManager.write('data/activity.json', 'done', False)
        users = DataManager.read('data/activity.json')['last-week']
        sbk = discord.utils.get(ctx.bot.guilds, id=257889450850254848)
        c = 0
        embed = discord.Embed(title='And here are the final results!',
                              color=ctx.author.color)
        for user, points in users.items():
            c += 1
            member = discord.utils.get(sbk.members, id=int(user))
            if not c >= 4:
                embed.add_field(name=f"{c}." + member.name,
                                value=f"XP: **{points}**",
                                inline=False)
        await ctx.send(embed=embed)
        # await ctx.send("Remember, only the top three get a custom!")

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id in DataManager.read('data/activity.json')['ignore-list']:
            return
        else:
            await Manager.xp_calc(message.author)


def setup(bot):
    print("Loaded Activity Tracker.")
    bot.add_cog(Tracker())
