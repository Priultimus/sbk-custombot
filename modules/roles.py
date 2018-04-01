import discord
from discord.ext import commands
import emoji
from __main__ import DataManager, Checks


def lunverify(member, message, mod, reason=None):
    embed = discord.Embed(colour=0xDD2E44, timestamp=message.created_at)
    embed.set_author(name="User Art blacklisted!",
                     icon_url="https://i.imgur.com/0owUvc3.png")
    embed.set_footer(text=f"ID:{member.id}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="Member:",
                    value=f"{member.name}#{member.discriminator}\n",
                    inline=False
                    )
    embed.add_field(name="Staff Member:",
                    value=f"{mod.name}#{mod.discriminator}\n",
                    inline=False
                    )
    if reason:
        embed.add_field(name="Reason:", value=reason, inline=False)
    return embed


class Roles:
    """Role commands."""

    @commands.command()
    @commands.has_any_role('Staff')
    async def artist(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name='Artist')
        if not str(member.id) in DataManager.read('data/artblacklist.json'):
            try:
                await member.add_roles(role, reason=f"[Artist command executed"
                                       f" by:{ctx.author.name}#"
                                       f"{ctx.author.discriminator}]")
                await ctx.send(f"✅ | {member.mention} is now an artist!")
            except Exception as e:
                if ctx.author.id == 286246724270555136:
                    await ctx.send(f"❌ | Ignoring exception in command "
                                   f"{ctx.command}:\n```py\n{e}\n```")
                else:
                    await ctx.send("❌ | An error has occured.")
        else:
            ap = DataManager.read('data/artblacklist.json')[str(member.id)]
            if not ap:
                blacklist = DataManager.read('data/artblacklist.json')
                await ctx.send(f"⚠ | This user is Artist role blacklisted! "
                               f"Reason: {blacklist[str(member.id)][1]}")
            else:
                await ctx.send(f"⚠ | This user is Artist role blacklisted!")

    @commands.command()
    @commands.has_any_role('Staff')
    async def notartist(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name='Artist')
        try:
            await member.remove_roles(role,
                                      reason=f"[Artist command executed "
                                      f"by:{ctx.author.name}#"
                                      f"{ctx.author.discriminator}]"
                                      )
            await ctx.send(f"✅ | {member.mention} is no longer an artist!")
        except Exception as e:
            if ctx.author.id == 286246724270555136:
                await ctx.send(f"❌ | Ignoring exception in command "
                               f"{ctx.command}:\n```py\n{e}\n```")
            else:
                await ctx.send("❌ | An error has occured.")

    @commands.group(name='artblacklist')
    @commands.has_any_role("Staff")
    async def _artblacklist(self, ctx, number=10):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(color=ctx.author.color)
            i = 0
            for b in DataManager.read('data/artblacklist.json'):
                greater = False
                i += 1
                if number:
                    if number > 10:
                        if i > 10:
                            greater = True
                        else:
                            greater = True
                    else:
                        if i > number:
                            break
                else:
                    if i > 10:
                        greater = True

                reason = DataManager.read('data/artblacklist.json')[str(b)][1]
                pos = DataManager.read('data/artblacklist.json')[str(b)][0]

                member = discord.utils.get(ctx.bot.get_all_members(),
                                           id=int(b))
                embed.set_author(name="Art channel blacklists:\n")
                clean_name = emoji.get_emoji_regexp().sub(r'\\\1', member.name)

                embed.add_field(
                             name=f"#{pos} {clean_name}#{member.discriminator}"
                             f" (ID:{member.id})",
                             value=reason,
                             inline=False
                             )

            try:
                if len(DataManager.read('data/artblacklist.json')) == 0:
                    await ctx.send("❌ | Nobody is blacklisted!")
                else:
                    await ctx.send(embed=embed)

            except discord.errors.HTTPException as e:
                await ctx.send("❌ | Nobody is blacklisted!")
                raise e

    @_artblacklist.command(aliases=['add'])
    @commands.has_any_role('Staff')
    async def addblacklist(self, ctx, member: discord.Member, *reason):
        if reason:
            reason = ' '.join(reason)
        if not str(member.id) in DataManager.read('data/artblacklist.json'):
            if reason:
                asas = [len(DataManager.read('data/artblacklist.json'))+1,
                        reason]
                DataManager.update('data/artblacklist.json', member.id, asas)
                role = discord.utils.get(ctx.guild.roles, name='Artist')
                check = discord.utils.get(member.roles, name='Artist')
                if check:
                    await member.remove_roles(role,
                                              reason=f"[Blacklisted user"
                                              f"{member.name}"
                                              f"#{member.discriminator}]"
                                              )

                await ctx.send(f"✅ | Successfully blacklisted"
                               f"{member.name}#{member.discriminator}.")
            else:
                role = discord.utils.get(ctx.guild.roles, name='Artist')
                check = discord.utils.get(member.roles, name='Artist')
                if check:
                    await member.remove_roles(role, reason=f"[Blacklisted User"
                                              f"""
                                        {member.name}#{member.discriminator}]
                                              """)
                asa = [len(DataManager.read('data/artblacklist.json'))+1,
                       None]
                DataManager.update('data/artblacklist.json', member.id, asa)
                await ctx.send(f"✅ | Successfully blacklisted `{member.name}"
                               f"#{member.discriminator}``.")
        else:
            await ctx.send("❌ | That user is already blacklisted!")

    @_artblacklist.command(aliases=['remove'])
    @commands.has_any_role("Staff")
    async def removeblacklist(self, ctx, member: discord.Member, reason=None):
        if str(member.id) in DataManager.read('data/artblacklist.json'):
            DataManager.delete('data/artblacklist', member.id)
            await ctx.send(f"✅ | Successfully removed {member.mention} from"
                           " the blacklist!")
        else:
            await ctx.send("❌ | That user is not blacklisted!")

    @commands.command()
    @Checks.is_staff()
    async def mentionable(self, ctx, *rolename):
        if not rolename:
            await ctx.send("❌ | You need to provide a rolename!")
        else:
            rolename = ' '.join(rolename)
            rolename = str(rolename)
            role = discord.utils.get(ctx.guild.roles, name=rolename)
            if role != None:
                await role.edit(mentionable=True)
                await ctx.send(f"✅ | `{rolename}` is now mentionable!")
            else:
                await ctx.send("❌ | I couldn't find that role.")

    @commands.command()
    @Checks.is_staff()
    async def notmentionable(self, ctx, *rolename):
        if not rolename:
            await ctx.send("❌ | You need to provide a rolename!")
        else:
            rolename = ' '.join(rolename)
            rolename = str(rolename)
            role = discord.utils.get(ctx.guild.roles, name=rolename)
            if role != None:
                await role.edit(mentionable=True)
                await ctx.send(f"✅ | `{rolename}` is no longer mentionable!")
            else:
                await ctx.send("❌ | I couldn't find that role.")

    @commands.command()
    @Checks.is_staff()
    async def mention(self, ctx, *role):
        role = ' '.join(role)
        role = str(role)
        role = discord.utils.get(ctx.guild.roles, name=role)
        this_is_useless_code = None
        if this_is_useless_code:
            new_message = message - "-c"

            channels = ctx.message.channel_mentions if ctx.message.channel_mentions != [] else None
            if role is not None:
                if channels is not None:
                    await role.edit(mentionable=True)
                    for channel in channels:
                        await channel.send(f"<@&{role.id}> " + new_message)
                        break
                    if len(channels) > 1:
                        await ctx.send("Only going sent it in one channel.")
                    await role.edit(mentionable=False)
                else:
                    await ctx.send("When adding the -c flag, you must mention a channel.")
            else:
                await ctx.send("I couldn't find that role.")
        else:
            if role is not None:
                await role.edit(mentionable=True)
                apples = await ctx.send(f"<@&{role.id}>" + message)
                await apples.delete()
                await ctx.message.delete()
                await role.edit(mentionable=False)
            else:
                await ctx.send("❌ | I couldn't find that role.")

    @commands.command(aliases=['addrole'])
    async def add(self, ctx, member: discord.Member, *roles):
        ca = discord.utils.get(ctx.author.roles, name='Challenge Approver')
        staffrole = discord.utils.get(ctx.author.roles, name='Staff')
        permos = ctx.author.guild_permissions.value & 268435456 == 268435456
        if (staffrole is not None or ca is not None) or not permos:
            if not roles:
                await ctx.send("❌ | You need to provide a role!")
            else:
                roles = ' '.join(roles)
                roles = discord.utils.get(ctx.guild.roles, name=roles)
                role_count = len(ctx.author.roles) - 1
                try:
                    if roles:
                        if ctx.author.roles[role_count] > roles:
                            await member.add_roles(roles, reason=f"[Command "
                                                   "executed by "
                                                   f"{ctx.author.name}#"
                                                   f"{ctx.author.discriminator}"
                                                   )
                            await ctx.send(f"✅ | Successfully added role"
                                           f"`{roles.name}` to {member.mention}"
                                           "!")
                        else:
                            await ctx.send("❌ | That role is higher than your"
                                           " highest role!")
                    else:
                        await ctx.send("❌ | I couldn't find that role.")
                except discord.errors.Forbidden:
                    await ctx.send("❌ | I couldn't add that role because"
                                   " I am either too far below it or I do not "
                                   "have the permissions required to add it.")
                except Exception as e:
                    await ctx.send("❌ | An error in adding that role has "
                                   "occured, please contact "
                                   "<@!286246724270555136>.")
                    raise e
        else:
            await ctx.send("❌ | You lack the required permissions to execute "
                           "this command.")

    @commands.command(aliases=['removerole'])
    async def remove(self, ctx, member: discord.Member, *roles):
        ca = discord.utils.get(ctx.author.roles, name='Challenge Approver')
        staffrole = discord.utils.get(ctx.author.roles, name='Staff')
        permos = ctx.author.guild_permissions.value & 268435456 == 268435456
        if (staffrole is not None or ca is not None) or not permos:
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
                            await ctx.send(f"✅ | Successfully removed role "
                                           f"`{roles.name}` from "
                                           f"{member.mention}!")
                        else:
                            await ctx.send("❌ | That role is higher than your"
                                           " highest role!")
                    else:
                        await ctx.send("❌ | I couldn't find that role.")
                except discord.errors.Forbidden:
                    await ctx.send("❌ | I couldn't remove that role because "
                                   "I am either too far below it or I do not"
                                   " have the permissions required to remove"
                                   "it.")
                except Exception as e:
                    await ctx.send("❌ | An error in adding that role has "
                                   "occured, please contact "
                                   "<@!286246724270555136>.")
                    raise e
        else:
            await ctx.send("❌ | You lack the required permissions to execute "
                           "this command.")

    async def on_member_update(self, before, after):
        try:
            role = discord.utils.get(after.guild.roles, name='Artist')
            if role in after.roles:
                if str(after.id) in DataManager.read('data/artblacklist.json'):
                    await after.remove_roles(role,
                                             reason=f"[Blacklisted user "
                                             f"{after.name}#"
                                             f"{after.discriminator}]"
                                             )
        except Exception as e:
            raise e


def setup(bot):
    bot.add_cog(Roles())
    print("Loaded Roles.")
