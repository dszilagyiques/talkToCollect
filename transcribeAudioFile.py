from openai import OpenAI
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

# Access the API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
def get_transcript(audio_path):
    client = OpenAI(api_key=api_key)
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        # print(transcript)
    return transcript.text  # Return the transcript text
# Example usage
# print(get_transcript(r"rawAudioFiles\sample1.m4a"))
