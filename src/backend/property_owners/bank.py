from backend.property_owners.property_holder import PropertyHolder

class Bank(PropertyHolder):
    def __init__(self):
        super().__init__(initial_cash=500_000)
    
