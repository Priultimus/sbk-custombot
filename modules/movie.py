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

    async def on_message(self, message):
        if message.channel.id == 426487069351608330:
            DataManager.list_update('data/movies.json', 'author', str(message.author.name))
            DataManager.list_update('data/movies.json', 'suggestion', str(message.content))

def setup(bot):
    bot.add_cog(Movie())
    print("Loaded Movie.")
