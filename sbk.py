import discord

client = discord.Client()

@client.event
async def on_message(message):
    if message.channel.id == 421800783072460810:
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

@client.event
async def on_ready():
    print("Ready!")

client.run('NDIxNzk5MTA1ODU0MTc3Mjkw.DYSgdA.6yePajnmegaatmvhB9_9jn8-vmI')