import discord
from discord.ext import commands

class Filters:
    async def on_message(self, message):
        list = ["ANT", "ANTONIO", "ANTONIO32A", "ANTO", "ANTIE", "ANTON", "166630166825664512"]
        contents = message.content.split(" ")
        bypass = ["166630166825664512"]
        member = discord.utils.get(message.guild.members, id=166630166825664512)
        for word in contents:
            if word.upper() in list:
                if not message.author.id in bypass:
                    try:
                        member.send(embed=discord.Embed(color=message.author.color, title=str(message.author) + str("({})".format(message.author.id), description=str(message.content), footer=str(message.id)))

def setup(bot):
    bot.add_cog(Filters(bot))
    print("Loaded Filters.")
