from discord import embeds

welcome = embeds.Embed(title="DUDE8 Setup",
                       description="To set up dude8, the timezone and your preferred "
                                   "notification time must be set. (Default 8am) \n")
welcome.add_field(name="Timezone",
                  value="!dd timezone <timezone> \n Note: timezone MUST be in the format 'America/New_York, "
                        "for a full list of Timezones see <link>",
                  inline=False)
welcome.add_field(name="Preferred Notification Time",
                  value="!dd notification <h> \n"
                        "ex: '!dd notification 8' for 8am.",
                  inline=False)


