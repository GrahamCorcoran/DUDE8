from discord.ext import commands
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



@dude8.event
async def on_guild_join(guild):
    dude8db.add_server(guild.id)

dude8.run(secrets.token)
