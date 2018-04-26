import discord
import datetime

class Filters:
    async def on_message(self, message):
        list = ["ANT", "ANTONIO", "ANTONIO32A", "ANTO", "ANTIE", "ANTON", "166630166825664512"]
        contents = message.content.split(" ")
        bypass = ["166630166825664512"]
        member = discord.utils.get(message.guild.members, id=166630166825664512)
        for word in contents:
            if word.upper() in list:
                if not message.author.id in bypass:
                    embed=discord.Embed(color=message.author.color, description=str(message.content))
                    embed.set_footer(text="Message ID: {0} | {1}".format(message.id, datetime.datetime.now()))
                    embed.set_author(icon_url=message.author.avatar_url, name="{0} ({1})".format(message.author, message.author.id))
                    await member.send(embed=embed)

def setup(bot):
    bot.add_cog(Filters())
    print("Loaded Filters.")
