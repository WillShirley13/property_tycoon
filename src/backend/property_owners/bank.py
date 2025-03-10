from typing import Dict, List

from ..ownables.ownable import Ownable
from ..constants import BANK_STARTING_CASH
from ..property_owners.property_holder import PropertyHolder
from ..enums.property_group import PropertyGroup

class Bank(PropertyHolder):
    def __init__(self):
        super().__init__(BANK_STARTING_CASH)
        # No additional attributes or methods beyond PropertyHolder
    
    
