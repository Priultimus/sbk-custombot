import discord
import datetime
from __main__ import DataManager, Formatter
from discord.ext import commands


def notify(message):
    embed = discord.Embed(color=message.author.color, description=str(message.content))
    embed.set_footer(text="Message ID: {0} | {1}".format(message.id, datetime.datetime.now()))
    embed.set_author(icon_url=message.author.avatar_url, name="{0} ({1})".format(message.author, message.author.id))
    return embed


class Triggers:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def block(self, ctx, member: discord.Member):
        DataManager.list_update('data/ignorelist.json', 'ignore', member.id)
        await Formatter.success(ctx, f'Successfully blocked {member.name}')

    @commands.command()
    async def unblock(self, ctx, member: discord.Member):
        DataManager.list_remove('data/ignorelist.json', 'ignore', member.id)
        await Formatter.success(ctx, f'Successfully unblocked {member.name}')

    @commands.command(aliases=['t'])
    async def trigger(self, ctx, *words):
        words = '|'.join(words)
        try:
            abc = DataManager.read('data/trigger.json')[str(ctx.author.id)]
            if abc == "":
                DataManager.write('data/trigger.json', str(ctx.author.id), words)
            else:
                words = words + '|'
                DataManager.write('data/trigger.json', str(ctx.author.id), words)
                words += abc
                DataManager.write('data/trigger.json', str(ctx.author.id), words)
        except KeyError:
            DataManager.write('data/trigger.json', str(ctx.author.id), words)

        await Formatter.success(ctx, "You've added a trigger for yourself!")

    @commands.command(aliases=['rt'])
    async def remove_trigger(self, ctx, *words):
        words = '|'.join(words)
        words = words + '|'
        print(words)
        try:
            abc = DataManager.read('data/trigger.json')[str(ctx.author.id)]
            words = abc.replace(words, "")
            print(words)
            print(abc)
            DataManager.write('data/trigger.json', str(ctx.author.id), words)
            await Formatter.success(ctx, "You've removed a trigger from yourself!")
        except KeyError:
            await Formatter.error(ctx, 'You need to have a trigger to use this!')
            return

    async def on_message(self, message):
        keywords = DataManager.read('data/trigger.json')
        ignore = DataManager.read('data/ignorelist.json')['ignore']
        if message.author.id in ignore:
            return
        for id in keywords:
            target = discord.utils.get(self.bot.get_all_members(), id=int(id)) if message.guild else None
            if keywords[id] == "":
                return
            msg = keywords[id].split('|')
            if (message.guild is not None) and ((any(var in message.content.lower() for var in msg)) or (target in message.mentions)):
                if target is None:
                    pass
                else:
                    if message.author.bot:
                        return
                    if message.author == target:
                        return
                    await target.send(f"You were mentioned in {message.channel.mention}:\n", embed=notify(message))

    async def on_message_edit(self, before, after):
        message = after
        ignore = DataManager.read('data/ignorelist.json')['ignore']
        if message.author.id in ignore:
            return
        keywords = DataManager.read('data/trigger.json')
        for id in keywords:
            target = discord.utils.get(self.bot.get_all_members(), id=int(id)) if message.guild else None
            if keywords[id] == "":
                return
            msg = keywords[id].split('|')
            if (message.guild is not None) and ((any(var in message.content.lower() for var in msg)) or (target in message.mentions)):
                if target is None:
                    pass
                else:
                    if message.author.bot:
                        return
                    if message.author == target:
                        return
                    await target.send(f"You were mentioned in {message.channel.mention}:\n", embed=notify(message))


def setup(bot):
    bot.add_cog(Triggers(bot))
    print("Loaded Triggers.")
