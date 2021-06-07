import discord
from discord.ext import commands
import sqlite3

class onGuildJoin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        c = self.client.connection.cursor()

        sql = ("INSERT INTO guilds(guild_id) VALUES(?)")
        val = (str(guild.id), )
        c.execute(sql, val)
        self.client.connection.commit()


def setup(client):
    client.add_cog(onGuildJoin(client))