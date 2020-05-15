from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union, Generator, TYPE_CHECKING

import sc2
from sc2.position import Point2
from sc2.bot_ai import BotAI
from sc2.units import Units
from sc2.unit import Unit
from sc2.ids.unit_typeid import UnitTypeId

from sc2_protoss_manager.exceptions.unit_management_exceptions import WorkerManagementException, UnitTypeException

class Base:

    def __init__(self, nexus: Unit, bot_object: BotAI):
        self._bot_object: BotAI = bot_object
        self.position: Point2 = nexus.position
        self.nexus: Unit = nexus
        self.nexus_tag: int = nexus.tag
        self.workers: Units = Units([], bot_object)
        self.mineral_nodes: Units = self._bot_object.mineral_field.filter(lambda m: m.distance_to_squared(self.position) < 64)
        self.vespene_nodes: Units = self._bot_object.vespene_geyser.filter(lambda v: v.distance_to_squared(self.position) < 64)
        self.assimilators: Units = Units([], bot_object)
        self.pylons: Units = Units([], bot_object)
        self.structures: Units = Units([], bot_object)
        # TODO self.orders = []

    @property
    def is_complete(self) -> bool:
        return self.nexus.is_ready

    def __repr__(self):
        is_complete_str = "+" if self.is_complete else "~"
        workers_str = f"{self.workers.amount}"
        ideal_workers_str = f"{self.nexus.ideal_harvesters}"
        workers_over_ideal_workers_pct = round((self.workers.amount / self.nexus.ideal_harvesters) * 100, 1)
        workers_over_ideal_workers_pct_str = f"{workers_over_ideal_workers_pct}"
        if self.workers.amount < 10:
            workers_str = "0" + workers_str
        if self.nexus.ideal_harvesters < 10:
            ideal_workers_str = "0" + ideal_workers_str
        if workers_over_ideal_workers_pct < 100:
            workers_over_ideal_workers_pct_str = " " + workers_over_ideal_workers_pct_str
            if workers_over_ideal_workers_pct < 10:
                workers_over_ideal_workers_pct_str = " " + workers_over_ideal_workers_pct_str
        return f"({is_complete_str}) W[{workers_str}/{ideal_workers_str}|{workers_over_ideal_workers_pct_str}%] P[{self.pylons.amount}]"

    # Add workers to the base
    def add_worker(self, new_worker: Unit):
        self.add_workers(Units([new_worker], self._bot_object))
    def add_workers(self, new_workers: Units):
        try:
            # Only add the units to the workers list if all of them are workers and aren't already in the list
            if new_workers.amount == new_workers(UnitTypeId.PROBE).amount:
                # Only add the units to the workers list if none them already is in the list
                if new_workers.filter(lambda w: w in self.workers).empty:
                    self.workers.extend(new_workers)
                else:
                    raise WorkerManagementException
            else:
                raise UnitTypeException
        except UnitTypeException:
            print(f"Only workers can be added to a workers list: {nw.type_id for nw in new_workers}")
            print()
        except WorkerManagementException:
            print(f"Some of the workers are already associated to the base: {nw.tag for nw in new_workers} | {w.tag for w in self.workers}")
            print()

    # Pop workers out of the base
    def pop_worker(self) -> Units:
        return self.pop_workers(1)
    def pop_workers(self, amount: int) -> Units:
        try:
            if amount <= self.workers.amount:
                return Units([self.workers.pop(0) for _ in range(amount)], self._bot_object)
            else:
                raise WorkerManagementException
        except WorkerManagementException:
            print(f"Cannot pop more workers than there are: {amount} / {self.workers.amount}")
            print()
            return Units([], self._bot_object)

    # Delete workers from the base
    # /!\ Only use these methods if the workers no longer exist (destroyed)
    def remove_worker(self, worker: Unit):
        self.remove_workers(Units([worker], self._bot_object))
    def remove_workers(self, workers: Units):
        try:
            if workers.filter(lambda w: w not in self.workers).empty:
                self.workers = self.workers.filter(lambda w: w not in workers)
            else:
                raise WorkerManagementException
        except WorkerManagementException:
            print(f"Cannot delete workers that are not associated to the base: {w.tag for w in workers}")
            print()

    def train_worker(self):
        self.nexus.train(UnitTypeId.PROBE)

    # TODO Place a pylon, prioritize ramp/choke
    def build_pylons(self, amount):
        worker = self.workers.first
        worker.move(self.position.offset([4.5,4.5]), False)
        # worker.gather(self.mineral_nodes.first, True)
