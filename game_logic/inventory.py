import flet as ft

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
            
            if item.effect_type in ["health", "max_health", 'stamina']:
                button_row.controls.append(
                    ft.ElevatedButton("Użyj", 
                        on_click=lambda e, i=idx: use_item(e, i, player, game_text, page, menu_container, show_main_menu))
                )
            elif item.effect_type == "attack":
                if item is player.equipped_weapon:
                    button_row.controls.append(
                        ft.ElevatedButton("Zdejmij", 
                            on_click=lambda e, i=idx: unequip_item(e, i, player, game_text, page, menu_container, show_main_menu))
                    )
                else:
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


def statistics(game_text, page, player):
    game_text.controls.append(ft.Text("STATYSTYKI", size=20, weight="bold"))
    game_text.controls.append(ft.Text(f"Imię: {player.name}"))
    game_text.controls.append(ft.Text(f"Zdrowie: {player.health}/{player.max_health}"))
    game_text.controls.append(ft.Text(f"Zbroja: {player.armor}"))
    game_text.controls.append(ft.Text(f"Obrażenia: {player.attack}"))
    game_text.controls.append(ft.Text(f"Złoto: {player.gold}"))
    game_text.controls.append(ft.Text(f"Doświadczenie: {player.experience}"))
    game_text.controls.append(ft.Text(f"Siła: {player.strength}"))
    game_text.controls.append(ft.Text(f"Zręczność: {player.dexterity}"))
    game_text.controls.append(ft.Text(f"Witalność: {player.vitality}"))
    game_text.controls.append(ft.Text(f"Charyzma: {player.charisma}"))
    game_text.controls.append(ft.Text(f"Inicjatywa: {player.initiative}"))
    page.update()