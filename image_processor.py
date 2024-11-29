import cv2
import numpy as np
import time

class ImageProcessor:
    def __init__(self, template_path=None, threshold=0.8):
        self.threshold = threshold
        self.template = None
        
        # Načtení template obrázku
        if template_path:
            self.template = cv2.imread(template_path)
            print(f"Template načten, rozměry: {self.template.shape}")
        else:
            print("Template soubor nenalezen!")

    def detect_fish(self, current_frame, save_debug=True):
        """Detekuje rybářský symbol pomocí template matching"""
        if self.template is None:
            return False
            
        try:
            if save_debug:
                # capture_area.png pro kontrolu
                cv2.imwrite('capture_area.png', current_frame)
            
            # Použití template matching
            result = cv2.matchTemplate(current_frame, self.template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            # Debug informace bez omezení rychlosti
            print(f"Match confidence: {max_val:.3f}", end='\r')
            
            return max_val > self.threshold
            
        except Exception as e:
            print(f"Chyba při detekci: {e}")
            return False

    def reset_reference(self):
        """Metoda ponechána pro kompatibilitu"""
        pass