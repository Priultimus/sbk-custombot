import discord
from discord.ext import commands
from __main__ import DataManager, Checks


class Movie:

    @Checks.is_staff()
    @commands.command()
    async def movielist(self, ctx):
        embed = discord.Embed(color=ctx.author.color)
        for author, suggestion in DataManager.read('data/movies.json').items():
            embed.add_field(name=author, value=suggestion, inline=False)
        await ctx.send(embed=embed)

    @Checks.is_staff()
    @commands.command()
    async def moviechannel(self, ctx, channel: discord.TextChannel):
        DataManager.write('data/movies.json', 'channel', channel.id)
        await ctx.send(f"✅ | Set the Movies channel to `{channel}`!")

    async def on_message(self, message):
        channel = DataManager.read('data/movies.json')[str('channel')]
        if message.channel.id == channel:
            try:
                DataManager.list_update('data/movies.json', message.author.id, message.content)
            except KeyError:
                DataManager.write('data/movies.json', message.author.id, [])
                DataManager.list_update('data/movies.json', message.author.id, message.content)

def setup(bot):
    bot.add_cog(Movie())
    print("Loaded Movie.")
