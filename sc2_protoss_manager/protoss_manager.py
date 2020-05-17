from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union, Generator, TYPE_CHECKING
import cv2, math
import numpy as np
# import tensorflow as tf
# from tensorflow import keras

import sc2
from sc2.position import Point2
from sc2.bot_ai import BotAI
from sc2.units import Units
from sc2.unit import Unit
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.ability_id import AbilityId

from .base import Base
from .proxy import Proxy
from .army import Army

NEXUS_ID = UnitTypeId.NEXUS
PYLON_ID = UnitTypeId.PYLON
WORKER_ID = UnitTypeId.PROBE
TRAININGFACILITIES_IDS = [UnitTypeId.GATEWAY, UnitTypeId.STARGATE, UnitTypeId.ROBOTICSFACILITY]
RESEARCHFACILITIES_IDS = [UnitTypeId.FORGE, UnitTypeId.CYBERNETICSCORE, UnitTypeId.ROBOTICSBAY, UnitTypeId.FLEETBEACON, UnitTypeId.TWILIGHTCOUNCIL, UnitTypeId.TEMPLARARCHIVE, UnitTypeId.DARKSHRINE]
DEFENSESTRUCTURES_IDS = [UnitTypeId.PHOTONCANNON, UnitTypeId.SHIELDBATTERY]
SOLDIERS_IDS = [UnitTypeId.ZEALOT, UnitTypeId.STALKER, UnitTypeId.SENTRY, UnitTypeId.ADEPT, UnitTypeId.HIGHTEMPLAR, UnitTypeId.DARKTEMPLAR, UnitTypeId.ARCHON, UnitTypeId.PHOENIX, UnitTypeId.ORACLE, UnitTypeId.VOIDRAY, UnitTypeId.CARRIER, UnitTypeId.TEMPEST, UnitTypeId.OBSERVER, UnitTypeId.WARPPRISM, UnitTypeId.IMMORTAL, UnitTypeId.COLOSSUS, UnitTypeId.DISRUPTOR, UnitTypeId.MOTHERSHIP]

class ProtossManager():

    def __init__(self, bot_object: BotAI):
        # self.early_guidance = early_guidance
        self._bot_object = bot_object
        self.bases: List[Base] = [Base(bot_object.townhalls.first, bot_object)]
        self.proxies: List[Proxy] = []
        self.armies: List[Army] = []
        self.map_size = bot_object.game_info.map_size

    def run(self, iteration):
        pass

    def run_test(self, iteration):
        pass

    # //////////////////////////////////////////////////////////////////////////////////////////

    def _bases_find_by_nexus_tag(self, nexus_tag: int) -> Base:
        for base in self.bases:
            if base.nexus_tag == nexus_tag:
                return base
        return None

    def _bases_filtered_by(self, predicate: callable) -> List[Base]:
        return list(filter(predicate, self.bases))

    def _bases_sorted_by(self, sorter: callable, reverse: bool = False) -> List[Base]:
        return sorted(self.bases, key=sorter, reverse=reverse)

    def _bases_sorted_by_distance_to(self, target: Union[Base, Unit, Point2], reverse: bool = False) -> List[Base]:
        return self._bases_sorted_by(lambda base: base.position._distance_squared(target.position), reverse)

    def __repr__(self):
        repr = f"ProtossManager:"
        for _ in range(len(self.bases)):
            repr += f"\n[Base {_}]: -- {self.bases[_]}"
        return repr

    # //////////////////////////////////////////////////////////////////////////////////////////

    def on_unit_created(self, unit: Unit):
        if unit.type_id == WORKER_ID:
            closest_base = self._bases_sorted_by_distance_to(unit)[0]
            closest_base.add_worker(unit)
        elif unit.type_id in SOLDIERS_IDS:
            # self.on_soldier_created(unit)
            pass

    def on_unit_type_changed(self, unit: Unit, previous_type: UnitTypeId):
        pass

    def on_unit_destroyed(self, unit_tag: int):
        for base in self.bases:
            if base.remove_worker(unit_tag):
                return

    def on_building_construction_started(self, building: Unit):
        if building.type_id == NEXUS_ID:
            self.bases.append(Base(building, self._bot_object))
        elif building.type_id == PYLON_ID:
            closest_base = self._bases_sorted_by_distance_to(building)[0]
            closest_base.add_pylon(building)
        elif building.type_id in TRAININGFACILITIES_IDS:
            pass
        elif building.type_id in RESEARCHFACILITIES_IDS:
            pass

    def on_building_construction_complete(self, building: Unit):
        pass

    def on_unit_took_damage(self, unit: Unit, amount_damage_taken: float):
        pass

    def on_enemy_unit_entered_vision(self, unit: Unit):
        pass

    def on_enemy_unit_left_vision(self, unit_tag: int):
        pass

    def on_upgrade_complete(self, upgrade: UpgradeId):
        pass

    # //////////////////////////////////////////////////////////////////////////////////////////

    def on_nexus_destroyed(self, nexus_tag):
        self.bases = self._bases_filtered_by(lambda base: base.nexus_tag == nexus_tag)

    # //////////////////////////////////////////////////////////////////////////////////////////

    # TODO Order bases to build pylons, prioritize outermost ramps/chokes
    def build_pylons(self, amount):
        pass
        # self.bases[0].build_pylons(1)
