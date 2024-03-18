import win32com.client as wincom

speak = wincom.Dispatch("SAPI.SpVoice")
text="hey noob now your getting started lets go"
speak.Speak(text)