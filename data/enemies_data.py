import random
from models.enemy import Enemy
from data.items_data import goblin_loot, fairy_loot

def get_random_enemy(player):
    if player.current_location == "Mroczna puszcza":
        enemies = [
            Enemy("Goblin", 21, 2, 4, 10, goblin_loot, 9),
            Enemy("Wróżka", 15, 3, 0, 15, fairy_loot, 7),
        ]
    elif player.current_location == "Przełęcz Shoi":
        enemies = [
            Enemy("Troll", 35, 5, 10, 50, [], 9),
            Enemy("Ogr", 40, 6, 14, 50, [], 10)
        ]
    return random.choice(enemies)