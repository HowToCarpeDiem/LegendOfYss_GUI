import flet as ft
from game_logic.save_system import get_available_saves, load_game, delete_save

def show_save_and_exit_menu(player, game_text, page, menu_container, show_start_menu_function, create_game_interface, return_callback=None):
    """
    Wyświetla ekran zapisywania gry przy wyjściu
    
    Args:
        player: Obiekt gracza
        game_text: Kontener na tekst gry
        page: Obiekt strony flet
        menu_container: Kontener na menu
        show_start_menu_function: Funkcja pokazująca menu startowe
        create_game_interface: Funkcja tworząca interfejs gry
        return_callback: Funkcja powrotu do menu głównego gry
    """
    from game_logic.save_system import save_game
    import datetime
    
    # Czyszczenie ekranu
    page.controls.clear()
    
    # Tytuł dialogu
    title = ft.Text(
        "Zapisz grę przed wyjściem", 
        size=24, 
        weight="bold", 
        text_align=ft.TextAlign.CENTER
    )
    
    # Pole na nazwę zapisu
    save_name_field = ft.TextField(
        label="Nazwa zapisu (opcjonalnie)",
        hint_text=f"{player.name}_{datetime.datetime.now().strftime('%Y%m%d')}",
        width=300
    )
    
    # Funkcja obsługująca zapisywanie i wyjście
    def save_and_exit(e):
        save_name = save_name_field.value
        save_game(player, save_name)
        
        # Wyświetl komunikat o zapisaniu
        page.snack_bar = ft.SnackBar(content=ft.Text("Gra została zapisana pomyślnie!"))
        page.snack_bar.open = True
        page.update()
        
        # Wróć do menu głównego
        show_start_menu_function(page, create_game_interface)
    
    # Funkcja obsługująca wyjście bez zapisywania
    def exit_without_saving(e):
        # Wróć bezpośrednio do menu głównego
        show_start_menu_function(page, create_game_interface)
    
    # Funkcja obsługująca anulowanie i powrót do gry
    def cancel_and_return(e):
        # Przywróć układ gry
        page.controls.clear()
        
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
        
        # Wywołaj funkcję zwrotną, aby przywrócić menu
        if return_callback:
            return_callback()
        
        page.update()
    
    # Przycisk zapisz i wyjdź
    save_button = ft.ElevatedButton(
        "Zapisz i wyjdź",
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor="#4CAF50"  # Zielony
        ),
        on_click=save_and_exit
    )
    
    # Przycisk wyjdź bez zapisywania
    exit_button = ft.ElevatedButton(
        "Wyjdź bez zapisywania",
        style=ft.ButtonStyle(
            color=ft.colors.WHITE, 
            bgcolor="#F44336"  # Czerwony
        ),
        on_click=exit_without_saving
    )
    
    # Przycisk anuluj (wróć do gry)
    cancel_button = ft.OutlinedButton(
        "Anuluj", 
        on_click=cancel_and_return 
    )
    
    # Dialog zapisywania
    dialog = ft.Card(
        content=ft.Container(
            content=ft.Column([
                title,
                save_name_field,
                ft.Row([
                    save_button,
                    exit_button,
                    cancel_button
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
            padding=20,
            width=400
        ),
        elevation=10
    )
    
    # Dodanie dialogu do strony
    page.add(dialog)
    page.update()

def show_load_game_screen(page, create_game_interface):
    """Wyświetla ekran wczytywania gry"""
    from game_logic.save_system import get_available_saves, load_game, delete_save
    
    # Czyszczenie ekranu
    page.controls.clear()
    
    # Tytuł
    title = ft.Text("Wczytaj grę", size=30, weight="bold", text_align=ft.TextAlign.CENTER)
    
    # Pobierz dostępne zapisy
    saves = get_available_saves()
    
    # Kontener na listę zapisów
    saves_container = ft.Container(
        width=600,
        height=400,
        border=ft.border.all(1, ft.colors.BLUE_200),
        border_radius=10,
        padding=20
    )
    
    # Funkcja obsługująca wczytywanie zapisu
    def load_saved_game(save_path):
        player = load_game(save_path)
        if player:
            page.snack_bar = ft.SnackBar(content=ft.Text("Gra wczytana pomyślnie!"))
            page.snack_bar.open = True
            page.update()
            
            # Uruchom grę z wczytanym graczem
            create_game_interface(page, player.name, player.race, player=player)
        else:
            # Obsługa błędu wczytywania
            page.snack_bar = ft.SnackBar(content=ft.Text("Błąd wczytywania zapisu!"))
            page.snack_bar.open = True
            page.update()
    
    # Funkcja obsługująca usuwanie zapisu
    def delete_saved_game(save_path):
        if delete_save(save_path):
            # Odświeżenie ekranu wczytywania
            show_load_game_screen(page, create_game_interface)
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Nie można usunąć pliku zapisu!"))
            page.snack_bar.open = True
            page.update()
    
    if not saves:
        # Brak zapisanych gier
        saves_container.content = ft.Column([
            ft.Text("Brak zapisanych gier", size=18, text_align=ft.TextAlign.CENTER),
            ft.Text("Rozpocznij nową grę, aby utworzyć zapis.", size=14, text_align=ft.TextAlign.CENTER)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    else:
        # Lista zapisanych gier
        save_list = ft.ListView(spacing=10, padding=10)
        
        for save in saves:
            # Format wyświetlania daty
            formatted_date = save["timestamp"].strftime("%d-%m-%Y %H:%M")
            
            # Zachowaj kopię ścieżki dla każdego przycisku
            save_path = save['path']
            
            # Element listy dla każdego zapisu
            save_item = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(f"{save['player_name']}", size=18, weight="bold"),
                        ft.Text(f"Lokacja: {save['location']}", size=14)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(f"Data: {formatted_date}", size=12, color="grey"),
                    ft.Row([
                        ft.ElevatedButton(
                            "Wczytaj", 
                            on_click=lambda e, path=save_path: load_saved_game(path)
                        ),
                        ft.OutlinedButton(
                            "Usuń", 
                            on_click=lambda e, path=save_path: delete_saved_game(path)
                        )
                    ], alignment=ft.MainAxisAlignment.END)
                ]),
                padding=10,
                border=ft.border.all(1, ft.colors.GREY_400),
                border_radius=5,
                margin=5
            )
            
            save_list.controls.append(save_item)
        
        saves_container.content = save_list
    
    # Przycisk powrotu
    def go_back(e):
        from ui.start_menu import show_start_menu
        show_start_menu(page, create_game_interface)
    
    back_button = ft.ElevatedButton(
        "Powrót", 
        on_click=go_back
    )
    
    # Główny kontener
    main_container = ft.Container(
        content=ft.Column([
            title,
            ft.Divider(height=20, color="transparent"),
            saves_container,
            ft.Divider(height=20, color="transparent"),
            back_button
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        width=page.window.width,
        height=page.window.height,
        padding=40,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#1a237e", "#3949ab", "#5c6bc0"]
        )
    )
    
    # Dodanie głównego kontenera do strony
    page.add(main_container)
    page.update()