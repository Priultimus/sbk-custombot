"""import discord
from discord.ext import commands
from __main__ import Checks, DataManager, test

if test == True:
    guild = discord.utils.get(self.bot.guilds, id=402197486317338625)

joining = DataManager.read('data/lockdown.json')[str('joining')]
role = discord.utils.get(guild.roles, id=DataManager.read('data/lockdown.json')[str('role')])


class Lockdown:
    def __init__(self, bot):
        self.bot = bot


    @commands.group(name="lockdown", invoke_without_command=True)
    @Checks.is_staff()
    async def lockdown(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("<:error:436279057416585217>")


    @lockdown.command()
    @Checks.is_staff()
    async def joining(self, ctx):
        if joining == "False":
            DataManager.write('data/lockdown.json', 'joining', 'True')
            await ctx.send("✅ | Joining lockdown is now **on**.")

        if joining == "True":
            member = discord.Member
            for member in guild.members:
                if role in member.roles:
                    await member.remove_roles(role)
            DataManager.write('data/lockdown.json', 'joining', 'False')
            await ctx.send("✅ | Joining lockdown is now **off**.")

        else:
            await ctx.send("<:error:436279057416585217>")


        async def on_member_join(self, member):
            if lockdown == "True":
                await member.add_roles(role)
            else:
                pass
"""
