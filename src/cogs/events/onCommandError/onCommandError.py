import discord
from discord.ext import commands
import datetime
import sqlite3

class onCommandError(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):

            embed = discord.Embed()

            if not "prefix" in ctx.message.content:

                embed.description = "Mention the channel you want to set."

            else:
                embed.description = "Say the prefix you want to set."

            embed.set_footer(icon_url=ctx.author.avatar_url, text = f"By {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()
            embed.color = discord.Colour.red()

            await ctx.send(embed = embed)

        if isinstance(error, commands.MissingPermissions):

            embed = discord.Embed(
                description = "You don't have permission to use this command.",
                color = discord.Colour.red()
            )
            embed.set_footer(icon_url=ctx.author.avatar_url, text = f"By {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()
            
            await ctx.send(embed = embed)

        if isinstance(error, commands.CommandNotFound):

            c = self.client.connection.cursor()

            c.execute("SELECT prefix FROM guilds WHERE guild_id = ?", (str(ctx.message.guild.id), ))
            prefix = c.fetchone()[0]

            embed = discord.Embed(
                description = f"Command `{ctx.message.content.replace(prefix, '')}` was not found.",
                color = discord.Colour.red()
            )
            embed.set_footer(icon_url=ctx.author.avatar_url, text = f"By {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed = embed)

        raise error

def setup(client):
    client.add_cog(onCommandError(client))