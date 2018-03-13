import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('h0r1zonz-b3fc89528e7d.json', scope)

gc = gspread.authorize(credentials)
sheet=gc.open_by_key('1iEsS6hcOQejOFK7DgduHfpvZN7tVfbkdQbq_yR0Xwro')
worksheet = sheet.get_worksheet(0)
val = worksheet.acell('B1').value

class Challenges:
    """SBK's challenges"""
    def __init__(self, bot):
        sbk = bot

    @commands.command()
    async def test(self, ctx):
        global val
        await ctx.send(val)

def setup(bot):
    bot.add_cog(Challenges(bot))
    print("Loaded Challenges.")
