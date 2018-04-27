import discord


class Filters:
    async def on_message(self, message):
        list = ["ANT", "166630166825664512"]

        member = discord.utils.get(message.guild.members, id=166630166825664512)
        for word in message:
            if word.upper() in list:
                embed=discord.Embed(color=message.author.color, description=str(message.content))
                embed.set_footer(text="{0} | {1}".format(message.channel.name, message.id))
                embed.set_author(icon_url=message.author.avatar_url, name="{0} ({1})".format(message.author, message.author.id))
                await member.send(embed=embed)

def setup(bot):
    bot.add_cog(Filters())
    print("Loaded Filters.")
