import discord
from discord.ext import commands
import sqlite3
import json
import datetime

from discord.ext.commands.cooldowns import BucketType

class deactivateCreateChannelLogs(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(
        name = "deactivateChannelCreateLogs",
        description = "Deactivate logs for created channels",
        usage = ""
    )
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 5, BucketType.guild)
    async def deactivateChannelCreateLogs(self, ctx):

        def check(reaction, user):
            return user == ctx.author

        c = self.client.connection.cursor()
        
        with open("utils\lang\langs.json", "r", encoding="utf-8") as read:
            data = json.load(read)

        sql = ("SELECT lang, create_channel_log FROM guilds WHERE guild_id = ?")
        val = (str(ctx.author.guild.id), )
        c.execute(sql, val)
        value = c.fetchone()
        lang_json = "portuguese" if value[0] == "pt" else "english"

        embed = discord.Embed(
            description = data[f"{lang_json}"]["commands"]["deactivateChannelCreateLog"]["FirstEmbed"]["Desc"],
            color = discord.Colour.orange()
        )
        embed.set_author(icon_url = ctx.author.avatar_url, name = data[f"{lang_json}"]["commands"]["deactivateChannelCreateLog"]["FirstEmbed"]["Confirm"])
        embed.set_footer(text = data[f"{lang_json}"]["commands"]["deactivateChannelCreateLog"]["FirstEmbed"]["Footer"])
        embed.timestamp = datetime.datetime.utcnow()

        msg = await ctx.send(embed = embed)

        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        reaction, user = await self.client.wait_for("reaction_add", timeout = 60, check = check)

        if str(reaction.emoji) == "✅":
            
            sql = ("UPDATE guilds SET create_channel_log = ? WHERE guild_id = ?")
            val = ("N", str(ctx.author.guild.id))
            c.execute(sql, val)
            self.client.connection.commit()

            embed = discord.Embed(
                description = data[f"{lang_json}"]["commands"]["deactivateChannelCreateLog"]["SecondEmbed"]["Desc"],
                color = discord.Colour.green()
            )
            embed.set_footer(icon_url = ctx.author.avatar_url, text = data[f"{lang_json}"]["commands"]["deactivateChannelCreateLog"]["SecondEmbed"]["Footer"].replace("{author}", f"{ctx.author}"))
            embed.timestamp = datetime.datetime.utcnow()

            await msg.edit(embed = embed)

        elif str(reaction.emoji) == "❌":

            embed = discord.Embed(
                description = data[f"{lang_json}"]["commands"]["deactivateChannelCreateLog"]["ThirdEmbed"]["Desc"],
                color = discord.Colour.red()
            )
            embed.set_footer(icon_url = ctx.author.avatar_url, text = data[f"{lang_json}"]["commands"]["deactivateChannelCreateLog"]["ThirdEmbed"]["Footer"].replace("{author}", f"{ctx.author}"))
            embed.timestamp = datetime.datetime.utcnow()

            await msg.edit(embed = embed)

def setup(client):
    client.add_cog(deactivateCreateChannelLogs(client))