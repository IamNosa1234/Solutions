# Idea: create datasets from my discord community
# create funny statistics and graphs using this data

import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt # for plotting
from discord.ext import commands
from discord import Intents

# Create a Discord class for discord bot, to connect to the server.
class DiscordBot(commands.Bot):
    def __init__(self):
        load_dotenv()

        self.get_intents = self.get_intents()
        self.token = os.getenv("DISCORD_BOT_TOKEN")

        self.columns = ["user_id", "channel_id", "message_id", "message_content", "message_lenght", "time_date",
                        "edited", "last_edit_time_date", "edit_count", "author_name", "author_discriminator", "author_nick",
                        "channel_name", "is_reply", "reply_to_message_id", "reply_to_message_content"]

        columns = [
            "user_id", "user_name", "channel_id", "channel_name", "activity_type",
            "message_id", "message_content", "message_length", "time_date",
            "voice_channel_id", "voice_channel_name", "voice_event_type"
        ]

        try:
            self.data = pd.read_csv("discord_data.csv")
        except FileNotFoundError as e:
            print(f"Data file not found. Please make sure to run the data collection script first. ({e})")

        super().__init__(command_prefix="!", intents=self.get_intents)

    @staticmethod
    def get_intents():
        intents = Intents.default()
        intents.message_content = True
        intents.messages = True
        return intents

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    @staticmethod
    async def on_connect():
        print(f"Connected to Discord")

    async def on_message(self, message):
        if message.author == self.user or message.author.bot:
            return
        print(f"{message.author}: {message.content}")

        if message.content == "!stats":
            await message.channel.send("Creating statistics...")
            self.create_statistics()

    def create_statistics(self):
        # Create a bar chart for the number of messages sent by each user
        message_counts = self.data["author"].value_counts()
        message = "```"

        for author, count in message_counts.items():
            message += f"{author}: {count}\n"


if __name__ == "__main__":
    bot = DiscordBot()
    bot.run(bot.token)
