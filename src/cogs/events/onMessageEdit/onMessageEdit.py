import discord
from discord.ext import commands
import sqlite3
import datetime
import json

class onMessageEdit(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        c = self.client.connection.cursor()

        sql = ("SELECT edit_channel, lang, edit_messages_log FROM guilds WHERE guild_id = ?")
        val = (str(before.guild.id), )
        c.execute(sql, val)
        values = c.fetchone()
        channel_id = values[0]
        lang = values[1]

        lang_json = "portuguese" if lang == "pt" else "english"

        if channel_id != "N" and not before.author.bot and values[2] == "S":

            with open("utils\lang\langs.json", "r", encoding="utf-8") as read:
                data = json.load(read)

            channel = before.guild.get_channel(int(channel_id))
            shortdesc = data[f"{lang_json}"]["events"]["onMessageEdit"]["Message"].replace("{user}", f"{after.author.mention}").replace("{url}", f"{after.jump_url}")
            desc_before = data[f"{lang_json}"]["events"]["onMessageEdit"]["Before"]
            desc_after = data[f"{lang_json}"]["events"]["onMessageEdit"]["After"]


            embed = discord.Embed(
                description = f"{shortdesc} \n\n {desc_before.replace('{before_message}', f'{before.content}')} \n {desc_after.replace('{after_message}', f'{after.content}')}",
                color = discord.Colour.orange()
            )
            embed.set_author(name = data[f"{lang_json}"]["events"]["onMessageEdit"]["Author"], icon_url=after.author.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
        
            await channel.send(embed = embed)


def setup(client):
    client.add_cog(onMessageEdit(client))