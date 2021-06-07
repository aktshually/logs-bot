import discord
from discord.ext import commands
import sqlite3
import os
import re
from utils.config.config import TOKEN
from utils.HelpCommand.HelpCommand import HelpCommand

async def get_prefix(client, message):

    c = client.connection.cursor()
    sql = ("SELECT prefix FROM guilds WHERE guild_id = ?")
    value = (message.guild.id, )
    c.execute(sql, value)
    prefix = c.fetchone()
    return prefix[0]

client = commands.Bot(command_prefix = get_prefix, intents = discord.Intents.all())
client.help_command = HelpCommand()
client.connection = sqlite3.connect("utils/db/db.db")

async def close():
    client.connection.close()

client.close = close

ext = []

def getcog():

    for root, _, files in os.walk("src/cogs"):

        for file in files:

            path = os.path.join(root, file)

            if not os.path.isfile(path):
                continue

            path, exten = os.path.splitext(path)
            if exten != ".py":
                continue
            
            ext.append(re.sub(r"\\|\/", ".", path))

    return ext

for extension in getcog():
    client.load_extension(extension)

client.run(TOKEN)