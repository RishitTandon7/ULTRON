import pyttsx3

def speak1(text):
    """Speak the given text with improved quality."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
    
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Change to voices[0].id for a male voice

    # Speak the text
    engine.say(text)
    engine.runAndWait()


speak1("Hello folks. I’m Ultron – your AI that sees, feels, and helps")
speak1("Ready to redefine assistance!") 
