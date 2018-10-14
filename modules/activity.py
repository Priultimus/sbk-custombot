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
    def __init__(self):
        self.name = 'name'

    def log_time_of_use(fn):
        """Time of use decorator."""
        @wraps(fn)
        def callback(*args, **kwargs):
            callback._last_use_time = time.now()
            return fn(*args, **kwargs)
        callback._last_use_time = time.now()
        return callback

    @log_time_of_use
    async def xp_calc(self, author):
        """Adds the XP to the author."""
        a = DataManager.read('data/activity.json')['done']
        global last_author
        try:
            last_author[author.id]
        except KeyError:
            last_author[author.id] = 0
        try:
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

    def get_xp(self, author):
        """Returns the XP of the author. Returns None if not avavilble."""
        try:
            xp = DataManager.read('data/xp.json')[str(author)]
            return xp
        except KeyError:
            return None

    def leaderboard(self):
        """Returns a list of the highest achievers this week."""
        x = DataManager.read('data/xp.json')
        return sorted(x, key=x.get, reverse=True)

    def rank(self, uid):
        """Returns a user's rank."""
        c = 0
        for a in self.leaderboard():
            c += 1
            if int(a) == int(uid):
                return c
                break
            else:
                continue


class Tracker:
    """Activity tracking system."""

    @commands.command(aliases=['rank', 'exp'])
    async def xp(self, ctx, user: discord.Member=None):
        m = Manager()
        """Gets the XP of a user."""
        if user is None:
            user = ctx.author
        exp = m.get_xp(user.id)
        xp = m.get_xp(ctx.author.id)
        catch_up = round((exp-xp))
        embed = discord.Embed(color=user.color)
        if not user == ctx.author:
            embed.set_author(name=user.name + "'s ranking statistics!",
                             icon_url=user.avatar_url)
        else:
            embed.set_author(name="Your ranking statistics!",
                             icon_url=user.avatar_url)
        if m.get_xp(user.id) is not None:
            if not user == ctx.author:
                embed.add_field(name='XP:', value="**"+str(exp)+"**")
                embed.add_field(name='Messages:', value="**"+str(int(exp/15))+"**")
                embed.add_field(name='Rank:', value="**"+str(m.rank(user.id))+"**")
                if not catch_up < 0:
                    embed.add_field(name=f"XP to catch up with {user.name}:",
                                    value=f"**{catch_up} (Messages: {round(catch_up/15)})**")
                await ctx.send(embed=embed)
            else:
                embed.add_field(name='XP:', value="**"+str(exp)+"**")
                embed.add_field(name='Messages:', value="**"+str(int(exp/15))+"**")
                embed.add_field(name='Rank', value="**"+str(m.rank(user.id))+"**")
                await ctx.send(embed=embed)
        else:
            await ctx.send("❌ | No XP!")

    @Checks.is_staff()
    @commands.command()
    async def ignore(self, ctx, channel: discord.TextChannel):
        DataManager.list_update('data/activity.json', 'ignore-list', channel.id)
        await ctx.send("Updated ignore list!")

    @commands.command(aliases=['lb', 'levels'])
    async def leaderboard(self, ctx):
        m = Manager()
        users = m.leaderboard()
        sbk = discord.utils.get(ctx.bot.guilds, id=257889450850254848)
        c = 0
        embed = discord.Embed(color=ctx.author.color)
        embed.set_author(name='Sinbad Knights Top Nine!',
                         icon_url=ctx.guild.icon_url)
        for user in users:
            c += 1
            member = discord.utils.get(sbk.members, id=int(user))
            if not c >= 11:
                z = m.get_xp(user)
                zz = DataManager.read('data/activity.json')['last-week']
                if member is not None:
                    if zz and user in zz:
                        if not c >= 4:
                            embed.add_field(name=f"{c}. "+ member.name, value=f"🔥 XP: **{z}**", inline=False)
                        else:
                            pass
                    else:
                        embed.add_field(name=f"{c}. "+ member.name, value=f"XP: **{z}**", inline=False)
                else:
                    c -= 1
                    continue
            else:
                break

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
        m = Manager()
        if message.author.bot:
            return
        if message.channel.id in DataManager.read('data/activity.json')['ignore-list']:
            return
        else:
            await m.xp_calc(message.author)


def setup(bot):
    bot.logger.info("Loaded Activity Tracker.")
    bot.add_cog(Tracker())
