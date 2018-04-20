import discord
from discord.ext import commands
from __main__ import Checks, DataManager, Formatter


class Voting:

    @commands.group(name="votereact", invoke_without_command=True)
    @Checks.is_staff()
    async def votereact(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("<:error:436279057416585217>")

    @votereact.command()
    @Checks.is_staff()
    async def on(self, ctx, channel: discord.TextChannel=None, *args):
        if channel is None:
            channel = ctx.channel
        ch = str(channel.id)
        args = ' '.join(args)
        try:
            a = DataManager.read('data/votereact.json')['channels']
        except KeyError:
            DataManager.write('data/votereact.json', 'channels', [])
            DataManager.list_update('data/votereact.json', 'channels', channel.id)
            await ctx.send("✅ | Enabled vote reacting here!")

        if '--arrows' or '-a' in args:
            DataManager.list_update('data/votereact.json', ch, 'arrows')
            if channel.id not in a:
                DataManager.list_update('data/votereact.json', 'channels', channel.id)
                await ctx.send("✅ | Enabled vote reacting here!")
            else:
                await Formatter.error(ctx, "Vote reacting is already enabled here!")
        elif '-nd' or '--no-downvote' in args:
            if channel.id not in a:
                DataManager.list_update('data/votereact.json', 'channels', channel.id)
                await ctx.send("✅ | Enabled vote reacting here!")
            else:
                await Formatter.error(ctx, "Vote reacting is already enabled here!")
            DataManager.list_update('data/votereact.json', ch, 'nd')
        elif '-np' or '--no-upvote' in args:
            if channel.id not in a:
                DataManager.list_update('data/votereact.json', 'channels', channel.id)
                await ctx.send("✅ | Enabled vote reacting here!")
            else:
                await Formatter.error(ctx, "Vote reacting is already enabled here!")
            DataManager.list_update('data/votereact.json', ch, 'np')
        else:
            DataManager.list_update('data/votereact.json', ch, None)
            if channel.id not in a:
                print("/")
                DataManager.list_update('data/votereact.json', 'channels', channel.id)
                await ctx.send("✅ | Enabled vote reacting here!")
            else:
                await Formatter.error(ctx, "Vote reacting is already enabled here!")


    @votereact.command()
    @Checks.is_staff()
    async def off(self, ctx, channel: discord.TextChannel=None):
        if channel is None:
            channel = ctx.channel
        ch = str(channel.id)
        try:
            a = DataManager.read('data/votereact.json')['channels']
        except KeyError:
            DataManager.write('data/votereact.json', 'channels', [])
            await Formatter.error(ctx, 'Votereact was never enabled!')
        if channel.id in a:
            DataManager.list_remove('data/votereact.json', 'channels', channel.id)
            try:
                DataManager.list_update('data/votereact.json', ch, [])
            except KeyError:
                pass
            await ctx.send("✅ | Disabled vote reacting!")
        else:
            await Formatter.error(ctx, "Votereact wasn't ever enabled.")

    @votereact.command()
    @Checks.is_staff()
    async def list(self, ctx):
        channels = DataManager.read('data/votereact.json')['channels']
        embed = discord.Embed(color=ctx.author.color, title="Channels")
        for channel in channels:
            ch = discord.utils.get(ctx.guild.channels, id=channel)
            embed.add_field(name=ch.name, value=ch.mention, inline=False)
        if channels == []:
            await Formatter.error(ctx, "No votereact channels!")
        else:
            await ctx.send(embed=embed)

    async def on_message(self, message):
        a = DataManager.read('data/votereact.json')['channels']
        try:
            b = DataManager.read('data/votereact.json')[str(message.channel.id)]
        except KeyError:
            b = []
        if message.author.bot:
            return
        if message.channel.id in a:
            if not message.attachments == []:
                if 'arrows' in b:
                    if 'np' in b:
                        await message.add_reaction("\U0001f53d")
                    elif 'nd' in b:
                        await message.add_reaction("\U0001f53c")
                    else:
                        await message.add_reaction("\U0001f53d")
                        await message.add_reaction("\U0001f53c")
                else:
                    if 'np' in b:
                        await message.add_reaction("\U0001f44e")
                    elif 'nd' in b:
                        await message.add_reaction('\U0001f44d')
                    else:
                        await message.add_reaction('\U0001f44d')
                        await message.add_reaction('\U0001f44e')
            elif not message.embeds == []:
                if 'arrows' in b:
                    if 'np' in b:
                        await message.add_reaction("\U0001f53d")
                    elif 'nd' in b:
                        await message.add_reaction("\U0001f53c")
                    else:
                        await message.add_reaction("\U0001f53d")
                        await message.add_reaction("\U0001f53c")

                else:
                    if 'np' in b:
                        await message.add_reaction("\U0001f44e")
                    elif 'nd' in b:
                        await message.add_reaction('\U0001f44d')
                    else:
                        await message.add_reaction('\U0001f44d')
                        await message.add_reaction('\U0001f44e')
            else:
                pass
        else:
            pass


def setup(bot):
    bot.add_cog(Voting())
    print("Loaded VoteReact.")
