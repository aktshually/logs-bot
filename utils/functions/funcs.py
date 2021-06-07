import datetime
import discord

def create_default_embed(name, usage, description):
    
    embed = discord.Embed(
        title = f"{name} {usage}",
        description = description,
        color = discord.Colour.teal()
    )
    embed.timestamp = datetime.datetime.utcnow()

    return embed