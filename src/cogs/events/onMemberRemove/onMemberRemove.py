import json
import discord
from discord.ext import commands
import sqlite3
import datetime

class onMemberRemove(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        c = self.client.connection.cursor()

        sql = ("SELECT welcome_channel, lang FROM guilds WHERE guild_id = ?")
        val = (str(member.guild.id), )
        c.execute(sql, val)
        values = c.fetchone()
        channel_id = values[0]
        lang_json = "portuguese" if values[1] == "pt" else "english"

        if channel_id != 'N':

            with open("utils\lang\langs.json", "r") as read:
                data = json.load(read)

            channel = member.guild.get_channel(channel_id)

            embed = discord.Embed(
                description = data[f"{lang_json}"]["events"]["onMemberRemove"]["Message"].replace("{user}", f"{member.mention}"),
                color = discord.Colour.green()
            )
            embed.set_author(name = data[f"{lang_json}"]["events"]["onMemberRemove"]["Author"].replace("{user}", f"{member.mention}"), icon_url = member.guild.icon_url)
            embed.set_thumbnail(url = member.avatar_url)

            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(emebd = embed)

def setup(client):
    client.add_cog(onMemberRemove(client))