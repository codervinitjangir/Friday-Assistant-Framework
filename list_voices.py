import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

print(f"Funds {len(voices)} voices:")
for index, voice in enumerate(voices):
    print(f"Index: {index}")
    print(f"Name: {voice.name}")
    print(f"ID: {voice.id}")
    print("-" * 20)
