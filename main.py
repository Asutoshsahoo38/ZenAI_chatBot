import os.path

import pyttsx3
import speech_recognition as sr
import webbrowser as wb
import datetime
import openai
from config import apikey
def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt:{prompt}\n"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response['choices'][0]['message']['content'])
    text += response['choices'][0]['message']['content']
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:])}.txt", "w") as f:
        f.write(text)

def chat(query):
    chatStr = ''
    openai.api_key = apikey
    chatStr += f"Ashu: {query}\n Zen:"
    print(chatStr)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": query}],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    speak(response['choices'][0]['message']['content'])
    chatStr += f"{response['choices'][0]['message']['content']}\n"
    return response['choices'][0]['message']['content']



def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Sorry I am unable to hear you . Sorry from Zen A.I"

if __name__ == '__main__':
    speak("Hello, I am Zen A.I.")
    while True:
        print("Listening ... ")
        query = takeCommand()
        sites = [['YouTube''https://www.youtube.com'],
        ['Facebook', 'https://www.facebook.com'],
        ['Instagram', 'https://www.instagram.com'],
        ['Twitter', 'https://www.twitter.com'],
        ['LinkedIn', 'https://www.linkedin.com'],
        ['Github', 'https://www.github.com'],
        ['wikipedia', 'https://en.wikipedia.org'],
        ['google', 'https://www.google.com']]
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                speak(f"Opening {site[0]} sir ...")
                wb.open(site[1])
        if "time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            speak(f"The time is {hour}hour and {min}minutes")
        elif "Using Artificial intelligence".lower() in query.lower():
            ai(prompt=query)
        elif "Quit".lower() in query.lower():
            exit()
        elif "what is your name ".lower() in query.lower():
            speak("I am an AI Assistant of ZEN A.I Bot")    
        else:
            chat(query)