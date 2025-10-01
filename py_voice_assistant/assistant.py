import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import speech_recognition as sr
from gtts import gTTS
import playsound3
import wikipedia
import webbrowser
import os
from datetime import datetime

USER_NAME = "Fizza"
ASSISTANT_NAME = "Alexa"

def speak(text):
    print(f"🤖 {ASSISTANT_NAME}: {text}")
    tts = gTTS(text=text, lang='en')
    tts.save("voice.mp3")
    playsound3.playsound("voice.mp3")
    os.remove("voice.mp3")

def listen(duration=5, fs=44100):
    print("Listening...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    
    # Convert float32 to int16
    recording_int16 = np.int16(recording * 32767)
    
    write("temp.wav", fs, recording_int16)
    
    r = sr.Recognizer()
    with sr.AudioFile("temp.wav") as source:
        audio = r.record(source)
    os.remove("temp.wav")
    
    try:
        command = r.recognize_google(audio)
        print(f"👧 Fizza: {command}")
        return command.lower()
    except:
        return ""


def calculate(command):
    try:
        command = command.replace("plus", "+").replace("minus", "-")
        command = command.replace("multiply", "*").replace("times", "*")
        command = command.replace("divide", "/")
        result = eval(command)
        speak(f"The answer is {result}")
    except:
        speak("I couldn't calculate that.")

def assistant():
    speak(f"Hello {USER_NAME}! I am {ASSISTANT_NAME}, your assistant. How can I help you?")

    while True:
        command = listen()

        if command == "":
            speak("I didn't catch that. Please repeat.")
            continue

        # Natural sentence mappings
        time_commands = ["what time is it", "can you tell me the time", "could you please tell me the time"]
        date_commands = ["what is the date today", "tell me the date", "could you tell me today's date"]
        hello_commands = ["hello", "hi", "hey"]
        how_are_you_commands = ["how are you", "how's it going", "how do you do"]
        goodbye_commands = ["goodbye", "bye", "see you"]
        thank_commands = ["thank you", "thanks", "thank you so much"]
        joke_commands = ["tell me a joke", "make me laugh"]
        fact_commands = ["tell me a fact", "share a fact"]

        # Time & Date
        if any(cmd in command for cmd in time_commands):
            now = datetime.now().strftime("%I:%M %p")
            speak(f"The time is {now}")
        elif any(cmd in command for cmd in date_commands):
            today = datetime.now().strftime("%d-%m-%Y")
            speak(f"Today's date is {today}")

        # Wikipedia
        elif "tell me about" in command or "who is" in command or "what is" in command:
            query = command.replace("tell me about", "").replace("who is", "").replace("what is", "").strip()
            try:
                result = wikipedia.summary(query, sentences=2, auto_suggest=False)
                speak(result)
            except:
                speak("I couldn't find that on Wikipedia.")

        # Websites / Apps
        elif "open" in command:
            if "youtube" in command:
                speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com")
            elif "google" in command:
                speak("Opening Google")
                webbrowser.open("https://www.google.com")
            elif "facebook" in command:
                speak("Opening Facebook")
                webbrowser.open("https://www.facebook.com")
            elif "notepad" in command:
                speak("Opening Notepad")
                os.system("notepad")
            elif "calculator" in command:
                speak("Opening Calculator")
                os.system("calc")
            else:
                speak("I am not sure how to open that website or app yet.")

        # Google Search
        elif "search" in command or "google" in command:
            query = command.replace("search", "").replace("google", "").strip()
            if query:
                speak(f"Searching Google for {query}")
                webbrowser.open(f"https://www.google.com/search?q={query}")
            else:
                speak("What do you want me to search for?")

        # Math
        elif any(word in command for word in ["plus","minus","multiply","divide","times"]):
            calculate(command)

        # Casual conversation
        elif any(cmd in command for cmd in hello_commands):
            speak(f"Hello {USER_NAME}! How are you?")
        elif any(cmd in command for cmd in how_are_you_commands):
            speak("I am good. Thank you!")
        elif any(cmd in command for cmd in thank_commands):
            speak("You're welcome!")
        elif any(cmd in command for cmd in goodbye_commands):
            speak("Goodbye!")
            break

        # Fun / jokes / facts
        elif any(cmd in command for cmd in joke_commands):
            speak("Why did the computer show up at work late? It had a hard drive!")
        elif any(cmd in command for cmd in fact_commands):
            speak("Did you know? Honey never spoils. Archaeologists have found edible honey in ancient Egyptian tombs!")

        else:
            speak("I am not sure how to do that yet.")

if __name__ == "__main__":
    assistant()
