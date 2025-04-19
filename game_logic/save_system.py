import pickle
import os
import datetime

def save_game(player, save_name=None):
    """Zapisuje stan gry do pliku"""
    # Utworzenie katalogu na zapisy
    save_dir = 'saves'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)    
    
    # Automatyczna nazwa pliku
    if save_name is None or save_name.strip() == "":
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_name = f"{player.name}_{timestamp}.sav"
    elif not save_name.endswith('.sav'):
        save_name += '.sav'

    # Pełna ścieżka do pliku zapisu
    save_path = os.path.join(save_dir, save_name)

    # Tworzenie słownika z danymi zapisu
    save_data = {
        "player": player,
        "timestamp": datetime.datetime.now(),
        "location": player.current_location,
    }

    # Zapisanie danych do pliku
    with open(save_path, 'wb') as save_file:
        pickle.dump(save_data, save_file)

    return save_path

def load_game(save_path):
    """Wczytuje stan gry z pliku"""
    if os.path.exists(save_path):
        try:
            with open(save_path, 'rb') as save_file:
                save_data = pickle.load(save_file)
                return save_data["player"]
        except Exception as e:
            print(f"Błąd wczytywania zapisu: {e}")
            return None
    return None

def get_available_saves():
    """Zwraca listę dostępnych zapisów gry"""
    save_dir = 'saves'
    saves = []

    if os.path.exists(save_dir):
        for filename in os.listdir(save_dir):
            if filename.endswith(".sav"):
                save_path = os.path.join(save_dir, filename)

                try:
                    with open(save_path, 'rb') as save_file:
                        save_data = pickle.load(save_file)

                        player = save_data.get("player", None)
                        if player is None:
                            continue
                            
                        saves.append({
                            "filename": filename,
                            "path": save_path,
                            "player_name": player.name,
                            "level": player.level if hasattr(player, "level") else 1,
                            "location": save_data.get("location", "Nieznana"),
                            "timestamp": save_data.get("timestamp", datetime.datetime.now())
                        })
                except Exception as e:
                    print(f"Błąd wczytywania zapisu {filename}: {e}")
                    continue

    # Sortowanie
    saves.sort(key=lambda x: x["timestamp"], reverse=True)
    return saves

def delete_save(save_path):
    """Usuwa plik zapisu gry"""
    if os.path.exists(save_path):
        try:
            os.remove(save_path)
            return True
        except Exception as e:
            print(f"Błąd usuwania zapisu: {e}")
            return False
    return False