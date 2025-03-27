import flet as ft

def show_name_input(page, create_game_interface):
    #Stałe dla statystyk
    BASE_ATTRIBUTE = 8
    AVAILABLE_POINTS = 5

    # Ile atrybutów przydzielono
    attribute_points = {
        "strength": 0,
        "dexterity": 0,
        "vitality": 0,
        "charisma": 0,
        "initiative":0
    }

    # Pozostałe punkty do rozdzielenia
    remaining_points = AVAILABLE_POINTS

    # Pozostałe punkty
    points_label = ft.Text(f"Pozostałe punkty: {remaining_points}",
                           size=16,
                           weight="bold",
                           color=ft.colors.WHITE,
                           text_align=ft.TextAlign.CENTER)
    
    def increase_attribute(attribute_name, label):
        nonlocal remaining_points
        if remaining_points > 0 and attribute_points[attribute_name] < 5:
            attribute_points[attribute_name] += 1
            remaining_points -= 1
            label.value =f"{BASE_ATTRIBUTE + attribute_points[attribute_name]}"
            points_label.value = f"Pozostałe punkty: {remaining_points}"
            page.update()
    

    def decrease_attribute(attribute_name, label):
        nonlocal remaining_points
        if attribute_points[attribute_name] > 0:
            attribute_points[attribute_name] -= 1
            remaining_points += 1
            label.value = f"{BASE_ATTRIBUTE + attribute_points[attribute_name]}"
            points_label.value = f"Pozostałe punkty: {remaining_points}"
            page.update()
    

    def create_attribute_row(name, display_name):
        value_label = ft.Text(f"{BASE_ATTRIBUTE}", size=16, width=30)

        return ft.Row(
            [
                ft.Text(f"{display_name}:", size=16, width=100),
                ft.IconButton(
                    icon=ft.icons.REMOVE,
                    on_click=lambda e: decrease_attribute(name, value_label)
                ),
                value_label,
                ft.IconButton(
                    icon=ft.icons.ADD,
                    on_click=lambda e: increase_attribute(name, value_label)
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    
    strength_row = create_attribute_row("strength", "Siła")
    dexterity_row = create_attribute_row("dexterity", "Zręczność")
    vitality_row = create_attribute_row("vitality", "Witalność")
    charisma_row = create_attribute_row("charisma", "Charyzma")
    initiative_row = create_attribute_row("initiative", "Inicjatywa")

    attributes_container = ft.Container(
        content=ft.Column([
            points_label,
            strength_row,
            dexterity_row,
            vitality_row,
            charisma_row,
            initiative_row
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=10,
        border=ft.border.all(1, ft.colors.WHITE24),
        border_radius=10,
        margin=ft.margin.only(top=10, bottom=10)
    )


    name_input = ft.TextField(
        label="Wprowadź imię postaci:",
        width=300,
        text_align=ft.TextAlign.CENTER,
        autofocus=True
    )
    
    race_dropdown = ft.Dropdown(
        label="Wybierz rasę postaci:",
        width=300,
        options=[
            ft.dropdown.Option("Człowiek", "Człowiek"),
            ft.dropdown.Option("Krasnolud","Krasnolud"),
            ft.dropdown.Option("Elf", "Elf")
        ],
        value = "Człowiek"
    )

    race_description = ft.Text("Człowiek: +1 do charyzmy i witalności",
                               size = 14,
                               color = ft.colors.WHITE70,
                               text_align=ft.TextAlign.CENTER)
    
    def update_race_description(e):
        if race_dropdown.value == "Człowiek":
            race_description.value = "Człowiek: +1 do charyzmy, +1 do witalności"
        elif race_dropdown.value == "Krasnolud":
            race_description.value = "Krasnolud: +1 do siły, +1 do witalności"
        elif race_dropdown.value == "Elf":
            race_description.value = "Elf: +1 do zręczności, +1 do inicjatywy"
        page.update() 

    race_dropdown.on_change = update_race_description

    def start_game(e):
        if not name_input.value or not name_input.value.strip():
            name_input.error_text = "Imię nie może być puste"
            page.update()
            return
        
        # Przekazanie imienia, rasy i wartości atrybutów
        create_game_interface(
            page=page,
            player_name=name_input.value.strip(),
            player_race=race_dropdown.value,
            attributes={
                "strength": BASE_ATTRIBUTE + attribute_points["strength"],
                "dexterity": BASE_ATTRIBUTE + attribute_points["dexterity"],
                "vitality": BASE_ATTRIBUTE + attribute_points["vitality"],
                "charisma": BASE_ATTRIBUTE + attribute_points["charisma"],
                "initiative": BASE_ATTRIBUTE + attribute_points["initiative"]
            }
        )
    
    start_button = ft.ElevatedButton("Rozpocznij grę",
                                     width=200,
                                     height=50,
                                     on_click=start_game)
    
    welcome_text = ft.Text("Witaj w grze LegendOfYss!", size=30, weight="bold",
                           color=ft.colors.WHITE,
                           text_align=ft.TextAlign.CENTER)
    
    input_column = ft.Column(
        [welcome_text, name_input, race_dropdown, race_description, attributes_container, start_button],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    page.controls.clear()
    page.add(
        ft.Container(
            content=input_column,
            alignment=ft.alignment.center,
            expand=True
        )
    )