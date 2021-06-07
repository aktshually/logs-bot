import discord
from discord.ext import commands
import sqlite3
import datetime
import json

from discord.ext.commands.cooldowns import BucketType

class setWelcomeLogChannel(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name = "setWelcomeChannel",
        description = "Set a channel for members who joined or leaved from your guild",
        usage = "[channel]"
    )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, BucketType.guild)
    async def setWelcomeChannel(self, ctx, channel: discord.TextChannel):

        c = self.client.connection.cursor()

        sql = ("SELECT lang, welcome_messages_log, prefix FROM guilds WHERE guild_id = ?")
        val = (str(ctx.author.guild.id), )
        c.execute(sql, val)
        value = c.fetchone()
        lang_json = "portuguese" if value[0] == "pt" else "english"

        def check(reaction, user):
            return user == ctx.author

        with open("utils\lang\langs.json", "r", encoding="utf-8") as read:
            data = json.load(read)

        embed = discord.Embed(
            title = data[f"{lang_json}"]["commands"]["setWelcomeLogChannel"]["FirstEmbed"]["Confirm"],
            description = data[f"{lang_json}"]["commands"]["setWelcomeLogChannel"]["FirstEmbed"]["Desc"].replace("{mentionauthor}", f"{ctx.author.mention}").replace("{mentionchannel}", f"{channel.mention}").replace("{prefix}", f"{value[2]}") if value[1] == "S" else data[f"{lang_json}"]["commands"]["setWelcomeLogChannel"]["FirstEmbed"]["PossibleDesc"].replace("{mentionauthor}", f"{ctx.author.mention}").replace("{mentionchannel}", f"{channel.mention}").replace("{prefix}", f"{value[2]}"),
            color = discord.Colour.orange()
        )
        embed.set_footer(text = data[f"{lang_json}"]["commands"]["setWelcomeLogChannel"]["FirstEmbed"]["Footer"].replace("{author}", f"{ctx.author}"), icon_url = ctx.author.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()

        msg = await ctx.send(embed = embed)

        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        reaction, user = await self.client.wait_for("reaction_add", timeout = 60, check = check)

        if str(reaction.emoji) == "✅":

            sql = ("UPDATE guilds SET welcome_channel = ? WHERE guild_id = ?")
            val = (str(channel.id), str(ctx.guild.id))

            c.execute(sql, val)
            self.client.connection.commit() 

            embed = discord.Embed(
                description = data[f"{lang_json}"]["commands"]["setWelcomeLogChannel"]["SecondEmbed"]["Desc"],
                color = discord.Colour.green()
            )
            embed.set_footer(icon_url=ctx.author.avatar_url, text = data[f"{lang_json}"]["commands"]["setWelcomeLogChannel"]["SecondEmbed"]["Footer"].replace("{mentionauthor}", f"{ctx.author}"))
            embed.timestamp = datetime.datetime.utcnow()

            await msg.edit(embed = embed)

        elif str(reaction.emoji) == "❌":

            embed = discord.Embed(
                description = data[f"{lang_json}"]["commands"]["setWelcomeLogChannel"]["ThirdEmbed"]["Desc"],
                color = discord.Colour.red()
            )
            embed.set_footer(icon_url=ctx.author.avatar_url, text = data[f"{lang_json}"]["commands"]["setWelcomeLogChannel"]["ThirdEmbed"]["Footer"].replace("{author}", f"{ctx.author}"))
            embed.timestamp = datetime.datetime.utcnow()

            await msg.edit(embed = embed)

def setup(client):
    client.add_cog(setWelcomeLogChannel(client))