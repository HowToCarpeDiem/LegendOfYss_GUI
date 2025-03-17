import flet as ft
import random
import time


class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
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
        self.initiative = 10


    def is_alive(self):
        return self.health > 0


class Enemy:
    def __init__(self, name, health, attack, gold_reward, exp_reward, loot, initiative):
        self.name = name
        self.health = health
        self.attack = attack
        self.gold_reward = gold_reward
        self.exp_reward = exp_reward
        self.loot = loot
        self.initiative = initiative

        
    def is_alive(self):
        return self.health > 0


class Item:
    def __init__(self, name, effect_type, effect_value, gold_value, upgrade_level):
        self.name = name
        self.effect_type = effect_type # health, max_health, attack, armor, initiative
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


goblin_loot = [Item("Drewniana pałka", 'attack', 5, 2, 0), Item('Gulasz z Goblina', 'health', 20, 5, 0)]
fairy_loot = [Item("Pył z skrzydeł Wróżki", 'max_health', 2, 6, 0)]


# Lista przedmiotów u handlarza
merchant_items = [
    Item("Miecz", 'attack', 8, 15, 0),
    Item("Skórzana zbroja", 'armor', 5, 12, 0),
    Item("Mikstura leczenia", 'health', 25, 8, 0)
]


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


def combat(player, game_text, page, menu_container, show_main_menu, show_city_menu):
    game_text.controls.clear()
    
    if player.fights_count >= 14 and player.current_location == "Mroczna puszcza":
        enemy = Enemy("Pani Puszczy", 50, 10, 30, 60, [], 12) 
        game_text.controls.append(ft.Text("Spotkałeś Bossa!"))
    else:
        enemy = get_random_enemy(player)
        game_text.controls.append(ft.Text(f"Spotkałeś {enemy.name}!"))
    
    # Porównanie inicjatywy
    if player.initiative > enemy.initiative:
        game_text.controls.append(ft.Text(f"Twoja inicjatywa ({player.initiative}) jest większa niż przeciwnika ({enemy.initiative}). Atakujesz pierwszy!"))
    else:
        game_text.controls.append(ft.Text(f"Inicjatywa przeciwnika ({enemy.initiative}) jest równa lub większa od twojej ({player.initiative}). Przeciwnik atakuje pierwszy!"))
    
    def attack_action(e):
        if player.is_alive() and enemy.is_alive():
            if player.initiative > enemy.initiative:
                player_attack(player, enemy, game_text)
                if enemy.is_alive():
                    enemy_attack(player, enemy, game_text)
            else:
                enemy_attack(player, enemy, game_text)
                if player.is_alive():
                    player_attack(player, enemy, game_text)

            check_combat_results(player, enemy, game_text, page, menu_container, show_main_menu, show_city_menu)
            
            page.update()
    \
    def escape_action(e):
        escape_chance = 0.4 + (player.initiative - enemy.initiative) * 0.05
        escape_chance = max(0.1, min(0.9, escape_chance)) 
        
        if random.random() < escape_chance:
            game_text.controls.append(ft.Text("Udało ci się uciec z walki!"))
            return_to_main_menu(game_text, page, menu_container, show_main_menu)
        else:
            game_text.controls.append(ft.Text("Nie udało ci się uciec! Przeciwnik atakuje!"))
            enemy_attack(player, enemy, game_text)
            check_combat_results(player, enemy, game_text, page, menu_container, show_main_menu, show_city_menu)
        
        page.update()

    menu_container.content = ft.Column([
        ft.ElevatedButton("Atakuj", width=120, height=40, on_click=attack_action),
        ft.ElevatedButton("Uciekaj", width=120, height=40, on_click=escape_action)
    ])
    
    page.update()

def player_attack(player, enemy, game_text):
    damage = random.randint(round(player.attack * 0.8), round(player.attack * 1.1))
    enemy.health -= damage
    game_text.controls.append(ft.Text(f"Zadałeś {damage} obrażeń!"))

def enemy_attack(player, enemy, game_text):
    damage_enemy = max(0, random.randint(round(enemy.attack * 0.8), round(enemy.attack * 1.1)) - player.armor)
    player.health -= damage_enemy 
    game_text.controls.append(ft.Text(f"{enemy.name} zadał ci {damage_enemy} obrażeń!"))

def check_combat_results(player, enemy, game_text, page, menu_container, show_main_menu, show_city_menu):
    if enemy.health <= 0:
        if enemy.name == "Pani Puszczy":
            game_text.controls.append(ft.Text("Pokonałeś Panią Puszczy!"))
            player.current_location = "Przełęcz Shoi"  
            player.fights_count = 0
        else:
            game_text.controls.append(ft.Text(f"Pokonałeś {enemy.name}!"))
            player.fights_count += 1
            
        player.experience += enemy.exp_reward
        player.gold += enemy.gold_reward
        
        if hasattr(enemy, 'loot') and enemy.loot and random.random() > 0.18:
            original_loot = random.choice(enemy.loot)
            loot = Item(original_loot.name, original_loot.effect_type, original_loot.effect_value, original_loot.gold_value, original_loot.upgrade_level)
            player.inventory.append(loot)
            game_text.controls.append(ft.Text(f"Zdobyłeś {loot.name}"))
            
        return_to_main_menu(game_text, page, menu_container, show_main_menu)
    
    elif player.health <= 0:
        game_text.controls.append(ft.Text("Zginąłeś!"))
        visit_city(game_text, page, menu_container, show_city_menu)


def equipment(game_text, page, player, menu_container, show_main_menu):
    menu_container.content = None
    page.update()
    
    game_text.controls.clear()
    game_text.controls.append(ft.Text("EKWIPUNEK", size=20, weight="bold"))

    game_text.controls.append(ft.Text("\nStatystyki:", weight="bold"))
    game_text.controls.append(ft.Text(f"Atak: {player.attack}"))
    game_text.controls.append(ft.Text(f"Pancerz: {player.armor}"))
    game_text.controls.append(ft.Text(f"Zdrowie: {player.health}/{player.max_health}"))
    game_text.controls.append(ft.Text(f"Inicjatywa: {player.initiative}"))

    game_text.controls.append(ft.Text("\nZałożone przedmioty:", weight="bold"))
    game_text.controls.append(ft.Text(f"Broń: {player.equipped_weapon.name if player.equipped_weapon else 'Brak'}"))
    game_text.controls.append(ft.Text(f"Pancerz: {player.equipped_armor.name if player.equipped_armor else 'Brak'}"))
    
    game_text.controls.append(ft.Text("\nPrzedmioty w plecaku:", weight="bold"))
    
    if not player.inventory:
        game_text.controls.append(ft.Text("Brak przedmiotów"))
    else:
        for idx, item in enumerate(player.inventory):
            is_equipped = (item is player.equipped_weapon) or (item is player.equipped_armor)
            text_color = ft.colors.GREEN if is_equipped else None
            
            button_row = ft.Row([
                ft.Text(f"{item.name} ({item.effect_type}: +{item.effect_value})", width=300, color=text_color)
            ])
            
            if item.effect_type in ["health", "max_health"]:
                button_row.controls.append(
                    ft.ElevatedButton("Użyj", 
                        on_click=lambda e, i=idx: use_item(e, i, player, game_text, page, menu_container, show_main_menu))
                )
            elif item.effect_type == "attack":
                if item is player.equipped_weapon:
                    # Jeśli przedmiot jest już założony, pokaż przycisk "Zdejmij"
                    button_row.controls.append(
                        ft.ElevatedButton("Zdejmij", 
                            on_click=lambda e, i=idx: unequip_item(e, i, player, game_text, page, menu_container, show_main_menu))
                    )
                else:
                    # Jeśli przedmiot nie jest założony, pokaż przycisk "Załóż"
                    button_row.controls.append(
                        ft.ElevatedButton("Załóż", 
                            on_click=lambda e, i=idx: equip_item(e, i, player, game_text, page, menu_container, show_main_menu))
                    )
            elif item.effect_type == "armor":
                if item is player.equipped_armor:
                    button_row.controls.append(
                        ft.ElevatedButton("Zdejmij", 
                            on_click=lambda e, i=idx: unequip_item(e, i, player, game_text, page, menu_container, show_main_menu))
                    )
                else:
                    button_row.controls.append(
                        ft.ElevatedButton("Załóż", 
                            on_click=lambda e, i=idx: equip_item(e, i, player, game_text, page, menu_container, show_main_menu))
                    )
                
            button_row.controls.append(
                ft.ElevatedButton("Wyrzuć", 
                    on_click=lambda e, i=idx: drop_item(e, i, player, game_text, page, menu_container, show_main_menu))
            )
            
            game_text.controls.append(button_row)
    
    game_text.controls.append(ft.ElevatedButton("Powrót", 
                              on_click=lambda e: back_to_game(game_text, page, menu_container, show_main_menu)))
    
    page.update()

def use_item(e, idx, player, game_text, page, menu_container, show_main_menu):
    item = player.inventory[idx]
    item.use(player, game_text, None)
    player.inventory.pop(idx)
    equipment(game_text, page, player, menu_container, show_main_menu)


def equip_item(e, idx, player, game_text, page, menu_container, show_main_menu):
    item = player.inventory[idx]
    item.equip(player, game_text)
    equipment(game_text, page, player, menu_container, show_main_menu)


def unequip_item(e, idx, player, game_text, page, menu_container, show_main_menu):
    item = player.inventory[idx]
    
    if item is player.equipped_weapon:
        player.attack -= int(item.effect_value)
        player.equipped_weapon = None
    elif item is player.equipped_armor:
        player.armor -= int(item.effect_value)
        player.equipped_armor = None
    game_text.controls.append(ft.Text(f"Zdejmujesz {item.name}."))
    
    equipment(game_text, page, player, menu_container, show_main_menu)


def drop_item(e, idx, player, game_text, page, menu_container, show_main_menu):
    item = player.inventory[idx]
    
    if item is player.equipped_weapon:
        player.attack -= int(item.effect_value)
        player.equipped_weapon = None
        game_text.controls.append(ft.Text(f"Zdejmujesz i wyrzucasz {item.name}"))
    elif item is player.equipped_armor:
        player.armor -= int(item.effect_value)
        player.equipped_armor = None
        game_text.controls.append(ft.Text(f"Zdejmujesz i wyrzucasz {item.name}"))
    else:
        game_text.controls.append(ft.Text(f"Wyrzuciłeś {item.name}"))
    
    player.inventory.pop(idx)
    equipment(game_text, page, player, menu_container, show_main_menu)


def back_to_game(game_text, page, menu_container, show_main_menu):
    game_text.controls.clear()
    game_text.controls.append(ft.Text("Wróciłeś do gry."))
    show_main_menu()
    page.update()


def return_to_main_menu(game_text, page, menu_container, show_main_menu):
    game_text.controls.append(ft.Text("Wracasz do głównego menu."))
    show_main_menu()  
    page.update()


def visit_city(game_text, page, menu_container, show_city_menu):
    game_text.controls.clear()
    game_text.controls.append(ft.Text("Jesteś w mieście"))
    show_city_menu()
    page.update()


def add_text(game_text, message, page):
    game_text.controls.append(ft.Text(message))
    page.update()


def statistics(game_text, page, player):
    game_text.controls.append(ft.Text("STATYSTYKI", size=20, weight="bold"))
    game_text.controls.append(ft.Text(f"Imię: {player.name}"))
    game_text.controls.append(ft.Text(f"Zdrowie: {player.health}/{player.max_health}"))
    game_text.controls.append(ft.Text(f"Zbroja: {player.armor}"))
    game_text.controls.append(ft.Text(f"Obrażenia: {player.attack}"))
    game_text.controls.append(ft.Text(f"Złoto: {player.gold}"))
    game_text.controls.append(ft.Text(f"Doświadczenie: {player.experience}"))
    game_text.controls.append(ft.Text(f"Inicjatywa: {player.initiative}"))

    page.update()


def merchant(game_text, page, player, menu_container, show_city_menu):
    global merchant_items
    
    menu_container.content = None
    page.update()
    
    game_text.controls.clear()
    game_text.controls.append(ft.Text("HANDLARZ", size=20, weight="bold"))
    game_text.controls.append(ft.Text(f"Twoje złoto: {player.gold}", weight="bold"))
    
    game_text.controls.append(ft.Text("\nSprzedaj przedmioty:", weight="bold"))
    
    if not player.inventory:
        game_text.controls.append(ft.Text("Nie masz przedmiotów na sprzedaż"))
    else:
        for idx, item in enumerate(player.inventory):
            is_equipped = (item is player.equipped_weapon) or (item is player.equipped_armor)
            text_color = ft.colors.GREEN if is_equipped else None
            
            sell_price = int(item.gold_value * 0.75)
            
            button_row = ft.Row([
                ft.Text(
                    f"{item.name} ({item.effect_type}: +{item.effect_value}) - {sell_price} złota", 
                    width=400, 
                    color=text_color
                )
            ])
            
            if not is_equipped:
                button_row.controls.append(
                    ft.ElevatedButton("Sprzedaj", 
                        on_click=lambda e, i=idx, p=sell_price: sell_item(e, i, p, player, game_text, page, menu_container, show_city_menu))
                )
            else:
                button_row.controls.append(
                    ft.Text("(Najpierw zdejmij przedmiot)")
                )
            
            game_text.controls.append(button_row)

    game_text.controls.append(ft.Text("\nDostępne przedmioty:", weight="bold"))
    
    if not merchant_items:
        game_text.controls.append(ft.Text("Handlarz nie ma obecnie nic na sprzedaż"))
    else:
        for item in merchant_items:
            button_row = ft.Row([
                ft.Text(f"{item.name} ({item.effect_type}: +{item.effect_value}) - {item.gold_value} złota", width=400)
            ])
            
            button_row.controls.append(
                ft.ElevatedButton("Kup", 
                    on_click=lambda e, i=item: buy_item(e, i, player, game_text, page, menu_container, show_city_menu))
            )
            
            game_text.controls.append(button_row)

    game_text.controls.append(ft.ElevatedButton("Powrót", 
                              on_click=lambda e: visit_city(game_text, page, menu_container, show_city_menu)))
    
    page.update()

def buy_item(e, item, player, game_text, page, menu_container, show_city_menu):
    global merchant_items
    
    if player.gold >= item.gold_value:
        player.gold -= item.gold_value
        
        new_item = Item(item.name, item.effect_type, item.effect_value, item.gold_value, item.upgrade_level)
        player.inventory.append(new_item)
        
        game_text.controls.append(ft.Text(f"Kupiłeś {item.name} za {item.gold_value} złota!"))
        
        if item.effect_type in ['attack', 'armor']:
            merchant_items = [i for i in merchant_items if i is not item]
    else:
        game_text.controls.append(ft.Text("Nie masz wystarczająco złota!"))
    
    merchant(game_text, page, player, menu_container, show_city_menu)


def sell_item(e, idx, price, player, game_text, page, menu_container, show_city_menu):
    item = player.inventory[idx]
    
    player.gold += price
    
    game_text.controls.append(ft.Text(f"Sprzedałeś {item.name} za {price} złota!"))
    
    player.inventory.pop(idx)
    
    merchant(game_text, page, player, menu_container, show_city_menu)


def blacksmith(game_text, page, player, menu_container, show_city_menu):
    menu_container.content = None
    page.update()
    game_text.controls.clear()
    game_text.controls.append(ft.Text("KOWAL", size=20, weight='bold'))
    game_text.controls.append(ft.Text(f"Twoje złoto: {player.gold}", weight='bold'))

    game_text.controls.append(ft.Text("\nUlepsz przedmioty:", weight='bold'))

    upgradeable_items = [(idx, item) for idx, item in enumerate(player.inventory) 
                         if item.effect_type in ['attack', 'armor'] and item.upgrade_level < 4] 
   
    if not upgradeable_items:
        game_text.controls.append(ft.Text("Nie masz przedmiotów, które można ulepszyć"))
    else:
        for idx, item in upgradeable_items:
            upgrade_cost_multiplier = {0: 0.5, 1: 1.0, 2: 2.0, 3: 4.0}
            upgrade_cost = int(item.gold_value * upgrade_cost_multiplier[item.upgrade_level])

            new_effect_value = int(item.effect_value * 1.1)

            is_equipped = (item is player.equipped_weapon) or (item is player.equipped_armor)
            text_color = ft.colors.GREEN if is_equipped else None

            item_name = f"{item.name}" if item.upgrade_level == 0 else f"{item.name} +{item.upgrade_level}"

            button_row = ft.Row([
                ft.Text(
                    f"{item_name} ({item.effect_type}: +{item.effect_value}) → +{new_effect_value} - Koszt: {upgrade_cost} złota",
                    width=400,
                    color=text_color
                )
            ])

            if player.gold >= upgrade_cost:
                button_row.controls.append(
                    ft.ElevatedButton("Ulepsz",
                        on_click=lambda e, i=idx, c=upgrade_cost: upgrade_item(e, i, c, player, game_text, page, menu_container, show_city_menu))
                )
            else:
                button_row.controls.append(
                    ft.Text("(Brak złota)")
                )

            game_text.controls.append(button_row)
    
    game_text.controls.append(ft.ElevatedButton("Powrót", 
                              on_click=lambda e: visit_city(game_text, page, menu_container, show_city_menu)))
    
    page.update()

def upgrade_item(e, idx, cost, player, game_text, page, menu_container, show_city_menu):
    item = player.inventory[idx]
    
    player.gold -= cost
    
    is_equipped_weapon = item is player.equipped_weapon
    is_equipped_armor = item is player.equipped_armor
    
    if is_equipped_weapon:
        player.attack -= item.effect_value
    elif is_equipped_armor:
        player.armor -= item.effect_value
    
    item.effect_value = int(item.effect_value * 1.1)  
    item.upgrade_level += 1
    
    if " +" in item.name:
        base_name = item.name.split(" +")[0]
        item.name = f"{base_name} +{item.upgrade_level}"
    else:
        item.name = f"{item.name} +{item.upgrade_level}"
    
    if is_equipped_weapon:
        player.equipped_weapon = item
        player.attack += item.effect_value
    elif is_equipped_armor:
        player.equipped_armor = item
        player.armor += item.effect_value
    
    game_text.controls.clear()
    game_text.controls.append(ft.Text(f"Ulepszono {item.name}!"))
  
    page.update()
    
    time.sleep(0.5)
    
    blacksmith(game_text, page, player, menu_container, show_city_menu)
    