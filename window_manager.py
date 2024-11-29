import win32gui
import win32con
from PIL import ImageGrab
import cv2
import numpy as np
import time
import traceback

class WindowManager:
    def __init__(self):
        self.game_window = None
        self.window_rect = None

    def find_game_window(self, window_title):
        """Najde herní okno"""
        try:
            def callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if "Astrallia" in title and "Chrome" not in title:
                        print(f"Nalezeno herní okno: {title}")
                        windows.append(hwnd)
                return True

            windows = []
            win32gui.EnumWindows(callback, windows)
  
            if not windows:
                print(f"Nenalezeno herní okno")
                return False

            self.game_window = windows[0]
            self.window_rect = win32gui.GetWindowRect(self.game_window)
            left, top, right, bottom = self.window_rect
            
            print(f"\nInformace o okně:")
            print(f"Handle: {self.game_window}")
            print(f"Název: {win32gui.GetWindowText(self.game_window)}")
            print(f"Pozice: Vlevo={left}, Nahoře={top}, Šířka={right-left}, Výška={bottom-top}")
            
            return True
                
        except Exception as e:
            print(f"Chyba při hledání okna: {e}")
            print(f"Stack trace: {traceback.format_exc()}")
            return False

    def capture_screen(self, monitor_scale=0.2):
        """Zachytí oblast herního okna"""
        if not self.window_rect:
            return None
            
        try:
            if not win32gui.IsWindow(self.game_window):
                print("Okno již neexistuje!")
                return None

            self.window_rect = win32gui.GetWindowRect(self.game_window)
            left, top, right, bottom = self.window_rect
            window_width = right - left
            window_height = bottom - top
            
            # Šířka stejná jako předtím
            monitor_width = int(window_width * monitor_scale)
            # Výška o 30% větší
            monitor_height = int(window_height * monitor_scale * 1.3)
            
            monitor_left = left + (window_width - monitor_width) // 2
            monitor_top = top + int(window_height * 0.2)  # Začátek stále na 20%
            
            screenshot = ImageGrab.grab(bbox=(
                monitor_left,
                monitor_top,
                monitor_left + monitor_width,
                monitor_top + monitor_height
            ))

            # Uložení debug screenshotu oblasti
            debug_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            cv2.imwrite('capture_area.png', debug_img)
            
            return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
        except Exception as e:
            print(f"Chyba při zachycení obrazovky: {e}")
            return None

    def cleanup(self):
        """Cleanup"""
        pass