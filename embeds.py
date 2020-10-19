from discord import embeds

setup = embeds.Embed(title="Setup",
                     description="To set up dude8, the timezone and your preferred "
                                 "notification time must be set. (Default 8am) \n")
setup.set_author(name="DUDE8", url="https://github.com/GrahamCorcoran/DUDE8",
                 icon_url="https://raw.githubusercontent.com/GrahamCorcoran/DUDE8/dev/DUDE8.jpg")
setup.add_field(name="Timezone",
                value="!dd timezone <timezone> \n Note: timezone MUST be in the format 'America/New_York, "
                      "for a full list of Timezones see <link>",
                inline=False)
setup.add_field(name="Preferred Notification Time",
                value="!dd notification <h> \n"
                      "ex: '!dd notification 8' for 8am.",
                inline=False)
setup.add_field(name="Notification Channel",
                value="!dd set_channel <channel> \n"
                      "ex: '!dd set_channel due-dates",
                inline=False)
