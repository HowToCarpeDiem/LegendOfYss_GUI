import flet as ft
import random

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.experience = 0
        self.gold = 0
        self.current_location = "Mroczna puszcza"  
        self.fights_count = 0  

    def is_alive(self):
        return self.health > 0


class Enemy:
    def __init__(self, name, health, attack, gold_reward, exp_reward):
        self.name = name
        self.health = health
        self.attack = attack
        self.gold_reward = gold_reward
        self.exp_reward = exp_reward

    def is_alive(self):
        return self.health > 0


def get_random_enemy(player):
    if player.current_location == "Mroczna puszcza":
        enemies = [
            Enemy("Goblin", 21, 2, 4, 10),
            Enemy("Wróżka", 15, 3, 0, 15)
        ]
    elif player.current_location == "Przełęcz Shoi":
        enemies = [
            Enemy("Troll", 35, 5, 10, 50),
            Enemy("Ogr", 40, 6, 14, 50)
        ]
    return random.choice(enemies)

def combat(player, game_text, page, menu_container, show_main_menu, show_city_menu):
    if player.fights_count >= 14 and player.current_location == "Mroczna puszcza":
        enemy = Enemy("Pani Puszczy", 50, 10, 30, 60)
        game_text.controls.append(ft.Text("Spotkałeś Bossa!"))
    else:
        enemy = get_random_enemy(player)
        game_text.controls.append(ft.Text(f"Spotkałeś {enemy.name}!"))
    
    def attack_action(e):
        if player.is_alive() and enemy.is_alive():
            damage = random.randint(round(player.attack * 0.8), round(player.attack * 1.1))
            enemy.health -= damage
            game_text.controls.append(ft.Text(f"Zadałeś {damage} obrażeń!"))
            
            if enemy.health <= 0:
                if enemy.name == "Pani Puszczy":
                    game_text.controls.append(ft.Text("Pokonałeś Panią Puszczy!"))
                    player.current_location = "Przełęcz Shoi"  
                    player.fights_count = 0
                else:
                    game_text.controls.append(ft.Text(f"Pokonałeś {enemy.name}!"))
                    player.fights_count += 1  
                return_to_main_menu(game_text, page, menu_container, show_main_menu)
            else:
                damage_enemy = random.randint(round(enemy.attack * 0.8), round(enemy.attack * 1.1))
                player.health -= damage_enemy
                game_text.controls.append(ft.Text(f"{enemy.name} zadał ci {damage_enemy} obrażeń!"))
                if player.health <= 0:
                    game_text.controls.append(ft.Text("Zginąłeś!"))
                    visit_city(game_text, page, menu_container, show_city_menu)
        page.update()
    
    def escape_action(e):
        game_text.controls.append(ft.Text("Uciekasz z walki!"))
        return_to_main_menu(game_text, page, menu_container, show_main_menu)
        page.update()

    menu_container.content = ft.Column([
        ft.ElevatedButton("Atakuj", width=120, height=40, on_click=attack_action),
        ft.ElevatedButton("Uciekaj", width=120, height=40, on_click=escape_action)
    ])
    
    page.update()

def return_to_main_menu(game_text, page, menu_container, show_main_menu):
    game_text.controls.append(ft.Text("Wracasz do głównego menu."))
    show_main_menu()  
    page.update()

def visit_city(game_text, page, menu_container, show_city_menu):
    game_text.controls.append(ft.Text("Jesteś w mieście"))
    show_city_menu()
    page.update()

def add_text(game_text, message, page):
    game_text.controls.append(ft.Text(message))
    page.update()
