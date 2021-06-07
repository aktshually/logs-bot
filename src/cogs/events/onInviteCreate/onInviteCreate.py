import discord
from discord.ext import commands
import sqlite3
import json
import datetime


class onInviteCreate(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_invite_create(self, invite):

        c = self.client.connection.cursor()

        sql = ("SELECT invite_channel, lang, invite_log FROM guilds WHERE guild_id = ?")
        val = (str(invite.guild.id), )
        c.execute(sql, val)
        values = c.fetchone()
        channel_id = values[0]
        lang = values[1]

        lang_json = "portuguese" if lang == "pt" else "english"

        if channel_id != "N" and values[2] == "S":

            with open("utils\lang\langs.json", "r", encoding="utf-8") as read:
                data = json.load(read)

            channel = invite.guild.get_channel(int(channel_id))

            embed = discord.Embed(
                description = data[f"{lang_json}"]["events"]["onInviteCreate"]["Message"].replace("{url}", f"{invite.url}").replace("{user}", f"{invite.inviter.mention}"),
                color = discord.Colour.green()
            )
            embed.set_author(name = data[f"{lang_json}"]["events"]["onInviteCreate"]["Author"], icon_url=invite.inviter.avatar_url)
            embed.set_thumbnail(url = invite.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()
        
            await channel.send(embed = embed)

def setup(client):
    client.add_cog(onInviteCreate(client))