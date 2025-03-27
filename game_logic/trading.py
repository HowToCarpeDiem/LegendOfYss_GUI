import flet as ft
import time
from data.items_data import merchant_items
from models.item import Item
from game_logic.navigation import visit_city

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
    
    item.effect_value = int(item.effect_value * 1.6)  
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