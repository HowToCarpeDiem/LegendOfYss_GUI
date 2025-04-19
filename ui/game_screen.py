import flet as ft
from models.player import Player
from ui.menu import create_main_menu, create_city_menu

def create_game_interface(page, player_name, player_race, attributes=None, player=None):
    page.controls.clear()

    # Jeśli przekazano gotowego gracza, użyj go zamiast tworzyć nowego
    if player is None:
        # Tworzenie nowego gracza dla nowej gry
        if attributes is None:
            attributes = {
                "strength": 0,
                "dexterity": 0,
                "vitality": 0,
                "charisma": 0,
                "initiative": 0
            }
        player = Player(player_name, player_race, attributes)
    
    # Główny interfejs gry
    game_text = ft.Column(scroll=True, expand=True, auto_scroll=True)
    menu_container = ft.Container()

    # Dodanie powitania
    game_text.controls.append(ft.Text(f"Witaj {player.name} w świecie Yss!", size=18))
    
    if player is None:
        # Wiadomość dla nowej gry
        game_text.controls.append(ft.Text(f"Jako {player.race} rozpoczynasz swoją przygodę...", size=16))
    else:
        # Wiadomość dla wczytanej gry
        game_text.controls.append(ft.Text(f"Twoja przygoda trwa dalej...", size=16))

    # Główne menu
    def show_main_menu():
        create_main_menu(player, game_text, page, menu_container, show_city_menu, create_game_interface)

    # Menu w mieście
    def show_city_menu():
        create_city_menu(player, game_text, page, menu_container, show_main_menu)

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
    page.update()