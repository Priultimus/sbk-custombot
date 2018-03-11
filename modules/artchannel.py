import discord
from discord.ext import commands 

channel = 'art'

class ArtChannel:
    """The art channel on_message."""

    def __init__(self, bot):
        sbk = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def setartchannel(self, ctx, logch:str):
        global channel

        def cfind(channel):
            for c in ctx.guild.channels:
                if c.name == channel:
                    return c

        r = cfind(logch)
        if r:
            log = logch
            await ctx.send(f"✅ | Set the Art channel to <#{r.id}>!")
        else:
            await ctx.send("❌ | Couldn't find that channel.")

        
    async def on_message(self, message):

        if message.channel.id == 281738644958609408:
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
    n = ArtChannel(bot)
    bot.add_cog(n)
    print("Loaded ArtChannel.")
