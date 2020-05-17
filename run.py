import sys, os

import sc2
from sc2 import Race, Difficulty
from sc2.player import Bot, Computer

from __init__ import run_ladder_game
from bot import ProtossBot

MAPS = ['AcropolisLE', 'DiscoBloodbathLE', 'EphemeronLE', 'ThunderbirdLE', 'TritonLE', 'WintersGateLE', 'WorldofSleepersLE']
RACES = [Race.Protoss, Race.Terran, Race.Zerg]
COMPUTER_DIFFICULTIES = [Difficulty.Easy, Difficulty.Medium, Difficulty.Hard, Difficulty.VeryHard]

map = 0
own_race = 0
computer_race = 0
computer_difficulty = 0

bot = Bot(RACES[own_race], ProtossBot())

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
        sc2.run_game(sc2.maps.get(MAPS[map]), [bot, Computer(RACES[computer_race], Difficulty.Easy)], realtime=True)