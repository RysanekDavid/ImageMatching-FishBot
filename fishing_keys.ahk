#Requires AutoHotkey v2.0
#SingleInstance Force

if not A_IsAdmin {
    Run '*RunAs "' A_ScriptFullPath '"'
    ExitApp
}

FileAppend "Bot spuštěn`n", "bot_log.txt"

ACTION_FILE := A_ScriptDir "\action.txt"
RESPONSE_FILE := A_ScriptDir "\response.txt"

; ...zbytek vašeho původního kódu...

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
}