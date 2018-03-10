import discord
from discord.ext import commands
import random
import time

enabled = True
roles = "UNVERIFIED"
sandbox = 402197486317338625
channel = 'signup'
log = 'logchannel'
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
    embed.set_author(name="User Unverified Successfully!", icon_url="https://i.imgur.com/0owUvc3.png")
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
        sbk = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def sandbox(self, ctx, guild_id:int):
        global sandbox
        sandbox = guild_id
        await ctx.send("✅ | I've successfully switched servers!")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def setrole(self, ctx, rolename:str):

        def find(rolename):
            for role in ctx.guild.roles:
                if role.name == rolename:
                    return role

        global roles
        if not find(rolename) == None:
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
            channel = cid
            await ctx.send(f"✅ | Set the Welcome channel to <#{r.id}>!")
        else:
            await ctx.send(f"❌ | Couldn't find that channel.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unverify(self, ctx, user:discord.Member, *reason):
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
            role = find(roles)
            await user.add_roles(role)
            c = cfind(log)
            await c.send(embed=lunverify(user, ctx.message, ctx.author, reason=reason))
            await ctx.send(f"⚠ | {user.mention} has just been unverified.")
        except Exception as e:
            await ctx.send(f"❌ | An error has occured.")
            raise e

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def setlogchannel(self, ctx, logch:int):
        global log

        def cfind(channel):
            for c in ctx.guild.channels:
                if c.name == channel:
                    return c

        r = discord.Object(logch)
        if r:
            log = r
            await ctx.send(f"✅ | Set the Log channel to <#{r.id}>!")
        else:
            await ctx.send("❌ | Couldn't find that channel.")
            
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def verify(self, ctx, user:discord.Member, *reason):
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
            global users
            global log
            role = find(roles)
            await user.remove_roles(role)
            c = cfind(log)
            await c.send(embed=mlogverify(user, ctx.message, ctx.author, reason))
            await user.send("✅ | You've successfully been verified!")
            users.pop(user.id, None)
            await ctx.send(f"✅ | {user.mention} has just been verified.")
        except Exception as e:
            await ctx.send(f"❌ | An Error has occured.")
            raise e

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def verif(self, ctx):
        global enabled
        global roles
        global channel 
        global log

        if enabled == False:
            if roles is None:
                await ctx.send("❌ | Set the Unverified role before enabling verification!")
            elif channel is None:
                await ctx.send("❌ | Set the Welcome channel before enabling verification!")
            elif log is None:
                await ctx.send("❌ | Set the Log channel before enabling verification!")
            else:
                enabled = True
                await ctx.send("✅ | Enabled verification!")
        else:
            enabled = False
            await ctx.send("✅ | Disabled verification!")


    async def on_member_join(self, member):
        global sandbox
        if not member.guild.id == sandbox:
            pass
        else:
            def find(rolename):
                for role in member.guild.roles:
                    if role.name == rolename:
                        return role

            r = find(roles)
            await member.add_roles(r)

    async def on_message(self, message):
        global sandbox
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
                if enabled == True:
                    try:
                        if message.content == '>getcode':
                            code = get_random()
                            global users
                            users[message.author.id] = str(code)
                            if not message.channel.permissions_for(message.author).value & 4 == 4:
                                await message.delete()
                            try:
                                await message.author.send(f"▶ | Use code `{code}` in <#{chan.id}> to authorize yourself!")
                            except discord.errors.Forbidden:
                                e = await message.channel.send(f"❌ | {message.author.mention}, I cannot DM you!")
                                time.sleep(5)
                                await e.delete()
                        elif message.content == users[message.author.id]:
                            global roles
                            role = find(roles)
                            await message.author.remove_roles(role)
                            r = cfind(log)
                            await r.send(embed=logverify(message))
                            if not message.channel.permissions_for(message.author).value & 4 == 4:
                                await message.delete()
                            users.pop(message.author.id, None)
                            await message.author.send("✅ | You've successfully been verified!")
                        else:
                            if not message.channel.permissions_for(message.author).value & 4 == 4:
                                await message.delete()
                    except KeyError:
                        if not message.channel.permissions_for(message.author).value & 4 == 4:
                            await message.delete()
                else:
                    pass        
            else:
                pass
            


def setup(bot):
    n = Verification(bot)
    bot.add_cog(n)
