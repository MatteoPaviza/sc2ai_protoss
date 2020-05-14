from itertools import chain
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union, Generator, TYPE_CHECKING

import sc2
from sc2.position import Point2
from sc2.bot_ai import BotAI
from sc2.units import Units
from sc2.unit import Unit

from sc2_protoss_manager.base import Base

class BaseManager():

    def __init__(self, first_nexus, bot_object: BotAI):
        self.bases: List[Base] = [Base(first_nexus, bot_object)]
        self._bot_object = bot_object

    @property
    def _bases(self):
        return self.bases.copy()

    def _bases_filtered_by(self, predicate: callable, reverse: bool = False) -> List[Base]:
        return filter(predicate, self._bases)

    def _bases_sorted_by(self, sorter: callable, reverse: bool = False) -> List[Base]:
        return sorted(self._bases, key=sorter, reverse=reverse)

    def _bases_sorted_by_distance_to(self, target: Union[Base, Unit, Point2], reverse: bool = False) -> List[Base]:
        return self._bases_sorted_by(lambda base: base.position._distance_squared(target.position), reverse)

    def __repr__(self):
        repr = f"ProtossBaseManager:"
        for _ in range(len(self.bases)):
            repr += f"\n[Base {_}]: -- {self.bases[_]}"
        return repr

    # //////////////////////////////////////////////////////////////////////////////////////////

    def event_worker_created(self, worker):
        closest_base = self._bases_sorted_by_distance_to(worker)[0]
        closest_base.add_worker(worker)

    def event_worker_destroyed(self, worker):
        for base in self:
            base.remove_worker(worker)

    def event_nexus_placed(self, nexus_tag):
        pass

    def event_nexus_completed(self, nexus_tag):
        pass

    def event_nexus_destroyed(self, nexus_tag):
        pass

    # //////////////////////////////////////////////////////////////////////////////////////////

    def build_pylons(self, amount):
        # TODO Order bases to build pylons, prioritize outermost ramps/chokes
        pass
