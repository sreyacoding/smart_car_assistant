# Smart Car Assistant
## Demo


https://github.com/user-attachments/assets/fea26899-a872-4965-a581-f552308accdd


## Overview

The Smart Car Assistant is an innovative application designed to enhance the driving experience by integrating voice recognition, emotion detection, drowsiness detection, and personalized music recommendations. This project utilizes a multimodal approach, leveraging modern AI techniques to create an interactive and engaging assistant for drivers.
![Conversation](https://github.com/user-attachments/assets/2cfdae94-78a0-4660-b061-f19fc55b11c2)
![WhatsApp Image 2024-10-20 at 6 29 01 AM (1)](https://github.com/user-attachments/assets/77cd5ea0-361b-4ca3-8197-83ae04dad407)
![WhatsApp Image 2024-10-20 at 6 29 01 AM](https://github.com/user-attachments/assets/e006d4bf-a3d8-4e52-b8f3-83b6a7dcfc73)


## Architecture

The application is built using the following key components:

- **Streamlit**: A powerful framework for building interactive web applications in Python. It provides a user-friendly interface for the Smart Car Assistant.

- **Text-to-Speech Engine (pyttsx3)**: This engine converts text responses from the assistant into audible speech, enhancing the interactive experience.

- **Speech Recognition (speech_recognition)**: The assistant listens to user queries and converts speech input into text, enabling natural conversations.

- **LLaMA Model (Ollama)**: A state-of-the-art language model used to generate responses to user queries based on the context provided by the conversation.

- **Emotion Prediction Model**: A trained machine learning model that predicts the user's emotional state based on their spoken input.

- **Drowsiness Detection**: A monitoring feature that detects signs of driver drowsiness and alerts the user through audio cues, ensuring safety while driving.

- **Pygame**: A library used to play music based on the detected emotion, creating a personalized audio experience for the user.

## Features

1. **General Conversation**:
   - Engage in natural conversations with the assistant.
   - Responds to user input using the LLaMA language model.

2. **Emotion Detection**:
   - Listens to the user's input to determine their emotional state.
   - Utilizes a trained emotion prediction model to classify emotions such as joy, sadness, anger, fear, love, and surprise.

3. **Drowsiness Detection**:
   - Monitors the driver's state for signs of drowsiness (e.g., yawning, head nodding).
   - Alerts the driver through audio prompts to encourage them to stay alert.

4. **Music Recommendations**:
   - Suggests and plays music based on the user's detected emotion.
   - Provides a unique auditory experience tailored to the user's mood.

5. **Interactive Voice Prompts**:
   - Uses text-to-speech to prompt the user for input, enhancing the interactive experience.
   - Speaks back responses and confirmations to keep the user engaged.

6. **User-Friendly Interface**:
   - Built using Streamlit for a seamless and intuitive user experience.

## Installation

To set up the Smart Car Assistant on your local machine, follow these steps:

1. **Install Dependencies**:
   - Ensure you have Python installed on your machine.
   - Install the required libraries using pip:

   ```bash
   pip install streamlit pyttsx3 SpeechRecognition ollama pygame
## Download the Emotion Model

Ensure you have the `final_model.pkl` file in your project directory.

## Run the Application

Execute the following command in your terminal:

```bash
streamlit run streamlit_with_drowsiness_detection.py

## Usage

- Click on the **Start Conversation** button to engage in a dialogue with the assistant.
- Use the **Suggest Music** button to prompt the assistant to ask about your feelings and receive music recommendations based on your emotional state.
- The system will continuously monitor for drowsiness, alerting the driver if signs of fatigue are detected.
- Use the **Stop Conversation** and **Stop Music** buttons to halt speech output and music playback, respectively.

