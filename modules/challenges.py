import discord
from discord.ext import commands
import gspread
from __main__ import Checks
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
keyfile = 'data/h0r1zonz-b3fc89528e7d.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scope)




val = worksheet.acell('B2').value


class Challenges:
    """Challenge Approver Module"""

    @Checks.is_ca()
    @commands.command()
    async def addpoints(self, ctx, user: discord.Member, pts):
        errored = True
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key('1UHXrqeaapyCXv-xJV7YmA9r5c_6tjjS9t_55YJhIFVc')
        worksheet = sheet.get_worksheet(0)
        try:
            cell = worksheet.find(str(user.id))
            errored = False
        except gspread.exceptions.CellNotFound:
            await ctx.send("❌ | I couldn't find that user...")

        if errored:
            pass
        else:
            values_list = worksheet.row_values(cell.row)
            newpts = int(values_list[3]) + int(pts)
            col = int(cell.col) + 2
            worksheet.update_cell(cell.row, col, newpts)
            values_list = worksheet.row_values(cell.row)
            await ctx.send(f"✅ | Successfully added {pts} points to {user.mention}")

    @Checks.is_ca()
    @commands.command()
    async def removepoints(self, ctx, user: discord.Member, pts):
        errored = True
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key('1UHXrqeaapyCXv-xJV7YmA9r5c_6tjjS9t_55YJhIFVc')
        worksheet = sheet.get_worksheet(0)
        try:
            cell = worksheet.find(str(user.id))
            errored = False
        except gspread.exceptions.CellNotFound:
            await ctx.send("❌ | I couldn't find that user...")
            
        if errored:
            pass
        else:
            values_list = worksheet.row_values(cell.row)
            if int(pts) > int(values_list[3]):
                await ctx.send(f"❌ | {user.mention} doesn't have that many points!")
            else:
                newpts = int(values_list[3]) - int(pts)
                col = int(cell.col) + 2
                worksheet.update_cell(cell.row, col, newpts)
                values_list = worksheet.row_values(cell.row)
                await ctx.send(f"✅ | Successfully removed {pts} points from {user.mention}!")

    @commands.command()
    async def points(self, ctx, member: discord.Member=None):
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key('1UHXrqeaapyCXv-xJV7YmA9r5c_6tjjS9t_55YJhIFVc')
        worksheet = sheet.get_worksheet(0)
        if member is None:
            member = ctx.author
        a = True
        try:
            cell = worksheet.find(str(member.id))
            a = False
        except gspread.exceptions.CellNotFound:
            await ctx.send("❌ | I couldn't find that user...")
            
        if not a:
            values_list = worksheet.row_values(cell.row)
            col_values = worksheet.col_values(cell.col)
            pts = values_list[3]
            embed = discord.Embed(color=member.color,
                                  title=f"{member.name}"
                                  f"#{member.discriminator}")
            embed.add_field(name=f'Ranked {values_list[0]}', value=f'{values_list[5]}', inline=False)
            val = worksheet.acell('A2').row
            first = worksheet.row_values(val)
            if int(values_list[0]) == 1:
                valuemsg = f"Already the most points!"
            elif int(values_list[0]) == 2:
                you = int(values_list[3])
                firsts = int(first[3])
                catch = firsts - you + 1
                valuemsg = f"{catch} points to go to catch up to {first[2]}(1)"
            else:
                ff = col_values[int(values_list[0])-1]
                up = worksheet.find(str(ff))
                variable = worksheet.row_values(up.row)
                firsts = int(first[3])
                you = int(values_list[3])
                catch3 = int(variable[3]) - you + 1
                catch = firsts - you + 1
                val = f"{catch} points to catch up with {first[2]}(1)"
                msg = f"{catch3} points to catch up with {variable[2]}({int(values_list[0])-1})"
                valuemsg = val + '\n' + msg
            embed.add_field(
                            name=f"{pts} Points",
                            value=valuemsg,
                            inline=False
                            )
            embed.add_field(name=f"Points to next rank:", value=f"{values_list[4]}")
            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Challenges())
    print("Loaded Challenges.")
