import flet as ft
from ui.start_menu import show_start_menu
from ui.game_screen import create_game_interface

def main(page: ft.Page):
    page.title = "LegendOfYss"
    page.bgcolor = "#6CA8E6"

    page.padding = 15
    # Rozmiar okna
    page.window.width = 1200
    page.window.height = 800
    page.window.resizable = True
    page.window.center()
    
    # Rozpoczęcie gry od ekranu tworzenia postaci
    show_start_menu(page, create_game_interface)

ft.app(target=main)