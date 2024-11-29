from ahk_controller import AHKController
from window_manager import WindowManager
from image_processor import ImageProcessor
import time
import random
import os
import sys
import psutil

def is_ahk_running():
    """Kontroluje, jestli už AHK běží"""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'AutoHotkey64.exe':
            return True
    return False

# Spustíme AHK skript jen pokud ještě neběží
ahk_script = "fishing_keys.ahk"
if not is_ahk_running():
    if os.path.exists(ahk_script):
        os.startfile(ahk_script)
        time.sleep(2)  
    else:
        print(f"Chyba: {ahk_script} nenalezen!")
        input("Stiskněte Enter pro ukončení...")
        sys.exit(1)

class FishingBot:
    def __init__(self):
        self.running = False
        self.ahk = AHKController()
        self.window = WindowManager()
        self.image_processor = ImageProcessor(
            template_path="fish_template.png",  # Cesta k templatu
            threshold=0.39  # Citlivost
        )
        
        # Časové parametry
        self.detection_delay = 0.05
        self.reaction_delay = 0.2
        self.post_catch_delay = 3.0    # po vytažení
        self.pre_cast_delay = 2.0      # před nahozením
        self.fish_pull_delay = 2.6     # čekání po záběru
        self.max_fishing_time = 30.0  # Maximální čas jednoho nahození
        
        # Statistiky
        self.total_attempts = 0
        self.successful_catches = 0
        
    def print_stats(self):
        """Vypíše aktuální statistiky"""
        success_rate = (self.successful_catches / self.total_attempts * 100) if self.total_attempts > 0 else 0
        print(f"\nStatistiky rybaření:")
        print(f"Celkem nahození: {self.total_attempts}")



    def throw_bait(self):
        """Hodí návnadu pomocí F1"""
        print("Hází návnadu (F1)")
        return self.ahk.send_key("F1")
        
    def cast_rod(self):
        """Nahazuje/vytahuje prut pomocí F2"""
        print("Nahazuje/vytahuje prut (F2)")
        return self.ahk.send_key("F2")

    def start_fishing(self):
        """Hlavní metoda pro spuštění rybaření"""
        print("Čekám na herní okno...")
        time.sleep(2)
        
        retry_count = 0
        max_retries = 3
        
        while retry_count < max_retries:
            if self.window.find_game_window("Astrallia"):
                break
            print(f"Pokus {retry_count + 1}/{max_retries} selhal. Zkouším znovu...")
            time.sleep(2)
            retry_count += 1
            
        if not self.window.game_window:
            print("Nepodařilo se najít herní okno ani po více pokusech!")
            return
            
        self.running = True
        print("\nBot začíná rybařit...")
        
        try:
            while self.running:
                print("\nNové kolo rybaření:")
                self.total_attempts += 1
                
                if not self.throw_bait():
                    print("Nepodařilo se hodit návnadu!")
                    continue
                    
                print(f"Čekám {self.pre_cast_delay} sekund před nahozením...")
                time.sleep(self.pre_cast_delay)
                
                if not self.cast_rod():
                    print("Nepodařilo se nahodit prut!")
                    continue
                
                time.sleep(1)  # Krátká pauza pro stabilizaci obrazu
                
                fishing_start_time = time.time()
                detection_start_time = time.time()
                
                while self.running:
                    current_time = time.time()
                    
                    # Kontrola maximálního času rybaření
                    if current_time - fishing_start_time > self.max_fishing_time:
                        print("Vypršel maximální čas rybaření, vytahuji prut...")
                        self.cast_rod()
                        time.sleep(self.post_catch_delay)
                        break
                    
                    current_frame = self.window.capture_screen()
                    if current_frame is None:
                        print("Chyba při zachycení obrazovky!")
                        break
                        
                    if self.image_processor.detect_fish(current_frame):
                        print("\nDetekován záběr! Čekám na správný moment...")
                        response_time = current_time - detection_start_time
                        print(f"Čas od začátku detekce: {response_time:.2f}s")
                        
                        print(f"Čekám {self.fish_pull_delay} sekund před vytažením...")
                        time.sleep(self.fish_pull_delay)
                        
                        if self.cast_rod():
                            print(f"Prut vytažen za {time.time() - detection_start_time:.2f}s od detekce")
                            self.successful_catches += 1
                        else:
                            print("Chyba při vytahování prutu!")
                            
                        self.print_stats()  # Vypíše aktuální statistiky
                            
                        print(f"Čekám {self.post_catch_delay} sekund před dalším pokusem...")
                        time.sleep(self.post_catch_delay)
                        break
                        
                    time.sleep(self.detection_delay)
                    
        except KeyboardInterrupt:
            print("\nBot zastaven uživatelem.")
            self.print_stats()  # Vypíše finální statistiky
            self.running = False
        finally:
            self.window.cleanup()
            self.ahk.cleanup()

if __name__ == "__main__":
    try:
        print("Spouštím rybářského bota...")
        print("Pro ukončení stiskněte Ctrl+C")
        
        # Kontrola existence template souboru
        if not os.path.exists("fish_template.png"):
            print("CHYBA: Soubor fish_template.png nenalezen!")
            print("Ujistěte se, že máte template obrázek ve stejné složce jako tento skript.")
            input("Stiskněte Enter pro ukončení...")
            sys.exit(1)
            
        bot = FishingBot()
        bot.start_fishing()
    except Exception as e:
        print(f"Neočekávaná chyba: {e}")
        input("Stiskněte Enter pro ukončení...")