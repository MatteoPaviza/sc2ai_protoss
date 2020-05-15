from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union, Generator, TYPE_CHECKING

import sc2
from sc2.position import Point2
from sc2.bot_ai import BotAI
from sc2.units import Units
from sc2.unit import Unit
from sc2.ids.unit_typeid import UnitTypeId

from sc2_protoss_manager.exceptions.unit_management_exceptions import WorkerManagementException

class Proxy:

    def __init__(self, pylon: Unit, bot_object: BotAI):
        self._bot_object: BotAI = bot_object
        self.position: Point2 = pylon.position
        self.pylons: Units = Units([pylon], bot_object)
        self.pylon_tag = pylon.tag
        self.workers: Units = Units([], bot_object)
        self.structures: Units = Units([], bot_object)
        # self.orders = []

    @property
    def is_complete(self) -> bool:
        return not self.pylons.ready.empty
