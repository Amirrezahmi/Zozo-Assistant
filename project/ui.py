#This is the same as 'main.py' but this time not console-based but UI.
import tkinter as tk
from tkinter import messagebox
import requests
import string
import random
import pyttsx3
import datetime
import speech_recognition as sr
from word2number import w2n
import threading
import pygame
from country_codes import country_codes
import joblib
import os
import openai
from tkinter import scrolledtext

engine = pyttsx3.init()
engine.setProperty('rate', 150)

# OpenAI API
OPENAI_API_KEY = ''    # Paste your API Key here

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]

# Check for API
def check_API():
    if len(OPENAI_API_KEY) != 0:
        openai.api_key = OPENAI_API_KEY
    else:
        return "No"

def api_not_worked(a):
    pipeline = joblib.load('model2.joblib')  # Paste your path
    print("API didn't work! Now we are using our pipeline model...")
    result = pipeline.predict([a])[0]
    return result


def cleaner(x):
    return [a for a in (''.join([a for a in x if a not in string.punctuation])).lower().split()]

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

# Global variable for the name
name = "Amirreza"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def alarm():
    pygame.mixer.init()
    pygame.mixer.music.load('Ring.wav')
    pygame.mixer.music.play()

zero = 0

def one_time():
    global zero
    if zero < 1:
        p = "Ok. Now write whatever you want."
        print(p)
        speak(p)
    zero += 1

def listen():
    mic = "no"
    if mic.lower() == "1" or mic.lower() == "y" or mic.lower() == "yes":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            li = ["Say something!", "OK?", "Now what?", "Speak up, I'm listening"]
            p = random.choice(li)
            speak(p)
            print(p)
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            # Update chatroom display with user input
            update_chatroom("User: " + text, "")
            return text
        except sr.UnknownValueError:
            p1 = "Sorry, I couldn't understand you. Please try again."
            speak(p1)
            print(p1)
            return listen()  # Retry listening
        except sr.RequestError as e:
            p2 = "Sorry, I am currently experiencing some technical issues. Please try again later."
            speak(p2)
            print(p2)
            return listen()  # Retry listening
    else:
        text = input("Enter your input: ")
        # Update chatroom display with user input
        update_chatroom("User: " + text, "")
        return text
def assistant_text(text):
    return input_box.get()
def aa(text):
    if "time" in text or "clock" in text:
        time = datetime.datetime.now().strftime("%H:%M")
        p = "The current time is " + time
        return p
    elif "date" in text:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        p = "The current date is " + date
        return p
    elif "bye" in text.lower():
        p="Good Bye!"
        update_chatroom(text, p)
        exit()
    else:
        input_text = text
        a = input_text
        message = {"role": "user", "content": a}
        messages.append(message)
        response = check_API()
        try:
            if response == "No":
                return api_not_worked(a)
            else:
                response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
                result = response["choices"][0]["message"]["content"]
                return result
        except:
            return api_not_worked(a)

def show_chatroom():
    chat_window.pack()
    mic_label.pack_forget()
    mic_entry.pack_forget()
    submit_button.pack_forget()
    exit_button.pack_forget()
    text_box.pack_forget()
    label.pack_forget()


def update_chatroom(prompt, response):
    chat_display.configure(state='normal')
    chat_display.insert(tk.END, f"User: {prompt}\n", 'user')
    chat_display.insert(tk.END, f"Bot: {response}\n", 'bot')
    chat_display.configure(state='disabled')
    chat_display.see(tk.END)

    engine.say(response)
    engine.runAndWait()

def on_window_configure(event):
    if window.state() == 'zoomed':
        chat_display.configure(width=window.winfo_width() // 10, height=window.winfo_height() // 30)
    else:
        chat_display.configure(width=50, height=13)

# Create a Tkinter window
window = tk.Tk()
window.title("Chatroom")
window.geometry("600x400")
window.configure(background='#F0F0F0')

# Bind the window's configure event to the update function
window.bind('<Configure>', on_window_configure)

# Create a chatroom window
chat_window = tk.Frame(window, bg='#F0F0F0')
chat_window.pack(pady=10)

# Create a scrolledtext widget for prompts and responses
chat_display = scrolledtext.ScrolledText(chat_window, width=50, height=13, bg='#FFFFFF', wrap=tk.WORD)
chat_display.pack()

# Configure tags for user and bot messages
chat_display.tag_configure('user', foreground='#000000')
chat_display.tag_configure('bot', foreground='#0000FF')

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# Create an input box for the user to enter their messages
input_box = tk.Entry(window, width=60)
input_box.pack(pady=10)
input_box.focus_set()




def submit_cha():
        
        input_value = input_box.get()
        if input_value:
            alarm_time = datetime.datetime.strptime(input_value, "%H:%M").strftime("%H:%M")



        
        response = ala(alarm_time)  # Replace with your own code to generate bot response
        submit_button = tk.Button(window, text="Send", command=submit_chaa)
        return response

g_num=0
def jnum():
    global g_num
    g_num+=1
def get_weather():
    def stop_weather():
        remove_weather_elements()
        input_box.pack()
        submit_button.pack() 

    def get_weather_info():
        location = location_entry.get()
        country = country_entry.get()

        if country in country_codes:
            country = country_codes[country]
        else:
            d = "Country not found in our dataset."
            update_chatroom(country, d)
            country = country

        try:
            desc = description(location, country)
            d = f"In {location} the weather is {desc}"
            # update_chatroom(prompt, response)
            advice = get_weather_advice(desc)
            result = f"{d}\n{advice}"
            update_chatroom(f"City: {location} & Country: {country}", result)
        except:
            d = "Couldn't find any results!"
            update_chatroom(f"City: {location} & Country: {country}", d)

        location_entry.delete(0, tk.END)
        country_entry.delete(0, tk.END)

    def remove_weather_elements():
        location_label.destroy()
        location_entry.destroy()
        country_label.destroy()
        country_entry.destroy()
        submit_butto.destroy()
        stop_button.destroy()

    # Create labels and entry fields
    location_label = tk.Label(window, text="City:")
    location_entry = tk.Entry(window)

    country_label = tk.Label(window, text="Country:")
    country_entry = tk.Entry(window)

    # Create submit button
    submit_butto = tk.Button(window, text="Get Weather", command=get_weather_info)
    stop_button = tk.Button(window, text="Back", command=stop_weather)


    # Pack labels, entry fields, and submit button
    location_label.pack()
    location_entry.pack()
    country_label.pack()
    country_entry.pack()
    submit_butto.pack()
    stop_button.pack()
    submit_button.pack_forget()

def play_music():
    folder_path = 'music' # Change based on your path
    music_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.mp3')]

    pygame.mixer.init()
    current_music_index = 0
    pygame.mixer.music.load(music_files[current_music_index])
    pygame.mixer.music.play()

    # print('Playing:', music_files[current_music_index])
    update_chatroom("play music", "Playing music")

    def play_next():
        nonlocal current_music_index
        current_music_index = (current_music_index + 1) % len(music_files)
        pygame.mixer.music.load(music_files[current_music_index])
        pygame.mixer.music.play()
        p='Playing next music'
        update_chatroom("next music", p)

    def play_previous():
        nonlocal current_music_index
        current_music_index = (current_music_index - 1) % len(music_files)
        pygame.mixer.music.load(music_files[current_music_index])
        pygame.mixer.music.play()
        p='Playing previous music' #, music_files[current_music_index]
        update_chatroom("previous music", p)

    def pause_music():
        pygame.mixer.music.pause()
        update_chatroom("pause", "music paused")

    def unpause_music():
        pygame.mixer.music.unpause()
        update_chatroom("unpause", "music unpaused")

    def stop_music():
        pygame.mixer.music.stop()
        remove_music_buttons()
        update_chatroom("stop", "Stopped")
        submit_button.pack() 

    def remove_music_buttons():
        next_button.destroy()
        previous_button.destroy()
        pause_button.destroy()
        unpause_button.destroy()
        stop_button.destroy()

    # Create buttons
    next_button = tk.Button(window, text="Next", command=play_next)
    previous_button = tk.Button(window, text="Previous", command=play_previous)
    pause_button = tk.Button(window, text="Pause", command=pause_music)
    unpause_button = tk.Button(window, text="Unpause", command=unpause_music)
    stop_button = tk.Button(window, text="Stop", command=stop_music)

    # Pack buttons
    next_button.pack()
    previous_button.pack()
    pause_button.pack()
    unpause_button.pack()
    stop_button.pack()
    submit_button.pack_forget()

    

def submit_chat():
    prompt = input_box.get()
    input_box.delete(0, tk.END)

    if "set alarm" in prompt or "alarm" in prompt:
        submit_button.pack_forget()
        # Ask the user for the time of the alarm
        p = "At what time do you want to set the alarm? Enter the time in seconds."
        update_chatroom(prompt, p)

        def capture_alarm_time():
            seconds = input_box.get()
            try:
                seconds = int(seconds)
            except ValueError:
                if g_num < 1:
                    jnum()
                else:
                    p = "Invalid input. Please enter a valid number of seconds."
                    update_chatroom(seconds, p)
                    input_box.delete(0, tk.END)
                return

            # Set the alarm using a timer
            t = threading.Timer(seconds, alarm)
            t.start()

            p = f"Alarm set for {seconds} seconds."

            # Clear the input box
            input_box.delete(0, tk.END)

            # Update the chatroom display
            update_chatroom(f"{prompt} for {seconds} seconds", p)

            # Remove the Capture Time button
            capture_button.pack_forget()
            submit_button.pack()


        # Create a new button to capture the alarm time
        capture_button = tk.Button(window, text="Capture Time", command=capture_alarm_time)
        capture_button.pack()

        return
    elif "play music" in prompt:
        #submit_button.pack_forget()
        play_music()
        #submit_button.pack()
        return
    elif "weather" in prompt:
        update_chatroom(prompt, "Enter your city and country.")
        submit_button.pack_forget()
        get_weather()
        #submit_button.pack()
        return

    response = generate_response(prompt)  # Replace with your own code to generate bot response
    update_chatroom(prompt, response)
    submit_button.pack()
    







# Function to generate a random bot response (for testing purposes)
def generate_response(prompt):
    
    return aa(prompt)

# Create a submit button
submit_button = tk.Button(window, text="Send", command=submit_chat)
submit_button.pack()

# Run the Tkinter event loop
window.mainloop()
