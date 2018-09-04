import discord
from discord.ext import commands
from __main__ import Checks, DataManager, key
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
keyfile = 'data/h0r1zonz-b3fc89528e7d.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scope)


class Challenges:
    """Challenge Approver Module"""

    @Checks.is_ca()
    @commands.command()
    async def create(self, ctx, user: discord.Member):
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key(key)
        worksheet = sheet.get_worksheet(0)
        r = len(worksheet.col_values(1))
        rr = r+1
        can = True
        try:
            worksheet.find(str(user.id))
            can = False
        except gspread.exceptions.CellNotFound:
            can = True
        code = f"""=if(F{rr}="Supreme","Maxed Rank",if(F{rr}="Master",5000-D{rr},if(F{rr}="Champion",4000-D{rr},if(F{rr}="Superior",3000-D{rr},if(F{rr}="Elite",2000-D{rr},if(F{rr}="Expert",1400-D{rr},if(F{rr}="Remarkable",1100-D{rr},if(F{rr}="Advanced",850-D{rr},if(F{rr}="Specialist",600-D{rr},if(F{rr}="Professional",450-D{rr},if(F{rr}="Veteran",330-D{rr},if(F{rr}="Proficient",200-D{rr},if(F{rr}="Experienced",100-D{rr},if(F{rr}="Skilled",70-D{rr},if(F{rr}="Adept",50-D{rr},if(F{rr}="Beginner",30-D{rr},if(F{rr}="Mediocre",20-D{rr},if(F{rr}="Inept",10-D{rr},if(F{rr}="No Rank",5-D{rr},"u wot m8 ?!?! FITE ME")))))))))))))))))))"""
        code2 = f"""=IF(D{rr}>=5000,"Supreme",IF(D{rr}>=4000,"Master",IF(D{rr}>=3000,"Champion",IF(D{rr}>=2000,"Superior",IF(D{rr}>=1400,"Elite",IF(D{rr}>=1100,"Expert",IF(D{rr}>=850,"Remarkable",IF(D{rr}>=600,"Advanced",IF(D{rr}>=450,"Specialist",IF(D{rr}>=330,"Professional",IF(D{rr}>=200,"Veteran",IF(D{rr}>=100,"Proficient",IF(D{rr}>=70,"Experienced",IF(D{rr}>=50,"Skilled",IF(D{rr}>=30,"Adept",IF(D{rr}>=20,"Beginner",IF(D{rr}>=10,"Mediocre",IF(D{rr}>=5,"Inept","No Rank"))))))))))))))))))
        """
        if can:
            worksheet.update_acell(f"A{rr}", f"=rank(D{rr},$D$2:$D$594,0)")
            worksheet.update_acell(f"B{rr}", str(user.id))
            worksheet.update_acell(f"C{rr}", str(user.name))
            worksheet.update_acell(f"D{rr}", str(0))
            worksheet.update_acell(f"E{rr}", code)
            worksheet.update_acell(f"""F{rr}""", code2)
            await ctx.send("✅ | Successfully created a new user! "
                           f"You can now add points to them with >addpoints {user.mention} `pts`!")
        else:
            await ctx.send("❌ | That user already exists!")

    @Checks.is_ca()
    @commands.command()
    async def addpoints(self, ctx, user: discord.Member, pts):
        errored = True
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key(key)
        worksheet = sheet.get_worksheet(0)
        try:
            cell = worksheet.find(str(user.id))
            errored = False
        except gspread.exceptions.CellNotFound:
            await ctx.send("❌ | I couldn't find that user...")

        if errored:
            pass
        else:
            a = DataManager.read('data/challenges.json')
            values_list = worksheet.row_values(cell.row)
            newpts = int(values_list[3]) + int(pts)
            col = int(cell.col) + 2
            worksheet.update_cell(cell.row, col, newpts)
            values_list = worksheet.row_values(cell.row)
            for r, v in a.items():
                if newpts >= v:
                    rr = discord.utils.get(user.roles, name=r)
                    if rr is None:
                        role = discord.utils.get(ctx.guild.roles, name=r)
                        rolelog = discord.utils.get(ctx.guild.channels,
                                                    name='challenge-role-logs')
                        await user.add_roles(role)
                        await rolelog.send(f"{user.mention} + **{r}** ({newpts} points!)")
            await ctx.send(f"✅ | Successfully added {pts} "
                           f"points to {user.mention}")
            chan = discord.utils.get(ctx.guild.channels,
                                     name='challenge-tracker')
            if not pts == 0:
                await chan.send(f"{ctx.author.mention} added **{pts}** points "
                                f"to {user.mention}!")

    @Checks.is_ca()
    @commands.command()
    async def removepoints(self, ctx, user: discord.Member, pts):
        errored = True
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key(key)
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
                await ctx.send(f"❌ | {user.mention} "
                               "doesn't have that many points!")
            else:
                newpts = int(values_list[3]) - int(pts)
                col = int(cell.col) + 2
                worksheet.update_cell(cell.row, col, newpts)
                values_list = worksheet.row_values(cell.row)
                await ctx.send(
                          f"✅ | Successfully removed "
                          f"{pts} points from {user.mention}!"
                          )
                chan = discord.utils.get(ctx.guild.channels,
                                         name='challenge-tracker')
                await chan.send(f"{ctx.author.mention} removed **{pts}** point"
                                f"s from {user.mention}!")

    @commands.command()
    async def points(self, ctx, member: discord.Member=None):
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key(key)
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
            embed.add_field(name=f'Ranked {values_list[0]}',
                            value=f'{values_list[5]}', inline=False)
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
                msg = f"{catch3} points to catch up with " \
                      f"{variable[2]}({int(values_list[0])-1})"
                valuemsg = val + '\n' + msg
            embed.add_field(
                            name=f"{pts} Points",
                            value=valuemsg,
                            inline=False
                            )
            embed.add_field(name=f"Points to next rank:",
                            value=f"{values_list[4]}")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Challenges())
    print("Loaded Challenges.")
