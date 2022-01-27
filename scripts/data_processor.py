import logging
import datetime
import os
import json

# Intern
from common import leaderboard_settings, CACHE_FILE

LOGGER = logging.getLogger(__name__)

DEBUG = True

# Check for cache hit
if os.path.exists(CACHE_FILE):
    CACHE_HIT = True
    with open(CACHE_FILE, encoding="utf8", mode="r") as handle:
        main_data = json.load(handle)
else:
    CACHE_HIT = False

# Set Debug logging if necessary
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
elif not DEBUG:
    logging.basicConfig(level=logging.INFO)

for leaderboard_setting in leaderboard_settings:
    # TODO: Temporary Flatten
    

# What can be derived:
# - we can make the players unique on each leaderboard
#   and count them -> same as now, but unique
# - we can count players within a certain amount of activity,
#   e.g. within last day, last 3 days, last 7 days, last 14 days
# - we can join all the unique players across the leaderboards
#   and create overall game activity
# - we can join all the unique players across the games and create
#   overall franchise (AoE2DE, AoE3DE, AoE4) multiplayer activity