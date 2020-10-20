from discord.ext import commands
from discord.utils import get
import embeds
import dude8db
import secrets

dude8 = commands.Bot(command_prefix="!dd ")


@dude8.event
async def on_ready():
    print('We have logged in as {0.user}'.format(dude8))


@dude8.command()
async def add(ctx, description, date):
    guild_id = ctx.message.guild.id
    response = dude8db.add_duedate(guild_id, description, date)
    await ctx.send(response)


@dude8.command(rest_is_raw=True)
async def bulkadd(ctx, *, csv):
    guild_id = ctx.message.guild.id
    response = dude8db.bulk_add(guild_id, csv)
    await ctx.send(response)


@dude8.command()
async def remove(ctx, description):
    guild_id = ctx.message.guild.id
    response = dude8db.remove_duedate(guild_id, description)
    await ctx.send(response)


@dude8.command()
async def timezone(ctx, new_timezone):
    guild_id = ctx.message.guild.id
    response = dude8db.change_timezone(guild_id, new_timezone)
    await ctx.send(response)


@dude8.command()
async def setup(ctx):
    await ctx.send(embed=embeds.setup)


@dude8.command()
async def set_channel(ctx, channel_name):
    channel = get(ctx.guild.channels, name=channel_name)
    if channel:
        server = dude8db.Server
        (server.update({server.text_channel: channel.id})
               .where(server.serverID == ctx.guild.id)).execute()
        await ctx.send(f"Updated notification channel to {channel_name}.")
    else:
        await ctx.send(f"No channel found named {channel_name}.")


@dude8.event
async def on_guild_join(guild):
    dude8db.add_server(guild.id)

dude8.run(secrets.token)
