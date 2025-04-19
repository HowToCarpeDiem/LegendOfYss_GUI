import flet as ft
from ui.save_load import show_load_game_screen
from ui.story import show_backstory

def show_start_menu(page, create_game_interface):
    """Wyświetla menu startowe gry"""
    page.controls.clear()
    
    # Tytuł gry
    title = ft.Text(
        "Legend of Yss",
        size=50,
        color=ft.colors.WHITE,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )
    
    # Podtytuł/opis
    subtitle = ft.Text(
        "Epicka przygoda w fantastycznym świecie",
        size=16,
        color="#DDDDDD",
        italic=True,
        text_align=ft.TextAlign.CENTER
    )
    
    # Funkcje obsługujące przyciski
    def new_game_click(e):
        show_backstory(page, create_game_interface)
    
    def load_game_click(e):
        show_load_game_screen(page, create_game_interface)
    
    def exit_game_click(e):
        page.window.destroy()
    
    # Przyciski menu
    new_game_button = ft.ElevatedButton(
        "Nowa Gra", 
        width=200, 
        height=45,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor="#4CAF50",  # Zielony
            shape=ft.RoundedRectangleBorder(radius=8)
        ),
        on_click=new_game_click
    )
    
    load_game_button = ft.ElevatedButton(
        "Wczytaj Grę", 
        width=200, 
        height=45,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor="#2196F3",  # Niebieski
            shape=ft.RoundedRectangleBorder(radius=8)
        ),
        on_click=load_game_click
    )
    
    exit_button = ft.ElevatedButton(
        "Wyjście", 
        width=200, 
        height=45,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor="#F44336",  # Czerwony
            shape=ft.RoundedRectangleBorder(radius=8)
        ),
        on_click=exit_game_click
    )
    
    # Kontener dla przycisków menu
    menu_container = ft.Container(
        content=ft.Column(
            [
                new_game_button,
                ft.Divider(height=10, color="transparent"),
                load_game_button,
                ft.Divider(height=10, color="transparent"),
                exit_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        margin=ft.margin.only(top=50)
    )
    
    # Tło menu
    background = ft.Container(
        content=ft.Column(
            [
                title,
                subtitle,
                ft.Divider(height=40, color="transparent"),
                menu_container
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=page.window.width,
        height=page.window.height,
        padding=40,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#1a237e", "#3949ab", "#5c6bc0"]
        )
    )
    
    # Dodanie tła do strony
    page.add(background)
    page.update()