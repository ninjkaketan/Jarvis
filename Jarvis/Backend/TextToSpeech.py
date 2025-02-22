import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")

# Ensure the Data directory exists
if not os.path.exists("Data"):
    os.makedirs("Data")

async def TextToAudioFile(text) -> None:
    file_path = os.path.join("Data", "speech.mp3")

    # Remove existing file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)

    # Generate and save the audio file
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(file_path)

def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            # Generate the audio file
            asyncio.run(TextToAudioFile(Text))

            # Initialize pygame mixer and play the audio
            pygame.mixer.init()
            pygame.mixer.music.load(os.path.join("Data", "speech.mp3"))
            pygame.mixer.music.play()

            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                if func() == False:  # Allow early termination if func returns False
                    break
                pygame.time.Clock().tick(10)  # Control the loop speed

            return True
        
        except Exception as e:
            print(f"Error in TTS: {e}")
            return False
        
        finally:
            try:
                # Clean up resources
                func(False)  # Ensure func is called with False
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception as e:
                print(f"Error in finally block: {e}")

def TextToSpeech(Text, func=lambda r=None: True):
    # Split text into sentences
    sentences = [s.strip() for s in Text.split(".") if s.strip()]
    responses = [
        "Would you like me to continue?",
        "Should I go on?",
        "Do you want to hear more?"
    ]

    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    # Handle long text by splitting it into chunks
    if len(sentences) > 4 and len(Text) >= 250:
        # Speak the first two sentences and ask if the user wants to continue
        chunk = ". ".join(sentences[:2]) + "."
        TTS(chunk + " " + random.choice(responses), func)
    else:
        # Speak the entire text
        TTS(Text, func)

if __name__ == "__main__":
    while True:
        text = input("Enter the text: ")
        if text.lower() in ["exit", "quit"]:
            break
        TextToSpeech(text)