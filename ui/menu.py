import flet as ft
from game_logic.combat import combat
from game_logic.inventory import equipment, statistics
from game_logic.navigation import return_to_main_menu, visit_city
from game_logic.trading import merchant, blacksmith
from ui.save_load import show_save_and_exit_menu
from ui.start_menu import show_start_menu

def create_main_menu(player, game_text, page, menu_container, show_city_menu, create_game_interface):
    menu_container.content = ft.Column([
        ft.ElevatedButton("Eksploruj", width=120, height=40, 
                    on_click=lambda e: combat(player, game_text, page, menu_container, 
                                             lambda: create_main_menu(player, game_text, page, menu_container, show_city_menu, create_game_interface), 
                                             show_city_menu)),
        ft.ElevatedButton("Statystyki", width=120, height=40, 
                    on_click=lambda e: statistics(game_text, page, player)),
        ft.ElevatedButton("Ekwipunek", width=120, height=40, 
                    on_click=lambda e: equipment(game_text, page, player, menu_container, 
                                               lambda: create_main_menu(player, game_text, page, menu_container, show_city_menu, create_game_interface))),
        ft.ElevatedButton("Miasto", width=120, height=40, 
                    on_click=lambda e: visit_city(game_text, page, menu_container, show_city_menu)),
        ft.ElevatedButton("Zapisz i wyjdź", width=160, height=40, 
                    on_click=lambda e: show_save_and_exit_menu(
                        player, 
                        game_text, 
                        page, 
                        menu_container,
                        show_start_menu, 
                        create_game_interface,
                        lambda: create_main_menu(player, game_text, page, menu_container, show_city_menu, create_game_interface)
                    ))
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