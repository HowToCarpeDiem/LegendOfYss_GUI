import random
import flet as ft
from models.enemy import Enemy
from models.item import Item
from data.enemies_data import get_random_enemy
from game_logic.navigation import return_to_main_menu

def combat(player, game_text, page, menu_container, show_main_menu, show_city_menu):
    game_text.controls.clear()
    
    if player.fights_count >= 14 and player.current_location == "Mroczna puszcza":
        enemy = Enemy("Pani Puszczy", 50, 10, 30, 60, [], 12) 
        game_text.controls.append(ft.Text("Spotkałeś Bossa!"))
    else:
        enemy = get_random_enemy(player)
        game_text.controls.append(ft.Text(f"Spotkałeś {enemy.name}!"))
    
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
    from game_logic.navigation import return_to_main_menu, visit_city
    
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