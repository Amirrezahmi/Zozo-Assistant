'''
Hello everyone.  paste your openai API key in 'OPENAI_API_KEY' variable and your openweathermap API in 'apiKey' local variable in the 'weather' function. If you don't have an API key, signup. However if you don't want to use openai API at all, the program uses the pipeline model which has trained before.
Hope you like it ;)
plus if you don't have microphone or had problem in this part, write "n" or "no" at the beginning!.
'''
import requests
from country_codes import country_codes
import pyaudio
import joblib
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.pipeline import Pipeline
import os
import pygame
import pyttsx3
import datetime
from IPython.display import Audio, display
import time
from word2number import w2n
import threading
import speech_recognition as sr
import json
import os
import openai
import random
#openai api
OPENAI_API_KEY = ''    #Paste your API Key here
messages=[
        {"role": "system", "content": "You are a helpful assistant."},
    ]
#check for API
def check_API():
    if len(OPENAI_API_KEY)!=0:
        openai.api_key =  OPENAI_API_KEY
    else:
        return "No"
def api_not_worked():
    pipeline = joblib.load('model2.joblib') #Pase your path 
    print("API didn't work! Now we are using our pipline model...")
    result = pipeline.predict([a])[0]
    print(result)
    speak(result)

#weather
def weather(location, country):
  # Returns full JSON object
  apiKey = '' # Enter your API Key here for weather
  base = 'http://api.openweathermap.org/data/2.5/weather?q='
  url = base + location + ',' + country + '&units=metric&appid=' + apiKey
  response = requests.get(url).json()
  return response

# dictionary to translate descriptions
status = {
  "clouds": "cloudy",
  "drizzle": "drizzly",
  "rain": "rainy",
  "thunderstorm": "stormy",
  "snow": "snowy",
  "mist": "misty"
}
def description(location, country):
  # returns weather description
  main = weather(location, country)['weather']
  d = main[0]['main'].lower()
  return status.get(d, d)

def temperature(location, country):
  # returns current temp 
  main = weather(location, country)['main']
  return main['temp']

def get_weather_advice(description):
    cloudy_advice = ["No sunglasses needed", "Light jacket recommended", "Stay indoors if possible"]
    rainy_advice = ["Get an umbrella", "Wear waterproof shoes", "Carry a raincoat"]
    snowy_advice = ["Mittens and earmuffs", "Wear warm boots", "Drive carefully on slippery roads"]
    default_advice = ["No particular advice", "Enjoy the weather!", "Stay hydrated"]

    if description == "cloudy":
        return random.choice(cloudy_advice)
    elif description == "rainy":
        return random.choice(rainy_advice)
    elif description == "snowy":
        return random.choice(snowy_advice)
    else:
        return random.choice(default_advice)
# A Global variable for your name
name = "Amirreza"
def speak(text):
    engine.say(text)
    engine.runAndWait()

def alarm():
    # speak("Time's up!")
    pygame.mixer.init()
    pygame.mixer.music.load('Ring.wav')
    pygame.mixer.music.play()
zero=0
def one_time():
    global zero
    if zero<1:
            p = "Ok. Now write whatever you want."
            print(p)
            speak(p)
    zero+=1


def listen():
    if mic.lower()=="1" or mic.lower() =="y" or mic.lower()=="yes":
        r = sr.Recognizer()
        while True:
            with sr.Microphone() as source:
                li = ["Say something!", "OK?", "Now what?", "Speak up, I'm listening"]
                p=random.choice(li)
                speak(p)
                print(p)
                audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                p1 = "Sorry, I couldn't understand you. Please try again."
                print(p1)
    else:
        one_time()
        text = input("Enter: ")
        return text

def cleaner(x):
    return [a for a in (''.join([a for a in x if a not in string.punctuation])).lower().split()]

engine = pyttsx3.init()
engine.setProperty('rate', 150)
w = "Welcome to Zozo Assistant. First thing first, do you have a microphone?"
speak(w)
print(w+" (y/n)")
mic = input()
if mic.lower()=="1" or mic.lower() =="y" or mic.lower()=="yes":
    w="Say Zozo to get my attention!"
    print(w)
    speak(w)
    r = sr.Recognizer()
    
else:
    pass
while True:
    if mic.lower()=="1" or mic.lower() =="y" or mic.lower()=="yes":
        with sr.Microphone() as source:
            audioo= r.listen(source)
            try:
                txt=r.recognize_google(audioo)
                if 'zozo' in txt.lower() or "hi zozo" in txt.lower():
                    pass
                else:
                    continue
            except sr.UnknownValueError:
                continue
    
                    
    while True:
        a = listen()
        if "who am I" in a or "what is my name" in a:
            p = f"You are {name}."
            speak(p)
        elif "play music" in a:
            folder_path = 'music' #change based on ur path
            music_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.mp3')]

            pygame.mixer.init()
            current_music_index = 0
            pygame.mixer.music.load(music_files[current_music_index])
            pygame.mixer.music.play()

            print('Playing:', music_files[current_music_index])

            while True:
                print('Enter:\n1. next\n2. previous\n3. pause\n4. unpause\n5. break\n')
                b = listen() #If you had problem in this part, you can simply use 'b=input("Enter your choice")' instead of 'b=listen()'.
                if b == 'next' or b == '1' or b == 'one':
                    current_music_index = (current_music_index + 1) % len(music_files)
                    pygame.mixer.music.load(music_files[current_music_index])
                    pygame.mixer.music.play()
                    print('Playing:', music_files[current_music_index])

                elif b == 'previous' or b == '2' or b == 'two':
                    current_music_index = (current_music_index - 1) % len(music_files)
                    pygame.mixer.music.load(music_files[current_music_index])
                    pygame.mixer.music.play()
                    print('Playing:', music_files[current_music_index])

                elif b == 'unpause' or b == '4' or b == 'four':
                    pygame.mixer.music.unpause()

                elif b == 'pause' or b == '3' or b == 'three':
                    pygame.mixer.music.pause()

                elif b == 'break' or b == '5' or b == 'five':
                    pygame.mixer.music.stop()
                    break

                else:
                    print('Wrong format! Please try again!')

        elif "clock" in a or "time" in a or "date" in a:
            now = datetime.datetime.now()
            print("Current date and time: ", now.strftime("%Y-%m-%d %H:%M:%S"))
            speak("Current date and time: " + now.strftime("%Y-%m-%d %H:%M:%S"))
        elif "bye" in a or "goodbye" in a:
            d = "Good bye."
            speak(d)
            break 
        elif a == "exit":
            d = "Good bye."
            speak(d)
            exit()
        elif "hi" in a or "hello" in a: 
            d = "Hi. How can I help you?"
            speak(d)
        elif "weather" in a:
            d= "Which city you live?"
            print(d)
            speak(d)
            location = listen()
            d = "Which country?"
            print(d)
            speak(d)
            country = listen()
            if country in country_codes:
                country= country_codes[country]

            else:
                d = "Country not found in our dataset."
                speak(d)
                print(d)
                country=country
            try:
                desc = description(location, country)
                d=f"In {location} the weather is {desc}"
                speak(d)
                print(d)
                advice = get_weather_advice(desc)
                speak(advice)
                print(advice)


            except:
                d="couldn't find any results!"
                print(d)
                speak(d)
        elif "set alarm" in a or "alarm" in a:
            # ask user for the time of the alarm
            speak("At what time do you want to set the alarm? Say in seconds.")
            print("Input the seconds (For example 60 for 1 min): ")
            seconds = listen()

            # Check if the given input is a number
            try:
                seconds = int(w2n.word_to_num(seconds))
            except ValueError:
                speak("I couldn't understand the number you said. Please try again.")
                continue

            # Set the alarm using a timer
            t = threading.Timer(seconds, alarm)
            t.start()
            speak(f"Alarm set for {seconds} seconds.")
            print(f"Alarm set for {seconds} seconds.")

        else:
            if check_API()!="No":
                try:
                    message={"role":"user","content":a}
                    messages.append(message)
                    response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=messages )
                    result = response["choices"][0]["message"]["content"]
                    print(result)
                    speak(result)
                    messages.append(response["choices"][0]["message"])
                except:
                    api_not_worked()
            else:
                api_not_worked()


                        #a = listen()
            # except sr.UnknownValueError:
            #     continue
