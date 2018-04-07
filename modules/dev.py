from discord.ext import commands
import textwrap
import traceback
import git
import asyncio
import inspect
from contextlib import redirect_stdout
import io
from __main__ import DataManager
from __main__ import Checks
# to expose to the eval command
import discord


class Developer:
    """Developer commands"""
    def __init__(self, bot):
        self._last_result = None
        self.sessions = set()

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f"""```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}:
        {e}```"""

    @commands.command()
    @Checks.is_staff()
    async def backup(self, ctx, channel: discord.TextChannel, limit=100):
        c = discord.utils.get(ctx.guild.channels, id=channel.id)
        messages = []
        async for elem in c.history(limit=limit):
            messages.append(elem)
        d = discord.utils.get(ctx.bot.guilds, id=402197486317338625)
        cba = discord.utils.get(d.channels, name='Backup-channels')
        cd = await d.create_text_channel(c.name, category=cba)
        for m in messages:
            try:
                await cd.send(m.content)
            except discord.errors.HTTPException:
                continue
        await ctx.send(f"✅ | Successfully backed up channel "
                       f"{channel.mention}!")

    @commands.command(name='eval')
    @Checks.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Evaluates code"""

        env = {
            'bot': ctx.bot,
            'sbk': ctx.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'discord': discord,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except Exception as e:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command(pass_context=True, hidden=True)
    @Checks.is_owner()
    async def repl(self, ctx):
        """Launches an interactive REPL session."""
        variables = {
            'ctx': ctx,
            'bot': ctx.bot,
            'message': ctx.message,
            'guild': ctx.guild,
            'channel': ctx.channel,
            'author': ctx.author,
            'discord': discord,
            '_': None
        }

        if ctx.channel.id in self.sessions:
            await ctx.send('Already running a REPL session in this channel.'
                           ' Exit it with `quit`.')
            return

        self.sessions.add(ctx.channel.id)
        await ctx.send('Enter code to execute or evaluate. `exit()` or `quit`'
                       ' to exit.')

        def check(m):
            return m.author.id == ctx.author.id and \
                   m.channel.id == ctx.channel.id and \
                   m.content.startswith('`')

        while True:
            try:
                response = await ctx.bot.wait_for('message', check=check,
                                                  timeout=10.0 * 60.0)

            except asyncio.TimeoutError:
                await ctx.send('Exiting REPL session.')
                self.sessions.remove(ctx.channel.id)
                break

            cleaned = self.cleanup_code(response.content)

            if cleaned in ('quit', 'exit', 'exit()'):
                await ctx.send('Exiting.')
                self.sessions.remove(ctx.channel.id)
                return

            executor = exec
            if cleaned.count('\n') == 0:
                # single statement, potentially 'eval'
                try:
                    code = compile(cleaned, '<repl session>', 'eval')
                except SyntaxError:
                    pass
                else:
                    executor = eval

            if executor is exec:
                try:
                    code = compile(cleaned, '<repl session>', 'exec')
                except SyntaxError as e:
                    await ctx.send(self.get_syntax_error(e))
                    continue

            variables['message'] = response

            fmt = None
            stdout = io.StringIO()

            try:
                with redirect_stdout(stdout):
                    result = executor(code, variables)
                    if inspect.isawaitable(result):
                        result = await result
            except Exception as e:
                value = stdout.getvalue()
                fmt = f'```py\n{value}{traceback.format_exc()}\n```'
            else:
                value = stdout.getvalue()
                if result is not None:
                    fmt = f'```py\n{value}{result}\n```'
                    variables['_'] = result
                elif value:
                    fmt = f'```py\n{value}\n```'

            try:
                if fmt is not None:
                    if len(fmt) > 2000:
                        await ctx.send('Content too big to be printed.')
                    else:
                        await ctx.send(fmt)
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await ctx.send(f'Unexpected error: `{e}`')

    @commands.command()
    @Checks.is_owner()
    async def git(self, ctx, *pull):
        """Pull from github."""
        g = git.cmd.Git("./")
        e = discord.Embed(color=ctx.author.color)
        e.set_author(name="Git Pull", icon_url=ctx.bot.user.avatar_url)
        e.add_field(name="Status:", value=g.pull())
        await ctx.send(embed=e)
        ctx.bot.restart()

    @commands.command()
    @Checks.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down...")
        await ctx.bot.logout()

    @commands.command()
    @Checks.is_owner()
    async def restart(self, ctx):
        await ctx.send("Restarting...")
        ctx.bot.restart()

    @commands.command()
    @commands.is_owner()
    async def owner(self, ctx, member: discord.Member):
        DataManager.list_update('data/bot.json', 'OWNERS', member.id)
        await ctx.send("Updated owner!")


def setup(bot):
    bot.add_cog(Developer(bot))
    print("Loaded Dev.")
