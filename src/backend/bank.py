from backend.property_holder import PropertyHolder

class Bank(PropertyHolder):
    def __init__(self):
        super().__init__(initial_cash=500_000)
    
    def sub_cash_balance(self, amount: int) -> None:  # Override to add comment
        # Bank should never run out of money
        super().sub_cash_balance(amount)
