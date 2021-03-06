import discord
from discord.ext import commands
import random
import time
from __main__ import test, DataManager

lockdown = False
sbk = None

if not test:
    enabled = True
    verifmsg = """**__Verification!__**
**~** In order to get verified you must do some things!
 1. Read <#429314209583726593>, because as soon as you're verified you swear under penalty of perjury that you read and agree to these rules.
 2. Do `>getcode` in order to have <@!421799105854177290> send you a DM! You must have DMs on. If you don't know how to don't worry.
 3. Enter the code Sinbot sent you here! And Sinbot'll verify you.
 4. If you were manually unverified (a staff did `>unverify` to you), you must reread <#429314209583726593> and then ping an online staff member to verify you."""
    roles = "Unverified"
    sandbox = 257889450850254848
    channel = 'welcome'
    log = 'staff-logs'
else:
    enabled = False
    verifmsg = "Testing mode is enabled."
    roles = 'UNVERIFED'
    channel = 'signup'
    log = 'logchannel'
    sandbox = 402197486317338625


users = {}


def logverify(message):
    embed = discord.Embed(colour=0x77B255, timestamp=message.created_at)
    embed.set_author(name="User Verified Successfully!", icon_url="https://i.imgur.com/SuDtnYE.png%22")
    embed.set_footer(text=f"ID:{message.author.id}")
    embed.set_thumbnail(url=message.author.avatar_url)
    embed.add_field(name="Member:", value=f"{message.author.name}#{message.author.discriminator}\n", inline=False)
    return embed


def mlogverify(member, message, mod, reason=None):
    embed = discord.Embed(colour=0x77B255, timestamp=message.created_at)
    embed.set_author(name="User Verified Successfully!", icon_url="https://i.imgur.com/SuDtnYE.png%22")
    embed.set_footer(text=f"ID:{member.id}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="Member:", value=f"{member.name}#{member.discriminator}\n", inline=False)
    embed.add_field(name="Staff Member:", value=f"{mod.name}#{mod.discriminator}\n", inline=False)
    if reason:
        embed.add_field(name="Reason:", value=reason, inline=False)
    return embed


def lunverify(member, message, mod, reason=None):
    embed = discord.Embed(colour=0xDD2E44, timestamp=message.created_at)
    embed.set_author(name="User Unverified!", icon_url="https://i.imgur.com/0owUvc3.png")
    embed.set_footer(text=f"ID:{member.id}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="Member:", value=f"{member.name}#{member.discriminator}\n", inline=False)
    embed.add_field(name="Staff Member:", value=f"{mod.name}#{mod.discriminator}\n", inline=False)
    if reason:
        embed.add_field(name="Reason:", value=reason, inline=False)
    return embed


def get_random():
    for i in random.sample(range(1000000, 9999999), 1):
        return i


class Verification:
    """The verification thing."""

    def __init__(self, bot):
        global sbk
        sbk = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def setrole(self, ctx, rolename: str):

        def find(rolename):
            for role in ctx.guild.roles:
                if role.name == rolename:
                    return role

        global roles
        if not find(rolename) is None:
            roles = rolename
            await ctx.send(f"✅ | Set the Unverified role to `{rolename}`!")
        else:
            await ctx.send(f"❌ | Couldn't find that role in this server.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def welcomechannel(self, ctx, cid):
        global channel

        def cfind(channel):
            for c in ctx.guild.channels:
                if c.name == channel:
                    return c
        r = cfind(cid)
        if r:
            channel = str(cid)
            await ctx.send(f"✅ | Set the Welcome channel to <#{r.id}>!")
        else:
            await ctx.send(f"❌ | Couldn't find that channel.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unverify(self, ctx, user: discord.Member, *reason):
        reason = ' '.join(reason)

        def find(rolename):

            for role in ctx.guild.roles:
                if role.name == rolename:
                    return role

        def cfind(channel):
            for c in ctx.guild.channels:
                if c.name == channel:
                    return c
        try:
            global roles
            global log
            global users
            role = find(str(roles))
            await user.add_roles(role)
            c = cfind(str(log))
            users[user.id] = 'N'
            await c.send(embed=lunverify(user, ctx.message, ctx.author, reason=reason))

            await ctx.send(f"⚠ | {user.mention} has just been unverified.")
        except Exception as e:
            await ctx.send(f"❌ | An error has occured.")
            raise e

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def setlogchannel(self, ctx, logch: str):
        global log

        def cfind(channel):
            for c in ctx.guild.channels:
                if c.name == channel:
                    return c

        r = cfind(logch)
        if r:
            log = logch
            await ctx.send(f"✅ | Set the Log channel to <#{r.id}>!")
        else:
            await ctx.send("❌ | Couldn't find that channel.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def verify(self, ctx, user: discord.Member, *reason):
        reason = ' '.join(reason)

        def find(rolename):
            for role in ctx.guild.roles:
                if role.name == rolename:
                    return role

        def cfind(channel):
            for c in ctx.guild.channels:
                if c.name == channel:
                    return c
        try:
            global roles
            global channel
            global users
            global log
            global verifmsg
            role = find(str(roles))
            await user.remove_roles(role)
            c = cfind(str(log))
            rr = cfind(str(channel))

            def is_me(m):
                return (m.author == user or m.author.bot) and ("Verification!" not in m.content)

            await rr.purge(limit=100, check=is_me)
            await ctx.message.delete()
            await c.send(embed=mlogverify(user, ctx.message, ctx.author, reason))
            try:
                await user.send("✅ | You've successfully been verified!")
            except Exception as e:
                pass
            users[user.id] = None
            await ctx.message.delete()
        except discord.errors.NotFound:
            users[user.id] = None
            pass
        except Exception as e:
            await ctx.send(f"❌ | An Error has occured.")
            raise e

    @commands.group(name="verif")
    @commands.has_permissions(ban_members=True)
    async def _verif(self, ctx):
        """Verification settings."""

        if ctx.invoked_subcommand is None:
            await ctx.send("The verification settings.")

    @_verif.command()
    @commands.has_permissions(ban_members=True)
    async def on(self, ctx):
        global enabled
        global roles
        global channel
        global log

        if roles is None:
            await ctx.send("❌ | Set the Unverified role before enabling verification!")
        elif channel is None:
            await ctx.send("❌ | Set the Welcome channel before enabling verification!")
        elif log is None:
            await ctx.send("❌ | Set the Log channel before enabling verification!")
        else:
            enabled = True
            await ctx.send("✅ | Enabled verification!")

    @_verif.command()
    @commands.has_permissions(ban_members=True)
    async def off(self, ctx):
        global enabled
        global roles
        global channel
        global log

        if roles is None:
            await ctx.send("❌ | Set the Unverified role before enabling verification!")
        elif channel is None:
            await ctx.send("❌ | Set the Welcome channel before enabling verification!")
        elif log is None:
            await ctx.send("❌ | Set the Log channel before enabling verification!")
        else:
            enabled = False
            await ctx.send("✅ | Disabled verification!")

    @_verif.command()
    @commands.has_permissions(ban_members=True)
    async def msg(self, ctx, *msg):
        global verifmsg
        if not msg:
            pass
        else:
            msg = '\n'.join(msg)
        if msg.lower() == 'null' or msg.lower() == 'null.':
            verifmsg = None
            await ctx.send("✅ | Cleared the verification message!")
        else:
            verifmsg = msg
            await ctx.send("✅ | Set the verification message!")

    @_verif.command()
    @commands.has_permissions(ban_members=True)
    async def cleanup(self, ctx, *count):
        def cfind(channel):
            for c in ctx.guild.channels:
                if c.name == channel:
                    return c
        global channel

        if ctx.channel != cfind(channel):
            await ctx.send("❌ | You can only clear messages in the welcome channel, not here.")
        else:
            global verifmsg
            if count:
                count = ' '.join(count)
                count = int(count)

                def eck(s):
                    if "Verification!" not in s.content:
                        return True
                    else:
                        return False

                await ctx.channel.purge(limit=count, check=eck)

            else:
                def eck(s):
                    if "Verification!" not in s.content:
                        return True
                    else:
                        return False
                await ctx.channel.purge(limit=100, check=eck)

    @_verif.command()
    @commands.has_permissions(ban_members=True)
    async def send(self, ctx):
        global verifmsg
        global channel
        a = await discord.utils.get(ctx.guild.channels, name=channel).send(verifmsg)
        await a.pin()

        def check(s):
            return "Verification!" not in s.content

        await a.channel.purge(limit=100, check=check)

    async def on_member_join(self, member):
        global sandbox
        try:
            if not member.guild.id == DataManager.read('data/bot.json')['SERVER']:
                pass
            else:
                await member.send("Hello!\nYou're in SbK or Sinbad :crossed_swords: Knights!\nYou should type \`>getcode` in the channel welcome. <#422736408520687617> <-- clickable.\nThen I'll send you some numbers and you can type those in the welcome place!\n:D")

                def find(rolename):
                    for role in member.guild.roles:
                        if role.name == rolename:
                            return role

                r = find(roles)
                await member.add_roles(r)
        except AttributeError:
            pass

    async def on_message_delete(self, message):
        if "Verification!" in message.content:
            global channel
            global verifmsg
            if message.channel == discord.utils.get(message.guild.channels, name=channel):
                b = discord.utils.get(message.guild.channels, name=channel)
                await b.purge(limit=100)
                a = await message.channel.send(verifmsg)
                await a.pin()

                def check(s):
                    return "Verification!" not in s.content

                await message.channel.purge(limit=100, check=check)

    async def on_message(self, message):
        global sandbox
        global lockdown

        try:
            if message.guild.id == sandbox:
                global channel

                def find(rolename):
                    for role in message.guild.roles:
                        if role.name == rolename:
                            return role

                def cfind(ch):
                    for c in message.guild.channels:
                        if c.name == ch:
                            return c

                chan = cfind(channel)

                if message.channel == chan:
                    global enabled
                    global users
                    global sbk
                    try:
                        users[message.author.id]
                    except KeyError:
                        users[message.author.id] = None
                    if enabled:
                        if message.content == '>getcode':
                            code = get_random()
                            try:
                                if users[message.author.id] == 'N' or lockdown == True:
                                    mmm = """⚠ | **You have been manually unverified.**\nPlease read <#425815476342489090> and ping an online staff member to be verified again."""
                                    await message.channel.send(mmm)

                                else:
                                    users[message.author.id] = str(code)
                                    try:
                                        await message.author.send(f"▶ | Use code `{code}` in <#{chan.id}> to authorize yourself!")
                                    except Exception as e:
                                        e = await message.channel.send(f"❌ | {message.author.mention}, I cannot DM you!")
                                        time.sleep(10)
                                        await e.delete()
                            except KeyError:
                                pass
                        elif str(message.content) == str(users[message.author.id]):
                            global roles
                            role = find(roles)
                            await message.author.remove_roles(role)
                            r = cfind(log)
                            rr = cfind(channel)

                            def is_me(m):
                                return (m.author == message.author or message.author.bot) and ("Verification!" not in m.content)

                            await rr.purge(limit=100, check=is_me)
                            await r.send(embed=logverify(message))
                            if not message.channel.permissions_for(message.author).value & 4 == 4:
                                if message.author.bot:
                                    pass
                                else:
                                    if users[message.author.id] == 'N' or lockdown:
                                        pass
                                    else:
                                        try:
                                            await message.delete()
                                        except Exception as e:
                                            pass
                            users[message.author.id] = None
                            print("Nin.")
                            await message.author.send("✅ | You've successfully been verified!")
                        else:
                            if not message.channel.permissions_for(message.author).value & 4 == 4:
                                if message.author.bot:
                                    pass
                                else:
                                    if users[message.author.id] == 'N':
                                        pass
                                    else:
                                        await message.delete()
                    else:
                        pass
                else:
                    pass
        except AttributeError:
            pass


def setup(bot):
    print("Loaded Verification.")
    n = Verification(bot)
    bot.add_cog(n)
