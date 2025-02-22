import flet as ft
from game_logic import Player,  combat, visit_city, return_to_main_menu, add_text, equipment

def main(page: ft.Page):
    page.title = "LegendOfYss"
    page.bgcolor = ft.colors.LIGHT_BLUE_700

    # Rozmiar okna
    page.window.width = 1100
    page.window.height = 800
    page.window.resizable = True
    page.window.center()

    player = Player('Kamil')

    game_text = ft.Column(scroll=True, expand=True, auto_scroll=True)

    # Kontener na dynamiczne menu
    menu_container = ft.Container()

    # Główne menu
    def show_main_menu():
        menu_container.content = ft.Column([
            ft.ElevatedButton("Eksploruj", width=120, height=40, on_click=lambda e: combat(player, game_text, page, menu_container, show_main_menu, show_city_menu)),
            ft.ElevatedButton("Statystyki", width=120, height=40, on_click=lambda e: add_text(game_text, "Statystyki", page)),
            ft.ElevatedButton("Ekwipunek", width=120, height=40, on_click=lambda e: equipment(game_text, page, player)),
            ft.ElevatedButton("Miasto", width=120, height=40, on_click=lambda e: visit_city(game_text, page, menu_container, show_city_menu)),
            ft.ElevatedButton("Wyjście", width=120, height=40, on_click=lambda e: page.window.destroy())
        ], spacing=10)
        page.update()

    # Menu w mieście
    def show_city_menu():
        menu_container.content = ft.Column([
            ft.ElevatedButton("Kowal", width=120, height=40, on_click=lambda e: add_text(game_text, "U kowala!", page)),
            ft.ElevatedButton("Kupiec", width=120, height=40, on_click=lambda e: add_text(game_text, "U kupca!", page)),
            ft.ElevatedButton("Wyjście z miasta", width=120, height=40, 
                              on_click=lambda e: return_to_main_menu(game_text, page, menu_container, show_main_menu))
        ], spacing=10)
        page.update()

    # Inicjalizacja głównego menu
    show_main_menu()

    game_text_box = ft.Container(
        content=game_text,
        width=500,
        height=500,
        border=ft.border.all(1, 'black'),
        padding=10,
        alignment=ft.alignment.center
    )

    image_box = ft.Container(
        content=ft.Text("Obrazek przeciwnika"),
        width=300,
        height=400,
        border=ft.border.all(1, "black"),
        alignment=ft.alignment.center
    )

    layout = ft.Row(
        [menu_container, game_text_box, image_box],
        spacing=40,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True
    )

    page.add(layout)

ft.app(target=main)
