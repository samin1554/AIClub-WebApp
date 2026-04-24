from app.config import settings


MOOD_QUERIES = {
    "study": "lo-fi chill beats study music",
    "hackathon": "electronic coding high energy tech",
    "chill": "ambient relaxing calm down music",
    "latenight": "late night lo-fi beats dark mood",
    "demo": "motivational upbeat celebration success",
}


class PlaylistService:
    def __init__(self):
        self.playlist_id = settings.AI_CLUB_PLAYLIST_ID

    def get_mood_query(self, mood: str) -> str:
        return MOOD_QUERIES.get(mood.lower(), MOOD_QUERIES["study"])

    def get_all_moods(self) -> list:
        return [
            {"id": "study", "name": "Study Mode", "emoji": "📚", "query": MOOD_QUERIES["study"]},
            {"id": "hackathon", "name": "Hackathon Mode", "emoji": "🚀", "query": MOOD_QUERIES["hackathon"]},
            {"id": "chill", "name": "Chill Lab", "emoji": "🧘", "query": MOOD_QUERIES["chill"]},
            {"id": "latenight", "name": "Late Night Debugging", "emoji": "🌙", "query": MOOD_QUERIES["latenight"]},
            {"id": "demo", "name": "Demo Day", "emoji": "🎉", "query": MOOD_QUERIES["demo"]},
        ]


playlist_service = PlaylistService()