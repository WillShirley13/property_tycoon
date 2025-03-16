from backend.property_owners.player import Player


def in_in_jail_helper(player: Player) -> bool:
    if not player.get_is_in_jail():
        return False
