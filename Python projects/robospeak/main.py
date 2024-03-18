import win32com.client as wincom

speak =wincom.Dispatch("SAPI.SPVOICE")
print("Welcome to Text to Speech")
print("V 1.1")
while True:
    cli =input("Enter the words you want to speak: ")
    speak.Speak(cli)
    if cli == "quit":
       speak.Speak("Goodbye Noob!!")
       break
