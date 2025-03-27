from models.item import Item

# Przedmioty z łupów
goblin_loot = [Item("Drewniana pałka", 'attack', 5, 2, 0), Item('Gulasz z Goblina', 'health', 20, 5, 0)]
fairy_loot = [Item("Pył z skrzydeł Wróżki", 'max_health', 2, 6, 0)]

# Lista przedmiotów u handlarza
merchant_items = [
    Item("Miecz", 'attack', 8, 15, 0),
    Item("Skórzana zbroja", 'armor', 5, 12, 0),
    Item("Mikstura leczenia", 'health', 25, 8, 0)
]