import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import sqlite3

class Invite(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(
        name = "invite",
        description = "Display my invite link. By using it, you can add me into your guild.",
        usage = "",
        aliases = ["convite", "Invite"]
    )
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    async def invite(self, ctx):

        c = self.client.connection.cursor()

        c.execute("SELECT lang FROM guilds WHERE guild_id = ?", (str(ctx.message.guild.id), ))
        lang = c.fetchone()[0]

        desc1 = "Necessary Permissions" if lang == "en" else "Permissões necessárias"
        desc2 = "Administrator permissions" if lang == "en" else "Permissões de administrador"

        embed = discord.Embed(
            description = f"[{desc1}](https://discord.com/api/oauth2/authorize?client_id=845430371771613224&permissions=0&scope=bot)\n[{desc2}](https://discord.com/api/oauth2/authorize?client_id=845430371771613224&permissions=8&scope=bot)",
            color = 0x36393f
        )
        embed.set_author(icon_url=ctx.author.avatar_url, name = "Invite" if lang == "en" else "Convite")

        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Invite(client))