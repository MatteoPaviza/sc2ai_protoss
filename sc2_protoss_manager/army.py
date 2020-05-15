from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union, Generator, TYPE_CHECKING

import sc2
from sc2.position import Point2
from sc2.bot_ai import BotAI
from sc2.units import Units
from sc2.unit import Unit
from sc2.ids.unit_typeid import UnitTypeId

from sc2_protoss_manager.exceptions.unit_management_exceptions import WorkerManagementException, UnitTypeException

class Army:

    def __init__(self, bot_object: BotAI):
        self._bot_object = bot_object
