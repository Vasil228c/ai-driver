from ai import aidriver
import asyncio
import io
import edge_tts
import pygame

pygame.mixer.init()

async def _speak_async(text: str, voice: str):
    communicate = edge_tts.Communicate(text, voice)
    audio_data = bytearray()
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])

    audio_stream = io.BytesIO(audio_data)
    pygame.mixer.music.load(audio_stream)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def speak_and_wait(text: str, voice: str = "uk-UA-OstapNeural"):
    if not text.strip():
        return
    asyncio.run(_speak_async(text, voice))


aig = aidriver()

while True:
    aig.msg(input("> "))
    
    for n in aig.get_full_msg():
        print(n, flush=True, end="")
        #speak_and_wait(n)  
    print()