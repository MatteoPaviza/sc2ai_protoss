import sc2, sys, os

from __init__ import run_ladder_game
from sc2 import Race, Difficulty
from sc2.player import Bot, Computer

# Load bot
from bot import ProtossBot

maps = ['AcropolisLE', 'DiscoBloodbathLE', 'EphemeronLE', 'ThunderbirdLE', 'TritonLE', 'WintersGateLE', 'WorldofSleepersLE']
races = [Race.Protoss, Race.Terran, Race.Zerg]

map = 0
own_race = 0
computer_race = 0

bot = Bot(races[own_race], ProtossBot())

# Start game
if __name__ == "__main__":
    if "--LadderServer" in sys.argv:
        # Ladder game started by LadderManager
        print("Starting ladder game...")
        result, opponentid = run_ladder_game(bot)
        print(result, " against opponent ", opponentid)
    else:
        # Local game
        print("Starting local game...")
        sc2.run_game(sc2.maps.get(maps[map]), [bot, Computer(races[computer_race], Difficulty.Easy)], realtime=True)