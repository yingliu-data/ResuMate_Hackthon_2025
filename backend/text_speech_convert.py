import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from groq import Groq

from dotenv import load_dotenv
load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
lab_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)


def text2speech(text):
    audio = lab_client.text_to_speech.convert(
                        text=text,
                        voice_id="onwK4e9ZLuTAKqWW03F9",
                        model_id="eleven_multilingual_v2",
                        output_format="mp3_44100_128",
                    )

    return audio

def speech2text(audio):
    # Open the audio file

    with open(audio, "rb") as file:

        transcription = groq_client.audio.transcriptions.create(
                                    file = (audio, file.read()),  # Required audio file
                                    model = "distil-whisper-large-v3-en",  # Required model to use for transcription
                                    prompt = "Specify context or spelling",  # Optional
                                    response_format = "json",  # Optional
                                    language = "en",  # Optional
                                    temperature = 0.0  # Optional
                             )

    return transcription.text

if __name__ == "__main__":
    audio = text2speech("Hello here is eleven lab")
    print(audio)
    # play(audio)
    # result = speech2text("20250222_211044_recording.webm")


