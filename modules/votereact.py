import discord
from discord.ext import commands
from __main__ import Checks, DataManager


class Voting:

    @commands.group(name="votereact")
    @Checks.is_staff()
    async def votereact(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @votereact.command(invoke_without_command=True)
    @Checks.is_staff()
    async def on(self, ctx):
        channel = ctx.channel
        try:
            a = DataManager.read('data/votereact.json')['channels']
        except KeyError:
            DataManager.write('data/votereact.json', 'channels', [])
            DataManager.list_update('data/votereact.json', 'channels', channel.id)
            await ctx.send("✅ | Enabled vote reacting here!")
        if channel.id not in a:
            DataManager.list_update('data/votereact.json', 'channels', channel.id)
            await ctx.send("✅ | Enabled vote reacting here!")

    @votereact.command(invoke_without_command=True)
    @Checks.is_staff()
    async def off(self, ctx):
        channel = ctx.channel
        try:
            a = DataManager.read('data/votereact.json')['channels']
        except KeyError:
            DataManager.write('data/votereact.json', 'channels', [])
            DataManager.list_remove('data/votereact.json', 'channels', channel.id)
            await ctx.send("✅ | Disabled vote reacting here!")
        if channel.id not in a:
            DataManager.list_remove('data/votereact.json', 'channels', channel.id)
            await ctx.send("✅ | Disabled vote reacting here!")

    @votereact.command()
    @Checks.is_staff()
    async def list(self, ctx):
        channels = DataManager.read('data/votereact.json')['channels']
        embed = discord.Embed(color=ctx.author.color, title="Channels")
        for channel in channels:
            ch = discord.utils.get(ctx.guild.channels, id=channel)
            embed.add_field(name=ch.name, value=ch.mention, inline=False)
        await ctx.send(embed=embed)

    async def on_message(self, message):
        a = DataManager.read('data/votereact.json')['channels']
        if message.channel.id in a:
            if not message.attachments == []:
                await message.add_reaction('\U0001f44d')
                await message.add_reaction('\U0001f44e')
            elif not message.embeds == []:
                await message.add_reaction('\U0001f44d')
                await message.add_reaction('\U0001f44e')
            else:
                pass
        else:
            pass


def setup(bot):
    bot.add_cog(VoteReact())
    print("Loaded VoteReact.")
