import discord
import datetime
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from utils.functions.funcs import create_default_embed
import sqlite3


class HelpCommand(commands.HelpCommand):
    
    def __init__(self):
        attrs = {
            "cooldown":commands.Cooldown(1, 3, BucketType.user),
            "usage":"[command]",
            "description":"Invokes this message"
        }

        super().__init__(command_attrs = attrs)

    async def send_command_help(self, command: commands.Command):
        
        ctx = self.context

        embed = create_default_embed(command.name, command.usage, command.description)
        embed.set_footer(text = f"By {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed = embed)

    async def send_bot_help(self, mapping):

        ctx = self.context

        connection = sqlite3.connect("utils/db/db.db")
        c = connection.cursor()

        c.execute("SELECT prefix FROM guilds WHERE guild_id = ?", (str(ctx.message.guild.id), ))
        prefix = c.fetchone()[0]
        
        embed = discord.Embed(
            description = f"This message is invoked by using `{prefix}help`",
            color = discord.Colour.teal()
        )
        embed.set_author(icon_url=ctx.author.avatar_url, name = "Help Pannel    ")

        for value in mapping.values():
            for command in value:
                embed.add_field(name = command.name, value = command.description, inline = False)

        try:
            await ctx.author.send(embed = embed)
        except:
            embed = discord.Embed(
                description = "I can't send you my help pannel because your DM is closed.",
                color = discord.Colour.red()
            )
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                description = "I sent my help pannel by DM, check it!",
                color = discord.Colour.green()
            )
            await ctx.send(embed = embed)


    async def command_not_found(self, string):
        
        return f"Command `{string}` was not found."

        

    async def on_help_command_error(self, ctx, error):
        
        if isinstance(error, commands.CommandOnCooldown):

            embed = discord.Embed(
                description = "Wait more `{:.2f}` seconds to use this command again.".format(error.retry_after),
                color = discord.Colour.red()
            )

            embed.set_footer(icon_url=ctx.author.avatar_url, text = f"By {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed = embed)

        raise error  