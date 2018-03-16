import discord
from discord.ext import commands
import json

def update(a, b):
    with open("config.json", "r") as jsonFile:
        data = json.load(jsonFile)
    data[a] = b
    with open("config.json", "w") as jsonFile:
        json.dump(data, jsonFile)

def delete(a):
    with open("config.json", "r") as jsonFile:
        data = json.load(jsonFile)
    del data[str(a)]
    with open("config.json", "w") as jsonFile:
        json.dump(data, jsonFile)

def read():
    with open("config.json") as f:
        blacklist = json.load(f)
        return blacklist

class Roles:
    """Role commands."""

    @commands.command()
    @commands.has_any_role('Staff')
    async def artist(self, ctx, member:discord.Member):
        role = discord.utils.get(ctx.guild.roles, name='Artist')
        if not str(member.id) in read():
            try:
                await member.add_roles(role, reason=f"[Artist command done by:{ctx.author.name}#{ctx.author.discriminator}]")
                await ctx.send(f"✅ | {member.mention} is now an artist!")
            except Exception as e:
                if ctx.author.id == 286246724270555136:
                    await ctx.send(f"❌ | Ignoring exception in command {ctx.command}:\n```py\n{e}\n```")
                else:
                    await ctx.send("❌ | An error has occured.")
        else:
            if read()[str(member.id)] != None:
                await ctx.send(f"⚠ | This user is Artist role blacklisted! Reason: {blacklist[member.id]}")
            else:
                await ctx.send(f"⚠ | This user is Artist role blacklisted!")

    @commands.command()
    @commands.has_any_role('Staff')
    async def notartist(self, ctx, member:discord.Member):
        role = discord.utils.get(ctx.guild.roles, name='Artist')
        try:
            await member.remove_roles(role, reason=f"[Artist command done by:{ctx.author.name}#{ctx.author.discriminator}]")
            await ctx.send(f"✅ | {member.mention} is no longer an artist!")
        except Exception as e:
            if ctx.author.id == 286246724270555136:
                await ctx.send(f"❌ | Ignoring exception in command {ctx.command}:\n```py\n{e}\n```")
            else:
                await ctx.send("❌ | An error has occured.")


    @commands.group(name='artblacklist')
    @commands.has_any_role("Staff")
    async def _artblacklist(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Artblacklist, blacklists a user with `>artblacklist add <@user>` or removes from said blacklist with `>artblacklist remove <@user>`.")

    @_artblacklist.command(aliases=['add'])
    @commands.has_any_role('Staff')
    async def addblacklist(self, ctx,member:discord.Member, reason=None):
        if not str(member.id) in read():
            if reason:
                update(member.id, reason)
                role = discord.utils.get(ctx.guild.roles, name='Artist')
                check = discord.utils.get(member.roles, name='Artist')
                if check:
                    await member.remove_roles(role, reason=f"[Blacklisted user {member.name}#{member.discriminator}]")
                await ctx.send(f"✅ | Successfully blacklisted {member.name}#{member.discriminator}.")
            else:
                role = discord.utils.get(ctx.guild.roles, name='Artist')
                check = discord.utils.get(member.roles, name='Artist')
                if check:
                    await member.remove_roles(role, reason=f"[Blacklisted user {member.name}#{member.discriminator}]")
                update(member.id, None)
                await ctx.send(f"✅ | Successfully blacklisted {member.name}#{member.discriminator}.")
        else:
            await ctx.send("❌ | That user is already blacklisted!")

    @_artblacklist.command(aliases=['remove'])
    @commands.has_any_role("Staff")
    async def removeblacklist(self, ctx,member:discord.Member, reason=None):
        if str(member.id) in read():
            delete(member.id)
            await ctx.send(f"✅ | Successfully removed {member.mention} from the blacklist.")
        else:
            await ctx.send("❌ | That user is not blacklisted!")

    @_artblacklist.command(aliases=['list'])
    @commands.has_any_role("Staff")
    async def _blacklist(self, ctx):
        a = ""
        for b in read():
            reason = read()[str(b)]
            member = discord.utils.get(ctx.bot.get_all_members(), id=int(b))
            a = a+f"**ID:** {member.id} - **Name:** {member.mention} {member.name}#{member.discriminator} - **Reason:** {reason}\n"
        try:
            await ctx.send(a)
        except discord.errors.HTTPException:
            await ctx.send("Nobody is blacklisted!")

    @commands.command(aliases=['addrole'])
    async def add(self, ctx, member:discord.Member, *roles):
        if (discord.utils.get(ctx.author.roles, name='Staff') != None or discord.utils.get(ctx.author.roles, name='Challenge Approver') !=None) or ctx.author.guild_permissions.value & 268435456  == 268435456 != True:
            if not roles:
                await ctx.send("You need to provide a role!")
            else:
                roles = ' '.join(roles)
                roles = discord.utils.get(ctx.guild.roles, name=roles)
                role_count = len(ctx.author.roles) - 1
                try:
                    if roles:
                        if ctx.author.roles[role_count] > roles:
                            await member.add_roles(roles, reason=f"[Command done by {ctx.author.name}#{ctx.author.discrimintao}")
                            await ctx.send(f"✅ | Successfully added role `{roles.name}` to {member.mention}!")
                        else:
                            await ctx.send("❌ | That role is higher than your highest role!")
                    else:
                        await ctx.send("❌ | I couldn't find that role.")
                except discord.errors.Forbidden:
                    await ctx.send("❌ | I couldn't add that role because I am either too far below it or I do not have the permissions required to add it.")
                except Exception as e:
                    await ctx.send("❌ | An error in removing that role has occured, please contact <@!286246724270555136>.")
        else:
            await ctx.send("❌ | You lack the required permissions to execute this command.")


    @commands.command(aliases=['removerole'])
    async def remove(self, ctx, member:discord.Member, *roles):
        if (discord.utils.get(ctx.author.roles, name='Staff') != None or discord.utils.get(ctx.author.roles, name='Challenge Approver') !=None) or ctx.author.guild_permissions.value & 268435456  == 268435456 != True:
            if not roles:
                await ctx.send("❌ | You need to provide a role!")
            else:
                roles = ' '.join(roles)
                roles = discord.utils.get(ctx.guild.roles, name=roles)
                role_count = len(ctx.author.roles) - 1
                try:
                    if roles:
                        if ctx.author.roles[role_count] > roles:
                            await member.remove_roles(roles)
                            await ctx.send(f"✅ | Successfully removed role `{roles.name}` from {member.mention}!")
                        else:
                            await ctx.send("❌ | That role is higher than your highest role!")
                    else:
                        await ctx.send("❌ | I couldn't find that role.")
                except discord.errors.Forbidden:
                    await ctx.send("❌ | I couldn't remove that role because I am either too far below it or I do not have the permissions required to remove it.")
                except Exception as e:
                    await ctx.send("❌ | An error in adding that role has occured, please contact <@!286246724270555136>.")
        else:
            await ctx.send("❌ | You lack the required permissions to execute this command.")

    async def on_member_update(self, before, after):
        try:
            role = discord.utils.get(after.guild.roles, name='Artist')
            if role in after.roles:
                if str(after.id) in read():
                    await after.remove_roles(role, reason=f"[Blacklisted user {after.name}#{after.discriminator}]")
        except Exception as e:
            raise e

def setup(bot):
    bot.add_cog(Roles())
    print("Loaded Roles.")
