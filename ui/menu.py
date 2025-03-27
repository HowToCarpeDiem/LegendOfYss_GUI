import flet as ft
from game_logic.combat import combat
from game_logic.inventory import equipment, statistics
from game_logic.navigation import return_to_main_menu, visit_city
from game_logic.trading import merchant, blacksmith

def create_main_menu(player, game_text, page, menu_container, show_city_menu):
    menu_container.content = ft.Column([
        ft.ElevatedButton("Eksploruj", width=120, height=40, 
                    on_click=lambda e: combat(player, game_text, page, menu_container, 
                                             lambda: create_main_menu(player, game_text, page, menu_container, show_city_menu), 
                                             show_city_menu)),
        ft.ElevatedButton("Statystyki", width=120, height=40, 
                    on_click=lambda e: statistics(game_text, page, player)),
        ft.ElevatedButton("Ekwipunek", width=120, height=40, 
                    on_click=lambda e: equipment(game_text, page, player, menu_container, 
                                               lambda: create_main_menu(player, game_text, page, menu_container, show_city_menu))),
        ft.ElevatedButton("Miasto", width=120, height=40, 
                    on_click=lambda e: visit_city(game_text, page, menu_container, show_city_menu)),
        ft.ElevatedButton("Wyjście", width=120, height=40, 
                    on_click=lambda e: page.window.destroy())
    ], spacing=10)
    page.update()

def create_city_menu(player, game_text, page, menu_container, show_main_menu):
    menu_container.content = ft.Column([
        ft.ElevatedButton("Kowal", width=120, height=40, 
                    on_click=lambda e: blacksmith(game_text, page, player, menu_container, 
                                                lambda: create_city_menu(player, game_text, page, menu_container, show_main_menu))),
        ft.ElevatedButton("Handlarz", width=120, height=40, 
                    on_click=lambda e: merchant(game_text, page, player, menu_container, 
                                              lambda: create_city_menu(player, game_text, page, menu_container, show_main_menu))),
        ft.ElevatedButton("Statystyki", width=120, height=40, 
                    on_click=lambda e: statistics(game_text, page, player)),
        ft.ElevatedButton("Wyjście z miasta", width=120, height=40, 
                    on_click=lambda e: return_to_main_menu(game_text, page, menu_container, show_main_menu))
    ], spacing=10)
    page.update()