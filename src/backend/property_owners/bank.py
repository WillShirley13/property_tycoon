from typing import Dict, List

from ..constants import BANK_STARTING_CASH
from ..enums.property_group import PropertyGroup
from ..ownables.ownable import Ownable
from ..property_owners.property_holder import PropertyHolder


class Bank(PropertyHolder):
    def __init__(self):
        super().__init__(BANK_STARTING_CASH)
        # No additional attributes or methods beyond PropertyHolder
