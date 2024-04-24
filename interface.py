import os.path
import pyttsx3
import speech_recognition as sr
import webbrowser as wb
import datetime
import streamlit as st
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
    text += response['choices'][0]['message']['content']
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:])}.txt", "w") as f:
        f.write(text)

def chat(query):
    openai.api_key = apikey
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
    return response['choices'][0]['message']['content']

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    st.title("Zen AI Assistant")

    query_type = st.radio("Select Query Input Type:", ("Text", "Voice"))

    if query_type == "Text":
        query = st.text_input("Enter your query:")
        if st.button("Submit"):
            st.write("User Query:", query)
            response = chat(query)
            st.write("Zen's Response:", response)

    elif query_type == "Voice":
        st.write("Press the button and speak your query:")
        if st.button("Start Recording"):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                st.write("Listening...")
                r.pause_threshold = 0.6
                audio = r.listen(source)
                try:
                    query = r.recognize_google(audio, language='en-in')
                    st.write("User Query:", query)
                    response = chat(query)
                    st.write("Zen's Response:", response)
                except Exception as e:
                    st.error("Sorry, I am unable to hear you.")

if __name__ == "__main__":
    main()
