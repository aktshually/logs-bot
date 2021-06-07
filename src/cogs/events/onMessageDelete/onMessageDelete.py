import discord
from discord.ext import commands
import sqlite3
import json
import datetime

class onMessageDelete(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):

        c = self.client.connection.cursor()

        sql = ("SELECT delete_channel, lang, delete_messages_log FROM guilds WHERE guild_id = ?")
        val = (str(message.author.guild.id), )
        c.execute(sql, val)
        values = c.fetchone()
        channel_id = values[0]
        lang = values[1]

        lang_json = "portuguese" if lang == "pt" else "english"

        if channel_id != "N" and not message.author.bot and values[2] == "S":

            with open("utils\lang\langs.json", "r", encoding="utf-8") as read:
                data = json.load(read)

            channel = message.author.guild.get_channel(int(channel_id))
            


            embed = discord.Embed(
                description = f'{data[f"{lang_json}"]["events"]["onMessageDelete"]["Message"].replace("{user}", f"{message.author.mention}")}\n\n{data[f"{lang_json}"]["events"]["onMessageDelete"]["Desc"].replace("{content}", f"{message.content}")}',
                color = discord.Colour.red()
            )
            embed.set_author(name = data[f"{lang_json}"]["events"]["onMessageDelete"]["Author"], icon_url=message.author.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
        
            await channel.send(embed = embed)

def setup(client):
    client.add_cog(onMessageDelete(client))