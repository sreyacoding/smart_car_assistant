import streamlit as st
import pyttsx3
import speech_recognition as sr
import ollama
import threading
import pygame
import os
import pickle
import time
from queue import Queue

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set speech rate

# Initialize Pygame mixer for playing music
pygame.mixer.init()

# Set default values in Streamlit's session state
if 'speaking' not in st.session_state:
    st.session_state.speaking = False
if 'response_text' not in st.session_state:
    st.session_state.response_text = ""
if 'emotion' not in st.session_state:
    st.session_state.emotion = ""
if 'speech_queue' not in st.session_state:
    st.session_state.speech_queue = Queue()  # Queue for managing speech requests
if 'alarm_playing' not in st.session_state:
    st.session_state.alarm_playing = False

# Function to convert text to speech (with queue management)
def speak_text(text):
    st.session_state.speech_queue.put(text)  # Add text to the queue
    process_speech_queue()  # Process the queue immediately

def process_speech_queue():
    if not st.session_state.speech_queue.empty() and not st.session_state.speaking:
        st.session_state.speaking = True
        text = st.session_state.speech_queue.get()  # Get the next item from the queue
        engine.say(text)  # Queue the text for speaking
        engine.runAndWait()  # Block until all speech is finished
        st.session_state.speaking = False
        process_speech_queue()  # Process the next item in the queue

# Function to convert speech to text
def listen_to_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            st.write("Processing...")
            text = recognizer.recognize_google(audio)
            st.write(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.write("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            st.write("Sorry, I couldn't request results from the speech recognition service.")
            return None

# Function to get a response from the LLaMA model
@st.cache_resource
def load_llama_model():
    return "llama3:latest"  # Specify the correct LLaMA model

# Load the model (caching to improve performance)
model = load_llama_model()

def get_llama_response(prompt):
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    
    # Adjusting for the correct key in the response object
    if 'message' in response and 'content' in response['message']:
        return response['message']['content']
    else:
        st.write("Error: The response does not contain a 'content' field.")
        return "Sorry, something went wrong."

# Function to load emotion prediction model
def load_emotion_model():
    with open('final_model.pkl', 'rb') as file:
        return pickle.load(file)

# Function to predict emotion based on text
def predict_emotion(text, model):
    return model.predict([text])[0]  # Assuming the model's predict method works this way

# Function to play song based on emotion
def play_song(emotion):
    songs = {
        "joy": "joy_song.mp3",
        "sadness": "sadness_song.mp3",
        "anger": "anger_song.mp3",
        "fear": "fear_song.mp3",
        "love": "song.mp3",
        "surprise": "surprise_song.mp3"
    }
    song_path = songs.get(emotion)
    if song_path:
        if os.path.exists(song_path):
            try:
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                st.write(f"Playing music for emotion: {emotion}")
            except Exception as e:
                st.write(f"Error loading music: {e}")
        else:
            st.write(f"Music file not found: {song_path}")
    else:
        st.write(f"No song assigned for emotion: {emotion}")

# Streamlit App UI
st.title("Smart Car Assistant")

# Start the drowsiness monitoring in a separate thread
def start_drowsiness_monitoring():
    from drowsiness_detection import start_monitoring
    start_monitoring()

drowsiness_thread = threading.Thread(target=start_drowsiness_monitoring, daemon=True)
drowsiness_thread.start()

# General Conversation Section
st.subheader("General Conversation")
if st.button("Start Conversation"):
    user_input = listen_to_speech()
    
    if user_input:
        # Get response from LLaMA
        st.session_state.response_text = get_llama_response(user_input)
        
        # Display the detected input and response
        st.write(f"You said: {user_input}")
        st.write(f"LLaMA says: {st.session_state.response_text}")
        
        # Speak the response
        speak_text(st.session_state.response_text)

# Button to stop the speech in conversation section
if st.button("Stop Conversation"):
    engine.stop()  # Stop the speech synthesis immediately
    st.write("Speech stopped.")

# Music Section
st.subheader("Music Interaction")
if st.button("Suggest Music"):
    # Display the prompt text
    st.write("How are you feeling today?")
    
    # Immediately take user input for feeling
    user_input = listen_to_speech()
    
    if user_input:
        # Predict emotion based on input
        emotion_model = load_emotion_model()
        st.session_state.emotion = predict_emotion(user_input, emotion_model)
        st.write(f"You are feeling: {st.session_state.emotion}")

        # Use audio to say the detected mood
        speak_text(f"You seem to be in a {st.session_state.emotion} mood today.")

        # Add a slight delay before speaking the next line
        time.sleep(1)

        # Use audio to say that music will be played
        speak_text("Here is some music according to your mood.")

        # Play the song corresponding to the emotion
        play_song(st.session_state.emotion)

# Button to stop the music
if st.button("Stop Music"):
    pygame.mixer.music.stop()  # Stop the music
    st.write("Music stopped.")
