from discord import embeds

dude8_logo = "https://raw.githubusercontent.com/GrahamCorcoran/DUDE8/dev/images/DUDE8.jpg"


setup = embeds.Embed(title="Setup",
                     description="To set up dude8, the timezone and your preferred "
                                 "notification time must be set. (Default 8am) Optionally, you can "
                                 "set up weekly notification days and default notification channels.\n",
                     color=0xe67e22)
setup.add_field(name="Timezone",
                value="!dd timezone <timezone> \n Note: timezone MUST be in the format 'America/New_York', "
                      "for a full list of Timezones see https://github.com/GrahamCorcoran/DUDE8/blob/dev/timezones",
                inline=False)
setup.add_field(name="Preferred Notification Time",
                value="!dd notification <h> \n"
                      "ex: '!dd notification 8' for 8am.",
                inline=False)
setup.add_field(name="Notification Channel",
                value="!dd set_channel <channel> \n"
                      "ex: '!dd set_channel due-dates",
                inline=False)
setup.add_field(name="Weekly Notification",
                value="!dd set_weekly_notification <0-6> \n"
                      "ex: '!dd set_weekly_notification 0 \n"
                      "Options are 0-6 Monday-Sunday",
                inline=False)


upcoming = embeds.Embed(title="Upcoming Due Dates",
                        color=0xe67e22)
