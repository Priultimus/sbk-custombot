from discord.ext import commands

class Levels:
    """Leveling system."""
    
    
    @commands.command()
    async def _placeholder(self, ctx):
        await ctx.send("Working!")
        
def setup(bot):
    print("Loaded levels.")
    bot.add_cog(Levels())
