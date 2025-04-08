import flet as ft

class Item:
    def __init__(self, name, effect_type, effect_value, gold_value, upgrade_level):
        self.name = name
        self.effect_type = effect_type # health, max_health, attack, armor, initiative, strength, dexterity, vitality, charisma, initiative, stamina
        self.effect_value = int(effect_value)
        self.gold_value = int(gold_value)
        self.upgrade_level = upgrade_level
    
    def use(self, player, game_text, enemy):
        if self.effect_type == 'health':
            player.health = min(player.health + self.effect_value, player.max_health)
            game_text.controls.append(ft.Text(f"Przywróciłeś {self.effect_value} zdrowia za pomocą: {self.name}"))
        elif self.effect_type == 'max_health':
            player.max_health += self.effect_value
            player.health += self.effect_value
            game_text.controls.append(ft.Text(f"Zwiększyłeś swoje maksymalne zdrowie o {self.effect_value}"))
        elif self.effect_type == 'attack':
            player.attack += self.effect_value
            game_text.controls.append(ft.Text(f"Zwiększyłeś swój podstawowy atak o {self.effect_value}"))
        elif self.effect_type == 'armor':
            player.armor += self.effect_value
            game_text.controls.append(ft.Text(f'Zwiększyłeś swoją zbroję o {self.effect_value}'))
        elif self.effect_type == 'initiative':
            player.initiative += self.effect_value
            game_text.controls.append(ft.Text(f"Zwiększyłeś inicjatywę o {self.effect_value}"))
        elif self.effect_type == 'stamina':
            player.stamina += self.effect_value
            game_text.controls.append(ft.Text(f"Przywróciłeś {self.effect_value} staminy"))
    
    def equip(self, player, game_text):
        if self.effect_type == 'attack':
            if player.equipped_weapon:
                player.attack -= player.equipped_weapon.effect_value
                game_text.controls.append(ft.Text(f"Zdejmujesz {player.equipped_weapon.name}."))
            player.equipped_weapon = self
            player.attack += self.effect_value
            game_text.controls.append(ft.Text(f"Wyposażyłeś się w {self.name}, +{self.effect_value} do ataku."))
        
        elif self.effect_type == 'armor':
            if player.equipped_armor:
                player.armor -= player.equipped_armor.effect_value
                game_text.controls.append(ft.Text(f"Zdejmujesz {player.equipped_armor.name}."))
            player.equipped_armor = self
            player.armor += self.effect_value
            game_text.controls.append(ft.Text(f"Założyłeś {self.name}, +{self.effect_value} do pancerza."))