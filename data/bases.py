from itertools import chain
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union, Generator, TYPE_CHECKING

import sc2
from sc2.position import Point2
from sc2.bot_ai import BotAI
from sc2.units import Units
from sc2.unit import Unit

from base import Base

class Bases(list):

    def __init__(self, bases, bot_object: BotAI):
        super().__init__(bases)
        self._bot_object = bot_object

    def __or__(self, other):
        return Bases(
            chain(
                iter(self),
                (other_base for other_base in other if other_base.location not in (self_base.location for self_base in self)),
            ),
            self._bot_object,
        )

    def __add__(self, other):
        return Bases(
            chain(
                iter(self),
                (other_base for other_base in other if other_base.location not in (self_base.location for self_base in self)),
            ),
            self._bot_object,
        )

    def __and__(self, other):
        return Bases(
            (other_base for other_base in other if other_base.location in (self_base.location for self_base in self)),
            self._bot_object,
        )

    def __sub__(self, other):
        return Bases(
            (self_base for self_base in self if self_base.location not in (other_base.location for other_base in other)),
            self._bot_object,
        )

    def __hash__(self):
        return hash(base.location for base in self)

    def copy(self):
        return self.subgroup(self)

    def subgroup(self, bases):
        return Bases(bases, self._bot_object)

    def filter(self, pred: callable):
        assert callable(pred), "Function is not callable"
        return self.subgroup(filter(pred, self))

    def sorted(self, key: callable, reverse: bool = False):
        return self.subgroup(sorted(self, key=key, reverse=reverse))

    def _list_sorted_by_distance_to(self, position: Union[Base, Unit, Point2], reverse: bool = False) -> List[Base]:
        if isinstance(position, Base):
            return sorted(
                self, key=lambda base: self._bot_object._distance_squared(position, base.location), reverse=reverse
            )
        elif isinstance(position, Unit):
            return sorted(
                self, key=lambda unit: self._bot_object._distance_squared(position, unit.position), reverse=reverse
            )
        distances = self._bot_object._distance_units_to_pos(self, position)
        unit_dist_dict = {unit.tag: dist for unit, dist in zip(self, distances)}
        return sorted(self, key=lambda unit2: unit_dist_dict[unit2.tag], reverse=reverse)

    # //////////////////////////////////////////////////////////////////////////////////////////

    @property
    def amount(self):
        return len(self)

    def sorted_by_distance_to(self, position: Union[Base, Units, Unit, Point2], reverse: bool = False) -> Units:
        return self.subgroup(self._list_sorted_by_distance_to(position, reverse=reverse))

    def create_base(self, nexus):
        self.append(Base(nexus, self._bot_object))

    def update_bases(self):
        for base in self:
            base.update_collections()