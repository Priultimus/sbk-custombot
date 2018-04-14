import discord
from discord.ext import commands
from __main__ import DataManager, Checks


class Movie:

    @Checks.is_staff()
    @commands.command()
    async def movielist(self, ctx):
        a = DataManager.read('data/movie.json')[str('movies')]
        embed = discord.Embed(color=ctx.author.color)
        for a in a:
            embed.add_field(name=str('\u200B'), value=str(a))
        await ctx.send(embed=embed)


    async def on_message(self, message):
        if message.channel.id == 426487069351608330:
            DataManager.list_update('data/movie.json', 'movies', message.content)


def setup(bot):
    bot.add_cog(Movie())
    print("Loaded Movie.")
