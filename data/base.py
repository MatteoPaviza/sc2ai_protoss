from itertools import chain
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union, Generator, TYPE_CHECKING

import sc2
from sc2.position import Point2
from sc2.bot_ai import BotAI
from sc2.units import Units
from sc2.unit import Unit
from sc2.ids.unit_typeid import UnitTypeId

class BaseWorkerException(Exception):
    pass

class Base:
    def __init__(self, nexus: Unit, bot_object: BotAI):
        self._bot_object: BotAI = bot_object
        self.location: Point2 = nexus.location
        self.nexus: Unit = nexus
        self.workers: Units = Units([], bot_object)
        self.mineral_nodes: Units = self._bot_object.mineral_field.filter(lambda m: m.ditance_to_squared(self.location) < 64)
        self.vespene_nodes: Units = self._bot_object.vespene_geyser.filter(lambda v: v.ditance_to_squared(self.location) < 64)
        self.assimilators: Units = Units([], bot_object)
        self.pylons: Units = Units([], bot_object)
        self.structures: Units = Units([], bot_object)
        self.base_orders = []

    @property
    def is_alive(self) -> bool:
        return not self.nexus.is_memory

    def update_collections(self):
        print("update_collections")
        # self.workers = self.workers.filter(lambda w: w in self._bot_object.workers)
        # self.mineral_nodes = self.mineral_nodes.filter(lambda m: m in self._bot_object.mineral_field)
        # self.vespene_nodes = self.vespene_nodes.filter(lambda v: v in self._bot_object.vespene_geyser)
        # self.assimilators = self.assimilators.filter(lambda a: a in self._bot_object.gas_buildings)
        # self.pylons = self.pylons.filter(lambda p: not p.is_memory)
        # self.structures = self.structures.filter(lambda s: not s.is_memory)

    # Add workers to the base
    def add_worker(self, new_worker: Unit):
        self.add_workers(Units([new_worker], new_worker._bot_object))
    def add_workers(self, new_workers: Units):
        try:
            if new_workers.amount == new_workers(UnitTypeId.PROBE).amount:
                self.workers.extend(new_workers)
            else:
                raise BaseWorkerException
        except BaseWorkerException:
            print(f"Only workers can be added to a workers list: {nw.type_id for nw in new_workers}")
            print()

    # Pop workers out of the base
    def pop_worker(self) -> Units:
        return self.pop_workers(1)
    def pop_workers(self, amount: int) -> Units:
        try:
            if amount <= self.workers.amount:
                return Units([self.workers.pop(0) for _ in range(amount)], self._bot_object)
            else:
                raise BaseWorkerException
        except BaseWorkerException:
            print(f"Cannot pop more workers than there are: {amount} / {self.workers.amount}")
            print()
            return Units([], self._bot_object)

    # Delete workers from the base
    # /!\ Only use these methods if the workers no longer exist
    def remove_worker(self, worker: Unit):
        self.remove_workers(Units([worker], self._bot_object))
    def remove_workers(self, workers: Units):
        try:
            if workers.filter(lambda w: w not in self.workers).empty:
                self.workers = self.workers.filter(lambda w: w not in workers)
            else:
                raise BaseWorkerException
        except BaseWorkerException:
            print(f"Cannot delete workers that are not part of the base: {w.tag for w in workers}")
            print()
