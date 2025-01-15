import pandas as pd

class Statistics:
    def __init__(self, file_path="discord_data.csv"):
        self.file_path = file_path
        try:
            self.data = pd.read_csv(file_path)
        except FileNotFoundError:
            self.data = pd.DataFrame()

    def global_stats(self):
        """Generate global statistics."""
        if self.data.empty:
            return "No data available for global statistics."

        stats = {
            "total_messages": len(self.data[self.data["activity_type"] == "chat"]),
            "total_users": self.data["user_id"].nunique(),
            "most_active_user": self.data["user_name"].value_counts().idxmax(),
            "total_voice_events": len(self.data[self.data["activity_type"] == "voice"]),
        }

        return stats

    def user_stats(self, user_id):
        """Generate user-specific statistics. """
        if self.data.empty:
            return f"No data available for user {user_id}."

        user_data = self.data[self.data["user_id"] == user_id]
        if user_data.empty:
            return f"No data found for user {user_id}."

        stats = {
            "total_messages": len(user_data[user_data["activity_type"] == "chat"]),
            "total_voice_events": len(user_data[user_data["activity_type"] == "voice"]),
            "average_message_length": user_data["message_length"].mean(),
            "total_call_duration": user_data["call_duration"].sum(),
        }

        return stats
