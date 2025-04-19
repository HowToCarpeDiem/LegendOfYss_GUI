import flet as ft
from ui.character_creation import show_name_input

def show_backstory(page, create_game_interface):
    """Wyświetla wprowadzenie fabularne przed tworzeniem postaci"""
    page.controls.clear()
    
    # Tytuł
    title = ft.Text(
        "Kroniki Lazoreth",
        size=42,
        color=ft.colors.WHITE,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        italic=True
    )
    
    # Treść historii
    story_text = ft.Markdown(
        """
        Królestwo Lazoreth zostało ogarnięte plagą. 
        
        Ludzie zmieniają się w przerażające istoty zwane La'theragami - stworzenia o skórze pokrytej niebieskimi żyłami i oczach wypełnionych błękitnym światłem. Choroba rozprzestrzenia się jak pożar, pochłaniając kolejne wioski i miasteczka.
        
        Twoja wioska na obrzeżach królestwa zostaje zaatakowana. W chaosie ucieczki trafiasz wraz z innymi do Amro - największego miasta i stolicy królestwa. To ostatni bastion ludzkości przed rozprzestrzeniającą się plagą.
        
        By przetrwać w nowym otoczeniu, zaczynasz kraść. Niestety, przy jednej z drobnych kradzieży zostałeś schwytany. Trafiasz do lochu i stajesz przed Wielkim Sądem.
        
        Wyrok jest surowy: szafot lub wstąpienie do Bractwa Oczyszczonych. Po szybkiej kalkulacji decydujesz się na drugą opcję.
        
        Od tej chwili twoja przeszłość przestaje mieć znaczenie...
        """,
        
        extension_set="gitHub",
        code_theme="dracula",
        selectable=True
    )
    
    # Informacje o Oczyszczonych
    order_info = ft.Markdown(
        """
        Zakon Oczyszczonych
        
        Oczyszczeni to pradawny zakon mający na celu chronić ludzkość przed plagą. 
        
        Wokół zakonu narosło wiele tajemnic. Nie udzielają się publicznie, a ich główna kwatera - Twierdza Ghest - mieści się na odludziu, na wschód od Amro.
        
        Rytuał dołączenia częściowo zmienia genetykę, co sprawia, że Oczyszczeni mają ograniczone emocje. Dzięki temu łatwiej podejmują decyzje, które mają na uwadze dobro królestwa.
        
        Od początku wpajają rekrutom, że La'theragi już nie są ludźmi. Szkolenie ma za zadanie wyzbyć nowicjuszy z wyrzutów sumienia podczas walki z przemienionymi.
        
        Wielu mieszkańców mniejszych wiosek, którzy nie wyściubiają nosa poza swoją chatę, traktuje Oczyszczonych tylko jako legendę...
        """
    )
    
    # Informacje o twoim zadaniu
    mission_info = ft.Markdown(
        """
        Twoje zadanie
        
        Po przybyciu do twierdzy zostałeś poddany intensywnemu treningowi. Mimo jego krótkiego trwania, zaskakująco szybko przyswoiłeś nowe umiejętności. Twój Wiedzący (mentor) Ozahim dostrzegł w tobie ogromny potencjał.
        
        Po zakończeniu podstawowego szkolenia otrzymujesz swoją pierwszą misję - odnalezienie klejnotu Yss. Według starożytnych zapisków studiowanych przez Skrybów bractwa, artefakt ten ma moc powstrzymania plagi. Znajduje się w ruinach miasta Thiedam, niegdyś zwanego "Perłą" dawnego legendarnego królestwa Yss.
        
        Wyruszasz na w kierunku Mrocznej puszczy. Za nią w oddali majaczą szczyty pasma górskiego Hr'othim.
        """
    )
    
    # Przycisk kontynuacji
    continue_button = ft.ElevatedButton(
        "Wybierz swoje nowe imię...",
        width=250,
        height=50,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor="#1A2F4B",
            shape=ft.RoundedRectangleBorder(radius=8)
        ),
        on_click=lambda e: show_name_input(page, create_game_interface)
    )
    
    # Tło dla historii
    scroll_background = ft.Container(
        content=ft.Column(
            [
                title,
                ft.Divider(height=15, color="transparent"),
                ft.Container(content=story_text, padding=ft.padding.only(bottom=20)),
                ft.Container(content=order_info, padding=ft.padding.only(bottom=20)),
                ft.Container(content=mission_info, padding=ft.padding.only(bottom=20)),
                continue_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        ),
        width=800,
        border_radius=10,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#3A4A63", "#2A394F"]
        ),
        border=ft.border.all(2, "#1A2F4B"),
        padding=40,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.BLACK54,
            offset=ft.Offset(2, 2)
        ),
    )
    
    # Główny kontener
    main_container = ft.Container(
        content=scroll_background,
        width=page.window.width,
        height=page.window.height,
        padding=40,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#121E2E", "#1A2F4B", "#234B78"]
        ),
        alignment=ft.alignment.center
    )
    
    page.add(main_container)
    page.update()