from common import leaderboard_settings, DATASET_FILE
from util.leaderboard_entry import LeaderboardEntry
from util.dataset import DataSet
import datetime
import json


class DataProcessor(object):
    def __init__(self):
        self.date = None
        self.data = {}
        self.dataset = DataSet()

    def new_with_data(data):
        d = DataProcessor()
        d.date = datetime.date.fromisoformat(data["date"])
        d.data = {
            "aoe2": {},
            "aoe3": {},
            "aoe4": {},
        }

        for (
            game,
            leaderboard,
            _,
            _,
        ) in leaderboard_settings:
            collector = []
            for entry in data[game][leaderboard]:
                collector.append(
                    LeaderboardEntry(
                        steam_id=entry["steam_id"],
                        profile_id=entry["profile_id"],
                        rank=entry["rank"],
                        rating=entry["rating"],
                        highest_rating=entry["highest_rating"],
                        previous_rating=entry["previous_rating"],
                        country_code=entry["country_code"],
                        name=entry["name"],
                        known_name=entry["known_name"],
                        avatar=entry["avatar"],
                        avatarfull=entry["avatarfull"],
                        avatarmedium=entry["avatarmedium"],
                        num_games=entry["num_games"],
                        streak=entry["streak"],
                        num_wins=entry["num_wins"],
                        win_percent=entry["win_percent"],
                        rating24h=entry["rating24h"],
                        games24h=entry["games24h"],
                        wins24h=entry["wins24h"],
                        last_match=entry["last_match"],
                    )
                )

            d.data[game][leaderboard] = collector

        return d

    def export_dataset(self, file=DATASET_FILE):
        with open(file, "w") as handle:
            json.dump(self.dataset.export, handle, indent=4)

    def calculate_activity_profiles(self):
        self.dataset.export["date"] = self.date.isoformat()
        for (
            game,
            leaderboard,
            _,
            _,
        ) in leaderboard_settings:
            activity_30d = 0
            activity_14d = 0
            activity_7d = 0
            activity_3d = 0
            activity_1d = 0

            if leaderboard == "unranked" and game == "aoe2":
                pass

            for entry in self.data[game][leaderboard]:
                if entry.last_activity(self.date, 30):
                    activity_30d += 1
                if entry.last_activity(self.date, 14):
                    activity_14d += 1
                if entry.last_activity(self.date, 7):
                    activity_7d += 1
                if entry.last_activity(self.date, 3):
                    activity_3d += 1
                if entry.last_activity(self.date, 1):
                    activity_1d += 1

            self.dataset.export["activity"]["30d"][game][
                leaderboard
            ] = activity_30d
            self.dataset.export["activity"]["14d"][game][
                leaderboard
            ] = activity_14d
            self.dataset.export["activity"]["7d"][game][
                leaderboard
            ] = activity_7d
            self.dataset.export["activity"]["3d"][game][
                leaderboard
            ] = activity_3d
            self.dataset.export["activity"]["1d"][game][
                leaderboard
            ] = activity_1d
