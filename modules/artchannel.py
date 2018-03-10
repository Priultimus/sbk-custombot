import discord
from discord.ext import commands 

channel = 421800783072460810

class ArtChannel:
    """The art channel on_message."""

    def __init__(self, bot):
        sbk = bot

    @commands.command(name='artchannel')
    @commands.has_permissions(ban_members=True)
    async def setartchannel(self, ctx, rolename:str):
        def find(rolename):
            for role in ctx.guild.channels:
                if role.name == rolename:
                    return role

        global channel
        if not find(rolename) == None:
            channel = rolename
            await ctx.send(f"✅ | Set the Art Channel to `{rolename}`!")
        else:
            await ctx.send(f"❌ | Couldn't find that channel on this server.")
        
    async def on_message(self, message):
        global channel 
        if message.channel.id == channel:
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
