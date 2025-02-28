"""
Test script to verify that all modules can be imported without circular dependencies.
"""

def test_imports():
    print("Testing imports...")
    
    # Import from property_owners
    from backend.property_owners import property_holder
    print("✓ property_holder imported")
    
    from backend.property_owners import player
    print("✓ player imported")
    
    from backend.property_owners import bank
    print("✓ bank imported")
    
    # Import from ownables
    from backend.ownables import ownable
    print("✓ ownable imported")
    
    from backend.ownables import property
    print("✓ property imported")
    
    from backend.ownables import station
    print("✓ station imported")
    
    from backend.ownables import utility
    print("✓ utility imported")
    
    # Import from non_ownables
    from backend.non_ownables import go
    print("✓ go imported")
    
    from backend.non_ownables import jail
    print("✓ jail imported")
    
    from backend.non_ownables import free_parking
    print("✓ free_parking imported")
    
    from backend.non_ownables import game_card
    print("✓ game_card imported")
    
    print("\nAll imports successful!")

if __name__ == "__main__":
    test_imports() 