import discord
from discord.ext import commands
import sqlite3
import json
import datetime

from discord.ext.commands.cooldowns import BucketType

class changeLang(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(
        name = "changeLang",
        description = "Change bot's language. I have support to EN-US or PT-BR",
        usage = ""
    )
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 2, BucketType.user)
    async def changeLang(self, ctx):

        def check(reaction, user):
            return user == ctx.author

        c = self.client.connection.cursor()

        sql = ("SELECT lang FROM guilds WHERE guild_id = ?")
        val = (str(ctx.author.guild.id), )
        c.execute(sql, val)
        lang = c.fetchone()[0]

        json_lang = "portuguese" if lang == "pt" else "english"

        with open("utils\lang\langs.json", "r", encoding="utf-8") as read:
            data = json.load(read)
        
        embed = discord.Embed(
            description = "🇧🇷 | PT-BR\n🇺🇸 | EN-US",
            color = discord.Colour.teal()
        )
        embed.set_author(icon_url = ctx.author.avatar_url, name = data[f"{json_lang}"]["commands"]["changeLang"]["FirstEmbed"]["Options"])
        embed.set_footer(text = data[f"{json_lang}"]["commands"]["changeLang"]["FirstEmbed"]["Footer"])

        msg = await ctx.send(embed = embed)

        await msg.add_reaction("🇧🇷")
        await msg.add_reaction("🇺🇸")

        reaction, user = await self.client.wait_for("reaction_add", timeout = 60, check = check)

        if str(reaction.emoji) == "🇧🇷":

            sql = ("UPDATE guilds SET lang = ? WHERE guild_id = ?")
            val = ("pt", str(ctx.author.guild.id))
            c.execute(sql, val)
            self.client.connection.commit()

            embed = discord.Embed(
                description = "✅ | A linguagem foi mudada com sucesso!",
                color = discord.Colour.green()
            )
            embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requisitado por {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed = embed)

        elif str(reaction.emoji) == "🇺🇸":

            sql = ("UPDATE guilds SET lang = ? WHERE guild_id = ?")
            val = ("en", str(ctx.author.guild.id))
            c.execute(sql, val)
            self.client.connection.commit()

            embed = discord.Embed(
                description = "✅ | The language has been changed sucessfully!",
                color = discord.Colour.green()
            )
            embed.set_footer(icon_url = ctx.author.avatar_url, text = f"By {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed = embed)

def setup(client):
    client.add_cog(changeLang(client))