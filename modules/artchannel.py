import discord
from discord.ext import commands
from __main__ import test
if test:
    channel = 'art'
else:
    channel = 'custombot-testing'

class ArtChannel:
    """The art channel on_message."""

    def __init__(self, bot):
        sbk = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def setartchannel(self, ctx, logch:int):
        global channel

        channel = logch
        await ctx.send(f"✅ | Set the Art channel to <#{id}>!")

    async def on_message(self, message):

        if message.channel.id == 421494597013733406:
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
    bot.logger.info("Loaded ArtChannel.")
