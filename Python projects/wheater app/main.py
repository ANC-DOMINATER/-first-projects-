import requests
import json
import win32com.client as wincom

x = input("Enter the city :")
url =f"http://api.weatherapi.com/v1/current.json?key=d4d5f666827a4ceeac4145841240103&q={x}&aqi=no"
r = requests.get(url)
m = json.loads(r.text)
print("Celsius is :",m["current"]["temp_c"])
print("Ferenhite is :",m["current"]["temp_f"])
print("The region is :",m["location"]["region"])
print("The humidity level is :",m["current"]["humidity"])
print("Country is :",m['location']['country'])
print("The Weather Condition is :",m["current"]["condition"]["text"])
print("The last updated Time is :",m["current"]["last_updated"])

# text to speech by using win32com module
speak = wincom.Dispatch("SAPI.SpVoice")
tell =[
f"the temperature of {x} is {m['current']['temp_c']} degree celsius",
f"and {m['current']['temp_f']} degree ferenhite",
f'the region of the current city is {m["location"]["region"]}',
f'the current humidity level of the city is{m["current"]["humidity"]}',
f'the country of the given city is {m["location"]["country"]}',
f'the weather condition in the city is {m["current"]["condition"]["text"]}'
]

for i in tell:
    speak.Speak(i)
