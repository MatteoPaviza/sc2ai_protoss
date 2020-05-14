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

import sc2_protoss_manager
from sc2_protoss_manager.base_manager import BaseManager
# from sc2_protoss_manager.proxy_manager import ProxyManager
# from sc2_protoss_manager.army_manager import ArmyManager

worker_type_id = UnitTypeId.PROBE
army_type_ids = [UnitTypeId.ZEALOT, UnitTypeId.STALKER]

class ProtossBot(BotAI):
    def __init__(self):
        # Initialize inherited class
        sc2.BotAI.__init__(self)
        # Managers
        self.base_manager: BaseManager = None
        self.print_managers_loop = 0

    async def on_start(self):
        print("~~~~~~~~~~ ON START ~~~~~~~~~~")
        await self.chat_send("Hello world !")
        self.base_manager = BaseManager(self.townhalls.first, self)

    async def on_step(self, iteration):
        if iteration == 0:
            print("~~~~~~~~~~ ON STEP 0 ~~~~~~~~~~")
        if self.time > self.print_managers_loop:
            self.print_managers_loop += 15
            print(self.base_manager)

    async def on_unit_created(self, unit: Unit):
        print(f"##### UNIT CREATED ##### [{self.time_formatted}]: {{{unit.type_id}, {unit.position}}}")
        if unit.type_id == worker_type_id:
            self.base_manager.event_worker_created(unit)
        if unit.type_id in army_type_ids:
            # self.bases.event_worker_created(unit)
            pass

    async def on_unit_destroyed(self, unit_tag: int):
        pass

    async def on_building_construction_started(self, unit: Unit):
        print(f"##### CONSTRUCTION STARTED ##### [{self.time_formatted}]: {{{unit.type_id}, {unit.position}}}")
        pass

    async def on_building_construction_complete(self, unit: Unit):
        print(f"##### CONSTRUCTION COMPLETE ##### [{self.time_formatted}]: {{{unit.type_id}, {unit.position}}}")
        pass

    async def on_enemy_unit_entered_vision(self, unit: Unit):
        pass

    async def on_enemy_unit_left_vision(self, unit_tag: int):
        pass

    async def on_upgrade_complete(self, upgrade: UpgradeId):
        print(f"##### UPGRADE COMPLETE ##### [{self.time_formatted}]: {{{upgrade}}}")
        pass

    async def on_end(self, game_result: Result):
        time = self.step_time
        print("#################### END OF GAME ####################")
        print(f"min: {time[0]}|avg: {time[1]}|max: {time[2]}")
