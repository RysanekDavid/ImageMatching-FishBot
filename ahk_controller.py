import os
import time

class AHKController:
    def __init__(self):
        self.action_file = "action.txt"
        self.response_file = "response.txt"
        
    def create_ahk_script(self):
        """Vytvoří AHK skript pro ovládání kláves"""
        ahk_content = """#Requires AutoHotkey v2.0
#SingleInstance Force

FileAppend "Bot spuštěn`n", "bot_log.txt"

ACTION_FILE := A_ScriptDir "\\action.txt"
RESPONSE_FILE := A_ScriptDir "\\response.txt"

LogMessage(msg) {
    FileAppend msg "`n", "bot_log.txt"
}

if FileExist(ACTION_FILE)
    FileDelete ACTION_FILE
if FileExist(RESPONSE_FILE)
    FileDelete RESPONSE_FILE

LogMessage("Bot čeká na příkazy...")

Loop {
    if FileExist(ACTION_FILE) {
        Try {
            action := FileRead(ACTION_FILE)
            FileDelete ACTION_FILE
            
            LogMessage("Přijat příkaz: " action)
            
            Switch action {
                Case "F1":
                    LogMessage("Odesílám F1")
                    Send "{F1 down}"
                    Sleep 50
                    Send "{F1 up}"
                    FileAppend "done", RESPONSE_FILE
                    LogMessage("F1 odesláno")
                
                Case "F2":
                    LogMessage("Odesílám F2")
                    Send "{F2 down}"
                    Sleep 50
                    Send "{F2 up}"
                    FileAppend "done", RESPONSE_FILE
                    LogMessage("F2 odesláno")
            }
        } 
        Catch as err {
            LogMessage("Chyba: " err.Message)
        }
    }
    Sleep 50
}

F12::{
    LogMessage("Ukončení skriptu")
    ExitApp
}"""
        
        with open("fishing_keys.ahk", "w", encoding='utf-8') as f:
            f.write(ahk_content)
            
        print("AHK skript vytvořen. Spusťte ho prosím ručně a pak stiskněte Enter...")
        input()

    def send_key(self, key):
        """Odešle stisk klávesy přes AHK"""
        try:
            if os.path.exists(self.response_file):
                os.remove(self.response_file)
            
            with open(self.action_file, 'w') as f:
                f.write(key)
            
            start_time = time.time()
            while not os.path.exists(self.response_file):
                if time.time() - start_time > 2:
                    print(f"Timeout při čekání na klávesu {key}")
                    return False
                time.sleep(0.1)
            
            os.remove(self.response_file)
            return True
            
        except Exception as e:
            print(f"Chyba při odesílání klávesy {key}: {e}")
            return False

    def cleanup(self):
        """Vyčistí komunikační soubory"""
        try:
            for file in [self.action_file, self.response_file]:
                if os.path.exists(file):
                    os.remove(file)
        except Exception as e:
            print(f"Chyba při čištění: {e}")