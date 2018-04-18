import discord
from discord.ext import commands
import time
from __main__ import test, DataManager

aactivity = """
**>xp :** Checks your xp.
**>leaderboard :** Shows 3 people with most xp.
"""
sstaffactivity = """
**>xp :** Checks your xp.
**>leaderboard :** Shows 3 people with most xp.
**>announce :** Resets xp and shows people with most xp.
**>ignore <channelname> :** Makes specified channel not gain xp.
"""

rroles = """
**>add <@ user or id> <rolename> :** Adds a role to the user.
**>remove <@ user or id> <rolename> :** Removes a role from the user.
"""

vverif = """
**>verify <@ User> [reason] :** Verifies a user.
**>unverify <@ User> [reason] :** Unverifies a user.
**>verif cleanup :** Use this instead of any other clear in the welcome channel whatsoever thanks.
**>verif send :** For when you use a clear command in a channel you shouldn't've.
**>verif lockdown :** Stops everyone from being verified. It's a toggle so use it again to turn it off.
"""

cconfig = """
**>welcomechannel <channelname> :** Example <#422736408520687617>
**>setlogchannel <channelname> :** Example <#260864259330801674>
**>setrole <rolename> :** Example Unverified role.
**>sandbox <serverid> :** Sets the server in which sinbot should glance at when being told what to do.
"""

aart = """
**>artist <@ user or id> :** Makes a user an artist.
**>notartist <@ user or id> :** Removes a user from being an artist.
**>artblacklist add <@ user or id> [reason] :** Adds a user to an artist blacklist.
**>artblacklist remove <@ user or id> :** Removes a user from the artist blacklist.
**>artblacklist list :** Lists people in the blacklist.
"""

ppoints = """
**>addpoints [usermention or id] [points] :** This adds points to the mentioned user.
**>removepoints [usermention or id] [points] :** Same deal as before, but removes.
**>create [usermention or id] :** Adds a new user to the spreadsheet
**>points <user> :** Checks your points or someone else's points.
"""

regpoints = """
**>points <user> :** Checks your points or someone else's points.
"""


def ant_help(ctx):
    staff = discord.utils.get(ctx.author.roles, name='Staff')
    ca = discord.utils.get(ctx.author.roles, name='Challenge Approver')
    embed = discord.Embed(title="Sinbot's commands", color=ctx.author.color)
    if staff or ca:
        embed.add_field(name="__Role Commands!__", value=rroles)
    if staff:
        embed.add_field(name="__Configuration Commands!__", value=cconfig)
    if staff:
        embed.add_field(name="__Artist Commands!__", value=aart)
    if staff:
        embed.add_field(name="__Activity Commands!__", value=sstaffactivity)
    else:
        embed.add_field(name="__Activity Commands!__", value=aactivity)
    if ca:
        embed.add_field(name="__Point commands!__", value=ppoints)
    if ca is None:
        embed.add_field(name="__Point commands!__", value=regpoints)
    return embed


class General:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def _help(self, ctx):
        try:
            await ctx.send(embed=ant_help(ctx))
        except discord.errors.Forbidden:
            await ctx.author.send(embed=ant_help(ctx))
            await ctx.send("📬 | Sent it to you in DMs!")

    @commands.command()
    async def ping(self, ctx):
        before = time.monotonic()
        message = await ctx.send("Pinging...")
        await ctx.trigger_typing()
        ping = (time.monotonic() - before) * 1000
        ping = round(ping)
        await message.delete()
        await ctx.send(f"🏓 | My ping is **{ping}ms!**")

    async def on_member_join(self, member):
        if test:
            testsbk = discord.utils.get(self.bot.guilds, id=402197486317338625)
            channel = discord.utils.get(testsbk, id=431944465532321802)
        else:
            mainsbk = discord.utils.get(self.bot.guilds, id=257889450850254848)
            channel = discord.utils.get(mainsbk, id=257895860757725186)
        message = DataManager.read('data/general.json')['welcome']
        await channel.send(message + f"{member.mention}!")


def setup(bot):
    bot.remove_command('help')
    bot.add_cog(General(bot))
    print("Loaded General.")
