# cog for S8010 (S8010_cog.py) ###
# commands for the discord bot ###
#

# test slash command

from discord.ext import commands
from discord import app_commands

class S8010Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test")
    async def test_command(self, ctx):
        await ctx.send("Test command works!")

    @app_commands.command(name="test", description="Test command")
    async def test_command(self, interaction):
        await interaction.response.send_message("Test command works!")

    @app_commands.command(name="change_prefix", description="Change the bot's prefix")
    async def change_prefix(self, interaction, prefix: str):
        self.bot.command_prefix = prefix
        await interaction.response.send_message(f"Prefix changed to {prefix}")
