class Player:
    def __init__(self, name, race, attributes=None):
        self.name = name
        self.health = 80
        self.max_health = 80
        self.armor = 0
        self.attack = 10 
        self.experience = 0
        self.gold = 0
        self.current_location = "Mroczna puszcza"  
        self.unlocked_locations = ["Mroczna puszcza"]
        self.fights_count = 0  
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None

        if attributes is None:
            self.strength = 8
            self.dexterity = 8
            self.vitality = 8
            self.charisma = 8
            self.initiative = 8
        else:
            self.strength = attributes["strength"]
            self.dexterity = attributes["dexterity"]
            self.vitality = attributes["vitality"]
            self.charisma = attributes["charisma"]
            self.initiative = attributes["initiative"]

        self.race = race
        self.apply_racial_bonuses()

        self.update_derived_stats()

    def apply_racial_bonuses(self):
        if self.race == "Człowiek":
            self.charisma += 1
            self.vitality += 1
        elif self.race == "Krasnolud":
            self.strength += 1
            self.vitality += 1
        elif self.race == "Elf":
            self.dexterity += 1
            self.initiative += 1

    def update_derived_stats(self):
        base_health = 80
        if self.vitality > 8:
            health_bonus = (self.vitality - 8) * 10
            self.max_health = base_health + health_bonus
            self.health = self.max_health

    def is_alive(self):
        return self.health > 0