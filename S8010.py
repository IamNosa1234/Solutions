import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timezone
from discord.ext import commands
from discord import Intents
from S8010_cog import S8010Cog


class DiscordBot(commands.Bot):
    def __init__(self):
        load_dotenv()

        self.get_intents = self.get_intents()
        self.token = os.getenv("DISCORD_BOT_TOKEN")

        # Setup DataFrame for collected data
        self.columns = [
            "user_id", "user_name", "channel_id", "channel_name", "activity_type",
            "message_id", "message_content", "message_length", "time_date",
            "voice_channel_id", "voice_channel_name", "voice_event_type", "call_duration"
        ]  # add presence state,
        try:
            self.data = pd.read_csv("discord_data.csv")
        except FileNotFoundError:
            self.data = pd.DataFrame(columns=self.columns)

        super().__init__(command_prefix="!", intents=self.get_intents)

    @staticmethod
    def get_intents():
        intents = Intents.default()
        intents.message_content = True
        intents.messages = True
        intents.voice_states = True
        return intents

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_connect(self):
        # Add the cog to the bot
        await self.add_cog(S8010Cog(self))
        try:
            await self.tree.sync()  # Sync the slash commands with Discord
            print("Slash commands synced!")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

    async def on_message(self, message):
        """Log text messages."""
        if message.author == self.user or message.author.bot:
            return

        data = {
            "user_id": message.author.id,
            "user_name": str(message.author),
            "channel_id": message.channel.id,
            "channel_name": str(message.channel),
            "activity_type": "chat",
            "message_id": message.id,
            "message_content": message.content,
            "message_length": len(message.content),
            "time_date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "voice_channel_id": None,
            "voice_channel_name": None,
            "voice_event_type": None
            # solution for *Voice* messages from phone?
        }
        self.store_data(data)

        await self.process_commands(message)

    async def on_voice_state_update(self, member, before, after):
        """Log voice channel activities."""
        voice_event = None
        voice_channel_id = None
        voice_channel_name = None

        if before.channel is None and after.channel is not None:
            voice_event = "join_voice"
            voice_channel_id = after.channel.id
            voice_channel_name = after.channel.name
        elif before.channel is not None and after.channel is None:
            voice_event = "leave_voice"
            voice_channel_id = before.channel.id
            voice_channel_name = before.channel.name
        elif before.self_deaf != after.self_deaf:
            voice_event = "deaf" if after.self_deaf else "undeaf"
            voice_channel_id = after.channel.id if after.channel else None
            voice_channel_name = after.channel.name if after.channel else None
        elif before.self_mute != after.self_mute:
            voice_event = "mute" if after.self_mute else "unmute"
            voice_channel_id = after.channel.id if after.channel else None
            voice_channel_name = after.channel.name if after.channel else None
        # log channel switching? if possible include whether user switched or was moved by admin (moved_by_admin(bool), admin name/id)
        print(voice_event, "in", voice_channel_name, "by", member)  # for debugging

        if voice_event:
            data = {
                "user_id": member.id,
                "user_name": str(member),
                "channel_id": None,
                "channel_name": None,
                "activity_type": "voice",
                "message_id": None,
                "message_content": None,
                "message_length": None,
                "time_date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                "voice_channel_id": voice_channel_id,
                "voice_channel_name": voice_channel_name,
                "voice_event_type": voice_event
            }
            self.store_data(data)

    def store_data(self, data):
        """Store data to DataFrame and save to CSV."""
        self.data = pd.concat([self.data, pd.DataFrame([data])], ignore_index=True)
        self.data.to_csv("discord_data.csv", index=False)


if __name__ == "__main__":
    bot = DiscordBot()
    bot.run(bot.token)

