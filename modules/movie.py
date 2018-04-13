import discord
from discord.ext import commands
from __main__ import DataManager, Checks


class Movie:

    @Checks.is_staff()
    @commands.commands()
    async def movielist(self, ctx):
        movies = DataManager.read('data/movie.json')[str('movies')]
        embed = discord.Embed(title='__Movie suggestions__:',
                              description=movies,
                              color=ctx.author.color)
        # DataManager.delete('data/movie.json', 'movies')
        await ctx.send(embed=embed)

    async def on_message(message):
        if message.channel.id == "426487069351608330":
            DataManager.list_update('data/movie.json', 'movies', message.content)


def setup(bot):
    bot.add_cog(Movie())
    print("Loaded Movie.")
