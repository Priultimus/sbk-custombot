import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
keyfile = 'data/h0r1zonz-b3fc89528e7d.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scope)

gc = gspread.authorize(credentials)
sheet = gc.open_by_key('1iEsS6hcOQejOFK7DgduHfpvZN7tVfbkdQbq_yR0Xwro')
worksheet = sheet.get_worksheet(0)
val = worksheet.acell('B2').value


class Challenges:
    """Challenge Approver Module"""

    @commands.command()
    async def test(self, ctx):
        global val
        await ctx.send(val)

    @commands.command()
    async def ttest(self, ctx, user: discord.Member, pts):
        errored = True
        try:
            cell = worksheet.find(str(user.id))
            errored = False
        except gspread.exceptions.CellNotFound:
            await ctx.send("❌ | I couldn't find that user...")
            pass
        if errored:
            pass
        else:
            await ctx.send(cell.value)
            values_list = worksheet.row_values(cell.row)
            if pts.startswith('+'):
                pts = pts.strip("+")
                pts = int(values_list[3]) + int(pts)
                await ctx.send(pts)
            elif pts.startswith('-'):
                pts = pts.strip('-')
                pts = int(values_list[3]) - int(pts)
                await ctx.send(pts)
            else:
                pts = int(pts)
                await ctx.send(pts)
            await ctx.send(values_list)
            newcell = worksheet.find(values_list[3])
            worksheet.update_cell(newcell.row, newcell.col, pts)
            values_list = worksheet.row_values(newcell.row)
            await ctx.send(values_list)

    @commands.command()
    async def value(self, ctx, num: int):
        values_list = worksheet.row_values(num)
        await ctx.send(values_list)


def setup(bot):
    bot.add_cog(Challenges())
    print("Loaded Challenges.")
