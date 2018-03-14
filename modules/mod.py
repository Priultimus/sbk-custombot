import discord
from discord.ext import commands

class Mod:
    """Moderation commands."""

    @commands.command()
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
                            await member.add_roles(roles)
                            await ctx.send(f"✅ | Successfully added role `{roles.name}` to {member.mention}!")
                        else:
                            await ctx.send("❌ | That role is higher than your highest role!")
                    else:
                        await ctx.send("I couldn't find that role.")
                except discord.errors.Forbidden:
                    await ctx.send("❌ | I couldn't add that role because I am either too far below it or I do not have the permissions required to add it.")
                except Exception as e:
                    await ctx.send("❌ | An error in removing that role has occured, please contact <@!286246724270555136>.")
        else:
            await ctx.send("❌ | You lack the required permissions to execute this command.")


    @commands.command()
    async def remove(self, ctx, member:discord.Member, *roles):
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
                            await member.remove_roles(roles)
                            await ctx.send(f"✅ | Successfully removed role `{roles.name}` from {member.mention}!")
                        else:
                            await ctx.send("❌ | That role is higher than your highest role!")
                    else:
                        await ctx.send("I couldn't find that role.")
                except discord.errors.Forbidden:
                    await ctx.send("❌ | I couldn't remove that role because I am either too far below it or I do not have the permissions required to remove it.")
                except Exception as e:
                    await ctx.send("❌ | An error in adding that role has occured, please contact <@!286246724270555136>.")
        else:
            await ctx.send("❌ | You lack the required permissions to execute this command.")

def setup(bot):
    bot.add_cog(Mod())
    print("Loaded Mod.")
