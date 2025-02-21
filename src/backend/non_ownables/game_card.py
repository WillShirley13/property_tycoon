class GameCard:
    def __init__(self):
        self.card_ids = {}  # dict<string, int>
        self.card_pack = []  # list<string>

    def getCard(self) -> tuple:
        pass

    def process_card(self, player, bank, card_id: int) -> None:
        pass

    def shuffle_pack(self) -> None:
        pass 