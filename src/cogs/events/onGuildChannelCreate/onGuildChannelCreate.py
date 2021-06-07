import discord
from discord.ext import commands
import sqlite3
import json
import datetime


class onGuildCreateChannel(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):

        c = self.client.connection.cursor()

        sql = ("SELECT create_channel_channel, lang, create_channel_log FROM guilds WHERE guild_id = ?")
        val = (str(channel.guild.id), )
        c.execute(sql, val)
        values = c.fetchone()
        channel_id = values[0]
        lang = values[1]

        lang_json = "portuguese" if lang == "pt" else "english"

        if channel_id != "N" and values[2] == "S":

            with open("utils\lang\langs.json", "r", encoding="utf-8") as read:
                data = json.load(read)

            channel = channel.guild.get_channel(int(channel_id))

            embed = discord.Embed(
                description = data[f"{lang_json}"]["events"]["onGuildChannelCreate"]["Message"].replace("{channel}", f"{channel.mention}").replace("{id}", f"{channel.id}"),
                color = discord.Colour.green()
            )
            embed.set_author(name = data[f"{lang_json}"]["events"]["onGuildChannelCreate"]["Author"], icon_url=channel.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()
        
            await channel.send(embed = embed)

def setup(client):
    client.add_cog(onGuildCreateChannel(client))