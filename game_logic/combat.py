import random
import flet as ft
from models.enemy import Enemy
from models.item import Item
from data.enemies_data import get_random_enemy
from game_logic.navigation import return_to_main_menu

def combat(player, game_text, page, menu_container, show_main_menu, show_city_menu):
    game_text.controls.clear()
    
    # Boss1
    if player.fights_count >= 14 and player.current_location == "Mroczna puszcza":
        enemy = Enemy("Pani Puszczy", 50, 10, 30, 60, [], 12) 
        game_text.controls.append(ft.Text("Spotkałeś Bossa!", size=18, weight="bold"))
    else:
        enemy = get_random_enemy(player)
        game_text.controls.append(ft.Text(f"Spotkałeś {enemy.name}!", size=18, weight="bold"))
    
    # Podstawowy atak
    def player_attack(player, enemy, game_text):
        damage = random.randint(round(player.attack * 0.8), round(player.attack * 1.1))
        if enemy.armor > 0:
            reduced_damage = max(1, damage - enemy.armor)
            game_text.controls.append(ft.Text(f"Zadałeś {damage} obrażeń, ale pancerz przeciwnika zredukował je do {reduced_damage}!"))
            enemy.health -= reduced_damage
        else:
            enemy.health -= damage
            game_text.controls.append(ft.Text(f"Zadałeś {damage} obrażeń!"))
    

    # Atak przeciwnika
    def enemy_attack(player, enemy, game_text):
        damage = random.randint(round(enemy.attack * 0.8), round(enemy.attack * 1.1))
        if player.armor > 0:
            reduced_damage = max(1, damage - player.armor)
            game_text.controls.append(ft.Text(f"{enemy.name} zadał {damage} obrażeń, ale twój pancerz zredukował je do {reduced_damage}!"))
            player.health -= reduced_damage
        else:
            player.health -= damage
            game_text.controls.append(ft.Text(f"{enemy.name} zadał ci {damage} obrażeń!"))
    

    # Wynik walki
    def check_combat_results(player, enemy, game_text, page, menu_container, show_main_menu, show_city_menu):
        if enemy.health <= 0:
            if enemy.name == "Pani Puszczy":
                game_text.controls.append(ft.Text("Pokonałeś Panią Puszczy!", size=18, weight="bold", color=ft.colors.GREEN))
                game_text.controls.append(ft.Text("Odblokowałeś nową lokację: Przełęcz Shoi!"))
                player.current_location = "Przełęcz Shoi"
                player.unlocked_locations.append("Przełęcz Shoi")
                player.fights_count = 0
            else:
                game_text.controls.append(ft.Text(f"Pokonałeś {enemy.name}!", size=16, color=ft.colors.GREEN))
                player.fights_count += 1
            
            player.experience += enemy.exp_reward
            player.gold += enemy.gold_reward
            game_text.controls.append(ft.Text(f"Zdobyłeś {enemy.exp_reward} doświadczenia i {enemy.gold_reward} złota!"))
            
            if hasattr(enemy, 'loot') and enemy.loot and random.random() < 0.82:
                original_loot = random.choice(enemy.loot)
                loot = Item(original_loot.name, original_loot.effect_type, original_loot.effect_value, original_loot.gold_value, original_loot.upgrade_level)
                player.inventory.append(loot)
                game_text.controls.append(ft.Text(f"Zdobyłeś {loot.name}"))
            
            return_button = ft.ElevatedButton("Powrót", on_click=lambda e: return_to_main_menu(game_text, page, menu_container, show_main_menu))
            game_text.controls.append(return_button)
            
        elif player.health <= 0:
            game_text.controls.append(ft.Text("Zostałeś pokonany!", size=18, weight="bold", color=ft.colors.RED))
            
            # Przegrana walka
            player.gold = 0
            player.health = player.max_health // 2 
            player.stamina = player.max_stamina  
            
            back_button = ft.ElevatedButton("Powrót do miasta", on_click=lambda e: show_city_menu())
            game_text.controls.append(back_button)
    

    # Stamina
    def update_stamina_display():
        stamina_text = "Stamina: "
        for i in range(player.max_stamina):
            if i < player.stamina:
                stamina_text += "●"  
            else:
                stamina_text += "○" 
        stamina_text += f" ({player.stamina}/{player.max_stamina})"
        return ft.Text(stamina_text, color=ft.colors.AMBER, size=16)
    

    # Zdrowie
    def update_player_health_display():
        return ft.Text(
            f"Twoje zdrowie: {player.health}/{player.max_health}", 
            color="#006400",
            size=16
        )
    

    # Zdrowie przeciwnika
    def update_enemy_health_display():
        if enemy.health >= 0:
            return ft.Text(
                f"{enemy.name}: {enemy.health} HP", 
                color="#EF0D44",
                size=16
            )
        else:
            return ft.Text(
                f"{enemy.name}: 0 HP",
                color="#EF0D44",
                size=16
            )
    

    # Panel statusu
    stamina_display = update_stamina_display()
    player_health_display = update_player_health_display()
    enemy_health_display = update_enemy_health_display()
    
    status_panel = ft.Container(
        content=ft.Column([
            enemy_health_display,
            player_health_display,
            stamina_display
        ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.START),
        padding=10,
        border=ft.border.all(1, ft.colors.BLUE_200),
        border_radius=5,
        margin=ft.margin.only(bottom=10)
    )
    
    def update_status_panel():
        nonlocal stamina_display, player_health_display, enemy_health_display
        
        stamina_display = update_stamina_display()
        player_health_display = update_player_health_display()
        enemy_health_display = update_enemy_health_display()
        
        status_panel.content = ft.Column([
            enemy_health_display,
            player_health_display,
            stamina_display
        ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.START)
    

    # Walka
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
            
            update_status_panel()
            check_combat_results(player, enemy, game_text, page, menu_container, show_main_menu, show_city_menu)
            page.update()


    # Silny atak - 175% obrażeń
    def strong_attack_action(e):
        if player.stamina < 3:
            game_text.controls.append(ft.Text("Nie masz wystarczająco staminy!", color=ft.colors.RED))
            page.update()
            return
            
        player.stamina -= 3  
        
        if player.is_alive() and enemy.is_alive():
            damage = int(random.randint(round(player.attack * 0.8), round(player.attack * 1.1)) * 1.75)
            if enemy.armor > 0:
                reduced_damage = max(1, damage - enemy.armor)
                game_text.controls.append(ft.Text(f"Wykonujesz silny atak za {damage} obrażeń, ale pancerz przeciwnika zredukował je do {reduced_damage}!", color=ft.colors.ORANGE))
                enemy.health -= reduced_damage
            else:
                enemy.health -= damage
                game_text.controls.append(ft.Text(f"Wykonujesz potężny cios i zadajesz {damage} obrażeń!", color=ft.colors.ORANGE))
            
            if enemy.is_alive():
                enemy_attack(player, enemy, game_text)
            
            update_status_panel()
            check_combat_results(player, enemy, game_text, page, menu_container, show_main_menu, show_city_menu)
            page.update()
    

    # Ucieczka z walki
    def escape_action(e):
        escape_chance = 0.4 + (player.initiative - enemy.initiative) * 0.05
        escape_chance = max(0.1, min(0.9, escape_chance)) 
        
        if random.random() < escape_chance:
            game_text.controls.append(ft.Text("Udało ci się uciec z walki!"))
            return_to_main_menu(game_text, page, menu_container, show_main_menu)
        else:
            game_text.controls.append(ft.Text("Nie udało ci się uciec! Przeciwnik atakuje!"))
            
            enemy_attack(player, enemy, game_text)
            
            update_status_panel()
            check_combat_results(player, enemy, game_text, page, menu_container, show_main_menu, show_city_menu)
            page.update()
    

    # Przygotowanie przycisków do walki
    attack_button = ft.ElevatedButton("Zwykły atak", width=160, height=40, on_click=attack_action)
    
    # Odblokowanie specjalnych ataków 
    special_attacks_container = ft.Column(spacing=5)
    if player.fights_count >= 10:
        strong_attack_button = ft.ElevatedButton(
            "Silne uderzenie (3 ●)", 
            width=160, 
            on_click=strong_attack_action, 
            icon=ft.icons.FLASH_ON, 
            icon_color=ft.colors.ORANGE
        )
        special_attacks_container.controls.append(strong_attack_button)
    else:
        locked_attack = ft.ElevatedButton("??? (odblokuj: 10 walk)", width=160, disabled=True)
        special_attacks_container.controls.append(locked_attack)
    
    escape_button = ft.ElevatedButton("Uciekaj)", width=160, height=40, on_click=escape_action)
    
    # Grupowanie przycisków
    attacks_group = ft.Container(
        content=ft.Column(
            [
                ft.Text("ATAKI", weight="bold"),
                attack_button,
                special_attacks_container
            ],
            spacing=5
        ),
        padding=10,
        border=ft.border.all(1, ft.colors.BLUE_200),
        border_radius=5
    )
    
    other_actions_group = ft.Container(
        content=ft.Column(
            [
                ft.Text("INNE AKCJE", weight="bold"),
                escape_button
            ],
            spacing=5
        ),
        padding=10,
        border=ft.border.all(1, ft.colors.BLUE_200),
        border_radius=5
    )
    
    # Utworzenie menu walki
    menu_container.content = ft.Column([
        status_panel,  
        attacks_group,
        other_actions_group
    ], spacing=10)
    
    page.update()