from itertools import chain
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union, Generator, TYPE_CHECKING

import sc2
from sc2.position import Point2
from sc2.bot_ai import BotAI
from sc2.units import Units
from sc2.unit import Unit

from data.libs.proxy import Proxy

class Proxies(list):

    def __init__(self, proxies, bot_object: BotAI):
        super().__init__(proxies)
        self._bot_object = bot_object

    def __or__(self, other):
        return Proxies(
            chain(
                iter(self),
                (other_proxy for other_proxy in other if other_proxy.position not in (self_proxy.position for self_proxy in self)),
            ),
            self._bot_object,
        )

    def __add__(self, other):
        return Proxies(
            chain(
                iter(self),
                (other_proxy for other_proxy in other if other_proxy.position not in (self_proxy.position for self_proxy in self)),
            ),
            self._bot_object,
        )

    def __and__(self, other):
        return Proxies(
            (other_proxy for other_proxy in other if other_proxy.position in (self_proxy.position for self_proxy in self)),
            self._bot_object,
        )

    def __sub__(self, other):
        return Proxies(
            (self_proxy for self_proxy in self if self_proxy.position not in (other_proxy.position for other_proxy in other)),
            self._bot_object,
        )

    def __hash__(self):
        return hash(proxy.position for proxy in self)

    def copy(self):
        return self.subgroup(self)

    def subgroup(self, proxies):
        return Proxies(proxies, self._bot_object)

    def filter(self, pred: callable):
        assert callable(pred), "Function is not callable"
        return self.subgroup(filter(pred, self))

    def sorted(self, key: callable, reverse: bool = False):
        return self.subgroup(sorted(self, key=key, reverse=reverse))

    def _list_sorted_by_distance_to(self, position: Union[Proxy, Unit, Point2], reverse: bool = False) -> List[Proxy]:
        if isinstance(position, Proxy):
            return sorted(
                self, key=lambda proxy: self._bot_object._distance_squared(position, proxy.position), reverse=reverse
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

    def sorted_by_distance_to(self, position: Union[Proxy, Unit, Point2], reverse: bool = False) -> Units:
        return self.subgroup(self._list_sorted_by_distance_to(position, reverse=reverse))

    def create_proxy(self, pylon):
        self.append(Proxy(pylon, self._bot_object))

    def update_proxies(self):
        for proxy in self:
            proxy.update_collections()
