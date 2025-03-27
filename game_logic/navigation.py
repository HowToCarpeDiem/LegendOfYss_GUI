import flet as ft

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