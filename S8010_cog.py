# cog for S8010 (S8010_cog.py) ###
# commands for the discord bot ###
#

# test slash command

from discord.ext import commands
from discord import app_commands, User

from S8010_stats import Statistics

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

    @app_commands.command(name="global_stats", description="View global statistics.")
    async def global_stats(self, interaction):
        stats = Statistics().global_stats()
        if isinstance(stats, str):
            await interaction.response.send_message(stats)
        else:
            message = "\n".join([f"{key}: {value}" for key, value in stats.items()])
            await interaction.response.send_message(f"Global Statistics:\n{message}")

    @app_commands.command(name="user_stats", description="View statistics for a specific user.")
    async def user_stats(self, interaction, user: User):
        """Fetch and display statistics for a specific user."""
        stats = Statistics().user_stats(user.id)
        if isinstance(stats, str):
            await interaction.response.send_message(stats)
        else:
            message = f"Statistics for {user.display_name}:\n"
            message += "\n".join([f"{key}: {value}" for key, value in stats.items()])
            await interaction.response.send_message(message)
