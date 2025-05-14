import requests
import os

def text_to_speech(text, voice_id):
    API_KEY = "sk_01157d79c97684506237cf7f7fe0c81f68761e7847a08a02"
    URL = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8
        }
    }

    response = requests.post(URL, headers=headers, json=data)

    if response.status_code == 200:
        with open("elevenlabs_output.mp3", "wb") as file:
            file.write(response.content)
        print("✅ Audio saved as elevenlabs_output.mp3")
        return True
    else:
        print(f"❌ Error: {response.status_code}, {response.text}")
        return False

# Voice IDs
voice_options = {
    "1": "pNInz6obpgDQGcFmaJgB",  # Voice 1
    "2": "pqHfZKP75CvOlQylNhV4",  # Voice 2
    "3": "cjVigY5qzO86Huf0OWal",  # Voice 3
    "4": "Xb7hH8MSUJpSbSDYk0k2"   # Voice 4
}

def generate_podcast(text, voice_choice="1"):
    """
    Generate a podcast from text using the specified voice
    Args:
        text: The text to convert to speech
        voice_choice: Voice ID (1-4) to use
    Returns:
        bool: True if successful, False otherwise
    """
    if voice_choice in voice_options:
        return text_to_speech(text, voice_options[voice_choice])
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")
        return False