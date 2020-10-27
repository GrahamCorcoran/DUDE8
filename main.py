from datetime import datetime, timedelta
import pytz
import time

from discord.ext import commands, tasks
from discord.utils import get
import embeds
import dude8db
import secrets

dude8 = commands.Bot(command_prefix="!dd ")


@dude8.event
async def on_ready():
    print('We have logged in as {0.user}'.format(dude8))
    post_reminders.start()


@dude8.command()
async def add(ctx, course, description, date):
    guild_id = ctx.message.guild.id
    response = dude8db.add_duedate(guild_id, course, description, date)
    await ctx.send(response)


@dude8.command()
async def remove(ctx, course, description):
    guild_id = ctx.message.guild.id
    response = dude8db.remove_duedate(guild_id, course, description)
    await ctx.send(response)


@dude8.command()
async def setup(ctx):
    await ctx.send(embed=embeds.setup)


@dude8.command()
async def set_timezone(ctx, new_timezone):
    guild_id = ctx.message.guild.id
    response = dude8db.change_timezone(guild_id, new_timezone)
    await ctx.send(response)


@dude8.command()
async def set_notification_time(ctx, new_notification_hour):
    guild_id = ctx.message.guild.id
    response = dude8db.change_notification(guild_id, new_notification_hour)
    await ctx.send(response)


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


@dude8.command()
async def set_weekly_notification(ctx, new_notification_day):
    guild_id=ctx.message.guild.id
    response = dude8db.change_weekly_notification(guild_id, new_notification_day)
    await ctx.send(response)


@tasks.loop(seconds=10)
async def post_reminders():
    valid_servers = dude8db.valid_servers()
    for server in valid_servers:
        now = datetime.now(tz=pytz.timezone(server['timezone']))
        notify = now.hour == server['notification_time']

        if notify:
            channel = dude8.get_channel(int(server['text_channel']))
            weekly = int(now.isoweekday()) == server['weekly_notification']

            if weekly:
                # Post the weekly
                pass
            daily = embeds.upcoming.copy()
            today = add_day_as_row(now, server, now.date())
            tomorrow = add_day_as_row(now, server, now.date() + timedelta(days=1))

            if today:
                daily.add_field(name=today[0], value=today[1], inline=False)
            if tomorrow:
                daily.add_field(name=tomorrow[0], value=tomorrow[1], inline=False)

            if today or tomorrow:
                await channel.send(embed=daily)

            print(server['serverID'], "Notification time!")


def add_day_as_row(now, server, target_date):
    day_return = []
    for course in server['course']:
        for due_date in course['duedates']:
            if datetime.date(due_date['due_date']) == target_date:
                day_return.append(f"{course['course_name']} - {due_date['description']}")

    if day_return:
        current_date = now.date()
        if current_date == target_date:
            title = "Today"
        elif current_date + timedelta(days=1) == target_date:
            title = "Tomorrow"
        else:
            title = target_date.strftime("%A")
        return_text = ""
        for due_date in day_return:
            return_text += due_date + "\n"

        return [title, return_text]
    return False


@dude8.event
async def on_guild_join(guild):
    dude8db.add_server(guild.id)

dude8.run(secrets.token)
