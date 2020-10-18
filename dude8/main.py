import discord
from dude8 import dude8db, secrets

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!dd'):
        await message.channel.send('Hello!')

@client.event
async def on_guild_join(guild):
    dude8db.add_server(guild.id)

client.run(secrets.token)
