import numpy as np
import random
from itertools import chain
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union, Generator, TYPE_CHECKING

import sc2
from sc2 import Race, Difficulty, BotAI, Result
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.buff_id import BuffId
from sc2.unit import Unit
from sc2.units import Units
from sc2.position import Point2

from data.libs.bases import Bases
from data.libs.proxies import Proxies
# from data.libs.armies import Armies

class ProtossBot(BotAI):
    def __init__(self):
        # Initialize inherited class
        sc2.BotAI.__init__(self)
        # global variables
        self.bases: Bases = Bases([], self)
        self.proxies: Proxies = Proxies([], self)
        # self.armies: Armies = Armies([], self)

    async def on_start(self):
        await self.chat_send("Hello world !")
        self.bases.create_base(self.townhalls.first)

    async def on_step(self, iteration):
        self.bases.update_bases()
        self.proxies.update_proxies()
        # self.armies.update_armies()

    async def on_end(self, game_result: Result):
        time = self.step_time
        print("########## END OF GAME ##########")
        print(f"min: {time[0]}|avg: {time[1]}|max: {time[2]}")
