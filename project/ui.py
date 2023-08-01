#This is the same as 'main.py' but this time not console-based but UI.
import tkinter as tk
from tkinter import messagebox
from tkinter import messagebox, scrolledtext, ttk, filedialog
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
import time
import shutil
from queue import Queue

# 'message_queue' will be our means of communication between recognition thread and main program thread
message_queue = Queue()
pygame.init()
def play_siri1():
    pygame.mixer.music.load("siri1.mp3")
    pygame.mixer.music.play()

def play_siri2():
    pygame.mixer.music.load("siri2.mp3")
    pygame.mixer.music.play()

btn_status = False

listening_flag = threading.Event()
listen_thread = None  # Track the active listen_for_speech thread

def listen_for_speech(queue: Queue):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    global listen_thread

    while True:
        with microphone as mic:
            # Wait for the call to start listening
            queue.get()

            # Check if the loop should run
            if not listening_flag.is_set():
                break

            while btn_status:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(mic, duration=1)
                audio = recognizer.listen(mic)

                if not btn_status:  # Stop the loop if the button is clicked
                    break

                print("Recognizing...")
                try:
                    text = recognizer.recognize_google(audio)
                    # Get the existing text from the input box
                    existing_text = input_box.get()
                    # Update the input box with the recognized speech joined with existing text
                    if existing_text.strip():  # Check if the input box is not empty
                        input_box.delete(0, tk.END)
                        input_box.insert(0, existing_text + " " + text)
                    else:
                        input_box.insert(tk.END, text)  # Append recognized speech to the end
                except sr.UnknownValueError:
                    print("Could not understand")
                except sr.RequestError:
                    print("Failed to get results.")

            # Reset the listen_thread when the loop exits
            listen_thread = None
            # Stop listening if the button is clicked while waiting for input
            if not btn_status:
                break

def start_stop_listening():
    submit_button.pack_forget()
    global btn_status, listen_thread

    btn_status = not btn_status
    if btn_status:
        listening_button.configure(text='⏹')
        play_siri1()
        if listen_thread is None or not listen_thread.is_alive():
            listening_flag.set()  # Set the flag to True to start the loop
            recognize_thread = threading.Thread(target=listen_for_speech, args=(message_queue,))
            recognize_thread.daemon = True
            recognize_thread.start()
            listen_thread = recognize_thread
            message_queue.put('start')
            print("Button clicked, start listening")
            #play_siri1()
    else:
        listening_button.pack_forget()
        submit_button.pack()
        listening_button.pack()
        listening_button.configure(text='🎙')
        listening_flag.clear()  # Set the flag to False to stop the loop
        print("Button clicked, stop listening")
        play_siri2()



engine = pyttsx3.init() # In this line of code you may face an error if you are using a non-Windows OS. In this case please follow my notes in the comment below: 👇
'''
1. First, make sure to install the pyttsx3 library correctly. Incorrect installation could potentially cause such an error. You can do this by running the following command in your terminal:
    pip uninstall pyttsx3
    pip install pyttsx3
2. Upgrade the library if it's outdated because some old versions might cause the error. Run the following command to update pyttsx3:
    pip install --upgrade pyttsx3
Note: Step 3 is crucial, especially if you are using a non-Windows OS such as Linux. It is essential to note that this program has been developed on a Windows-powered device, which may result in encountering errors with certain libraries on other operating systems, such as pyttsx3. In this case read step 3 carefully.
3. pyttsx3 uses speech synthesis engines that depend on your operating system. Make sure that the corresponding speech engine is correctly installed and configured. For example, on Linux, pyttsx3 uses espeak. You might need to install it in case you are using Linux:
    sudo apt-get update && sudo apt-get install espeak
'''
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
    text=text.lower()
    if "what time is it" in text or text=="time":
        time = datetime.datetime.now().strftime("%H:%M")
        p = "The current time is " + time
        return p
    elif "who am i" in text or "what is my name" in text:
        p = f"You are {name}."
        return p
    elif text == "zozo":
        p=["yes?","I'm listening", f"{name}?"]
        p= random.choice(p)
        return p
    elif "date" in text:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        p = "The current date is " + date
        return p
    elif "bye" in text:
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
window.title("Zozo")
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
    input_box.pack_forget()
    def stop_weather():
        remove_weather_elements()
        input_box.pack()
        submit_button.pack() 
        listening_button.pack()

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
    listening_button.pack_forget()


# Global variable to store music files
music_files = []

def music_management():
    global music_files # Access the global music_files variable
    def remove_music_management_elements():
        music_management_window.destroy()

    def delete_music():
        index = music_list.curselection()[0]
        music_file = music_files[index]
        result = messagebox.askyesno("Confirm Deletion", f"Do you really want to delete '{os.path.basename(music_file)}'?")
        if result:
            os.remove(music_file)
            music_list.delete(index)
            del music_files[index]

    def add_music():
        filename = filedialog.askopenfilename(initialdir="/", title="Select Music File", filetypes=[("MP3 files", "*.mp3")])
        if filename:
            if filename.endswith(".mp3"):
                shutil.copy(filename, "music/")
                music_files.append(filename)
                show_music_list()
            else:
                messagebox.showerror("Error", "Please select an MP3 file.")
        
    def show_music_list():
        music_list.delete(0, tk.END)
        for i, music_file in enumerate(music_files):
            music_list.insert(tk.END, os.path.basename(music_file))

    music_files = [os.path.join("music", f) for f in os.listdir("music") if f.endswith(".mp3")]

    # Create a new window for music management
    music_management_window = tk.Toplevel(window)
    music_management_window.title("Music Management")
    music_management_window.geometry("400x500")

    # music_management_window.grid_rowconfigure(0, weight=1)
    # music_management_window.grid_columnconfigure(0, weight=1)

    # Create a label for the title
    title_label = tk.Label(music_management_window, text="Music Management", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, pady=10, sticky="n")

    # Create a custom Listbox widget with canvas feature to display the music list
    class CustomListbox(tk.Listbox):
        def init(self, master, **kwargs):
            super().init(master, **kwargs)
            self.bind("<MouseWheel>", self.hide_delete_icon)

        def show_delete_icon(self, event):
            index = self.nearest(event.y)
            x, y, _, _ = self.bbox(index)
            width = self.winfo_width()
            self.delete_icon.place(x=width - 30, y=y)  # Move the '❌' icon to the right corner of the row

        def hide_delete_icon(self, event):
            self.delete_icon.place_forget()

    music_list = CustomListbox(music_management_window, font=("Arial", 12), height=10, selectbackground="#b2d8b2", selectforeground="black", activestyle="none")
    music_list.grid(row=1, column=0, pady=10, sticky="nsew")

    for i, music_file in enumerate(music_files):
        music_list.insert(tk.END, os.path.basename(music_file))

    def show_delete_icon(event):
        index = music_list.nearest(event.y)
        x, y, _, _ = music_list.bbox(index)
        width = music_list.winfo_width()
        music_list.delete_icon.place(x=width - 30, y=y)  # Move the '❌' icon to the right corner of the row

    # Create a delete icon label
    music_list.delete_icon = tk.Label(music_list, text="❌", cursor="hand2", font=("Arial", 12))
    music_list.delete_icon.bind("<Button-1>", lambda event: delete_music())

    # Bind the Listbox to show the delete icon on selection
    music_list.bind("<Button-1>", show_delete_icon)

    # Create a Scrollbar for the Listbox
    scrollbar = ttk.Scrollbar(music_management_window, orient=tk.VERTICAL, command=music_list.yview)
    scrollbar.grid(row=1, column=1, sticky="ns")
    music_list.config(yscrollcommand=scrollbar.set)

    # Create a button to add music
    add_music_button = tk.Button(music_management_window, text="Add Music", command=add_music)
    add_music_button.grid(row=2, column=0, pady=10, sticky="n")

    # Create a back button to go back to the music player
    back_button = tk.Button(music_management_window, text="Back", command=remove_music_management_elements)
    back_button.grid(row=3, column=0, pady=10, sticky="n")
    # Configure resizing behavior for widgets
    music_management_window.grid_rowconfigure(1, weight=1)
    music_list.grid_rowconfigure(0, weight=1)
    music_list.grid_columnconfigure(0, weight=1)
    music_management_window.grid_columnconfigure(0, weight=1)


def play_music():
    global music_files # Access the global music_files variable
    input_box.pack_forget()
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
        input_box.pack()
        submit_button.pack()
        listening_button.pack()

    def remove_music_buttons():
        next_button.destroy()
        previous_button.destroy()
        pause_button.destroy()
        unpause_button.destroy()
        stop_button.destroy()
        music_management_button.destroy()  # New button to manage music



    # Create buttons
    next_button = tk.Button(window, text="Next", command=play_next)
    previous_button = tk.Button(window, text="Previous", command=play_previous)
    pause_button = tk.Button(window, text="Pause", command=pause_music)
    unpause_button = tk.Button(window, text="Unpause", command=unpause_music)
    stop_button = tk.Button(window, text="Stop", command=stop_music)
    music_management_button = tk.Button(window, text="Music Management", command=music_management)  # New button

    # Pack buttons
    next_button.pack()
    previous_button.pack()
    pause_button.pack()
    unpause_button.pack()
    stop_button.pack()
    music_management_button.pack()  # New button

    submit_button.pack_forget()
    listening_button.pack_forget()



    

def submit_chat():
    global btn_status
    btn_status = False  # Stop the speech recognition loop

    prompt = input_box.get()
    input_box.delete(0, tk.END)
    

    if "set alarm" in prompt or "alarm" in prompt:
        submit_button.pack_forget()
        listening_button.pack_forget()
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
            listening_button.pack()


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
    #listening_button.pack()
    







# Function to generate a random bot response (for testing purposes)
def generate_response(prompt):
    
    return aa(prompt)

# Create a submit button
submit_button = tk.Button(window, text="Send", command=submit_chat)
submit_button.pack()
listening_button = tk.Button(window, text='🎙', command=start_stop_listening)
listening_button.pack()
# Run the Tkinter event loop
window.mainloop()
