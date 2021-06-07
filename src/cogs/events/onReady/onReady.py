import discord
from discord.ext import commands

class onReady(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):

        await self.client.change_presence(status = discord.Status.online, activity = discord.Activity(type = discord.ActivityType.watching, name = "lb!help"))

        print(f"Logged as: {self.client.user}")
        print(f"Conectado como: {self.client.user}")

def setup(client):
    client.add_cog(onReady(client))