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
from sc2_protoss_manager.protoss_manager import ProtossManager
# from sc2_protoss_manager.proxy_manager import ProxyManager
# from sc2_protoss_manager.army_manager import ArmyManager

# from sc2_protoss_manager.unit_type_categories import UnitTypeCategory
base_type_id = UnitTypeId.NEXUS
worker_type_id = UnitTypeId.PROBE
army_type_ids = [UnitTypeId.ZEALOT, UnitTypeId.STALKER]

DEBUG = True

class ProtossBot(BotAI):
    def __init__(self):
        # Initialize inherited class
        sc2.BotAI.__init__(self)

    # //////////////////////////////////////////////////////////////////////////////////////////

    async def on_before_start(self):
        # Managers
        self.manager: ProtossManager = ProtossManager([], self)

    async def on_start(self):
        if DEBUG:
            print("~~~~~~~~~~~~~~~~~~~~ GAME START ~~~~~~~~~~~~~~~~~~~~")
        await self.chat_send("GL HF !")

    async def on_step(self, iteration):
        self.manager.run(iteration)
        # self.manager.run_test(iteration)

    async def on_end(self, game_result: Result):
        time = self.step_time
        if DEBUG:
            print("~~~~~~~~~~~~~~~~~~~~ END OF GAME ~~~~~~~~~~~~~~~~~~~~")
            print(f"min: {time[0]}|avg: {time[1]}|max: {time[2]}")

    # //////////////////////////////////////////////////////////////////////////////////////////

    async def on_unit_created(self, unit: Unit):
        if DEBUG:
            print(f"##### UNIT CREATED ##### [{self.time_formatted}]: {{{unit.type_id}, {unit.position}}}")
        self.manager.on_unit_created(unit)

    async def on_unit_type_changed(self, unit: Unit, previous_type: UnitTypeId):
        self.on_unit_type_changed(unit, previous_type)

    async def on_unit_destroyed(self, unit_tag: int):
        self.manager.on_unit_destroyed(unit_tag)

    async def on_building_construction_started(self, unit: Unit):
        if DEBUG:
            print(f"##### CONSTRUCTION STARTED ##### [{self.time_formatted}]: {{{unit.type_id}, {unit.position}}}")
        self.manager.on_building_construction_started(unit)

    async def on_building_construction_complete(self, unit: Unit):
        if DEBUG:
            print(f"##### CONSTRUCTION COMPLETE ##### [{self.time_formatted}]: {{{unit.type_id}, {unit.position}}}")
        self.manager.on_building_construction_started(unit)

    async def on_unit_took_damage(self, unit: Unit, amount_damage_taken: float):
        self.manager.on_unit_took_damage(unit, amount_damage_taken)

    async def on_enemy_unit_entered_vision(self, unit: Unit):
        self.manager.on_enemy_unit_entered_vision(unit)

    async def on_enemy_unit_left_vision(self, unit_tag: int):
        self.manager.on_enemy_unit_left_vision(unit_tag)

    async def on_upgrade_complete(self, upgrade: UpgradeId):
        if DEBUG:
            print(f"##### UPGRADE COMPLETE ##### [{self.time_formatted}]: {{{upgrade}}}")
        self.manager.on_upgrade_complete(upgrade)
