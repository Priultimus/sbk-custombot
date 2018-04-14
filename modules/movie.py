import discord
from discord.ext import commands
from __main__ import DataManager, Checks



class Movie:

    @Checks.is_staff()
    @commands.command()
    async def movielist(self, ctx):
        for author, suggestion in DataManager.read('data/movie.json').items():
            author = discord.utils.get(ctx.guild.members, id=int(author))
            embed = discord.Embed(color=ctx.author.color)
            embed.add_field(name=str(author.name), value=str(suggestion), inline=False)
        await ctx.send(embed=embed)


    async def on_message(self, message):
        if message.channel.id == 426487069351608330:
            DataManager.list_update('data/movie.json', 'author', str(message.author.name))
            DataManager.list_update('data/movie.json', 'suggestion', str(message.content))

def setup(bot):
    bot.add_cog(Movie())
print("Loaded Movie.")
