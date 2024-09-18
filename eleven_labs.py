from elevenlabs import generate, voices, play, stream, save, Voice, VoiceSettings
import time
import os
from dotenv import load_dotenv

load_dotenv("api.env")

class ElevenLabsManager:

    def __init__(self):
        # Fetch voices using the `voices()` function
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        if not self.api_key:
            raise ValueError("API key not found. Please check your .env file.")
        
        self.voices = voices()  # Fetch all available voices

        # Create a map of Names->IDs, so that we can easily grab a voice's ID later on
        self.voice_to_id = {}
        for voice in self.voices:
           self.voice_to_id[voice.name] = voice.voice_id
        self.voice_to_settings = {}

    # Convert text to speech, then save it to file. Returns the file path.
    def text_to_audio(self, input_text, voice="Callum", save_as_wave=True, subdirectory="", model_id="eleven_monolingual_v1"):
        # Fetch the voice settings if they haven't been stored already
        if voice not in self.voice_to_settings:
            # Set default stability and similarity_boost values (adjust these based on your needs)
            self.voice_to_settings[voice] = VoiceSettings(stability=0.75, similarity_boost=0.75)
        
        voice_settings = self.voice_to_settings[voice]

        # Generate the audio
        audio_saved = generate(
            text=input_text,
            voice=Voice(voice_id=self.voice_to_id[voice], settings=voice_settings),
            model=model_id
        )

        # Save the audio file
        if save_as_wave:
            file_name = f"___Msg{str(hash(input_text))}{time.time()}_{model_id}.wav"
        else:
            file_name = f"___Msg{str(hash(input_text))}{time.time()}_{model_id}.mp3"

        tts_file = os.path.join(os.path.abspath(os.curdir), subdirectory, file_name)
        save(audio_saved, tts_file)

        return tts_file
