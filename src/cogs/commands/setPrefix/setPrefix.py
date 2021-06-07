import discord
from discord.ext import commands
import sqlite3
import json
import datetime
from discord.ext.commands.cooldowns import BucketType


class setPrefix(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(
        name = "setPrefix",
        description = "Set a new prefix to the bot for your guild",
        usage = "[prefix]",
        aliases = ["prefix"]
    )
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.guild)
    async def setPrefix(self, ctx, prefix):

        def check(reaction, user):
            return user == ctx.author

        c = self.client.connection.cursor()

        with open("utils\lang\langs.json", "r", encoding="utf-8") as read:
            data = json.load(read)

        c.execute("SELECT lang FROM guilds WHERE guild_id = ?", (str(ctx.message.guild.id), ))
        lang = c.fetchone()[0]

        json_lang = "portuguese" if lang == "pt" else "english"

        embed = discord.Embed(
            description = data[f"{json_lang}"]["commands"]["setPrefix"]["FirstEmbed"]["Desc"].replace("{prefix}", f"{prefix}"),
            color = discord.Colour.orange()
        )
        embed.set_footer(text = data[f"{json_lang}"]["commands"]["setPrefix"]["FirstEmbed"]["Footer"].replace("{author}", f"{ctx.author}"))
        embed.set_author(icon_url=ctx.author.avatar_url, name = data[f"{json_lang}"]["commands"]["setPrefix"]["FirstEmbed"]["Confirm"])
        embed.timestamp = datetime.datetime.utcnow()

        msg = await ctx.send(embed = embed)

        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        reaction, user = await self.client.wait_for("reaction_add", timeout=60, check = check)

        if str(reaction.emoji) == "✅":

            c.execute("UPDATE guilds SET prefix = ? WHERE guild_id = ?", (prefix, str(ctx.message.guild.id)))
            self.client.connection.commit()

            embed = discord.Embed(
                description = data[f"{json_lang}"]["commands"]["setPrefix"]["SecondEmbed"]["Desc"],
                color = discord.Colour.green()
            )
            embed.set_footer(icon_url=ctx.author.avatar_url, text = data[f"{json_lang}"]["commands"]["setPrefix"]["SecondEmbed"]["Footer"].replace("{author}", f"{ctx.author}"))
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed = embed)

        if str(reaction.emoji) == "❌":
            embed = discord.Embed(
                description = data[f"{json_lang}"]["commands"]["setPrefix"]["ThirdEmbed"]["Desc"],
                color = discord.Colour.green()
            )
            embed.set_footer(icon_url=ctx.author.avatar_url, text = data[f"{json_lang}"]["commands"]["setPrefix"]["SecondEmbed"]["Footer"].replace("{author}", f"{ctx.author}"))
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed = embed)

def setup(client):
    client.add_cog(setPrefix(client))