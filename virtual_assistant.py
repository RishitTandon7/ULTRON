import speech_recognition as sr
import cv2
import face_recognition
import pyttsx3
import datetime
import turtle as t
import webbrowser
import subprocess
import pyautogui
import requests
from bardapi import BardCookies
from bs4 import BeautifulSoup
import requests
from googletrans import Translator
from gtts import gTTS
import os
import sys
import PyPDF2
import nltk  # Ensure NLTK is installed
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import json
import pywhatkit as kit
import pyfiglet 
from tqdm import tqdm
import time

 


language_mapping = {
    
    'afrikaans': 'af',
    'albanian': 'sq',
    'amharic': 'am',
    'arabic': 'ar',
    'armenian': 'hy',
    'azerbaijani': 'az',
    'basque': 'eu',
    'belarusian': 'be',
    'bengali': 'bn',
    'bosnian': 'bs',
    'bulgarian': 'bg',
    'catalan': 'ca',
    'cebuano': 'ceb',
    'chichewa': 'ny',
    'chinese (simplified)': 'zh-cn',
    'chinese (traditional)': 'zh-tw',
    'corsican': 'co',
    'croatian': 'hr',
    'czech': 'cs',
    'danish': 'da',
    'dutch': 'nl',
    'english': 'en',
    'esperanto': 'eo',
    'estonian': 'et',
    'filipino': 'tl',
    'finnish': 'fi',
    'french': 'fr',
    'frisian': 'fy',
    'galician': 'gl',
    'georgian': 'ka',
    'german': 'de',
    'greek': 'el',
    'gujarati': 'gu',
    'haitian creole': 'ht',
    'hausa': 'ha',
    'hawaiian': 'haw',
    'hebrew': 'he',
    'hindi': 'hi',
    'hmong': 'hmn',
    'hungarian': 'hu',
    'icelandic': 'is',
    'igbo': 'ig',
    'indonesian': 'id',
    'irish': 'ga',
    'italian': 'it',
    'japanese': 'ja',
    'javanese': 'jw',
    'kannada': 'kn',
    'kazakh': 'kk',
    'khmer': 'km',
    'kinyarwanda': 'rw',
    'korean': 'ko',
    'kurdish (kurmanji)': 'ku',
    'kyrgyz': 'ky',
    'lao': 'lo',
    'latin': 'la',
    'latvian': 'lv',
    'lithuanian': 'lt',
    'luxembourgish': 'lb',
    'macedonian': 'mk',
    'malagasy': 'mg',
    'malay': 'ms',
    'malayalam': 'ml',
    'maltese': 'mt',
    'maori': 'mi',
    'marathi': 'mr',
    'mongolian': 'mn',
    'myanmar (burmese)': 'my',
    'nepali': 'ne',
    'norwegian': 'no',
    'pashto': 'ps',
    'persian': 'fa',
    'polish': 'pl',
    'portuguese': 'pt',
    'punjabi': 'pa',
    'romanian': 'ro',
    'russian': 'ru',
    'samoan': 'sm',
    'scots gaelic': 'gd',
    'serbian': 'sr',
    'sesotho': 'st',
    'shona': 'sn',
    'sindhi': 'sd',
    'sinhala': 'si',
    'slovak': 'sk',
    'slovenian': 'sl',
    'somali': 'so',
    'spanish': 'es',
    'sundanese': 'su',
    'swahili': 'sw',
    'swedish': 'sv',
    'tajik': 'tg',
    'tamil': 'ta',
    'telugu': 'te',
    'thai': 'th',
    'turkish': 'tr',
    'ukrainian': 'uk',
    'urdu': 'ur',
    'uzbek': 'uz',
    'vietnamese': 'vi',
    'welsh': 'cy',
    'xhosa': 'xh',
    'yiddish': 'yi',
    'yoruba': 'yo',
    'zulu': 'zu'
}



website = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print("User said:", command)
            return command
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return "" 

def summarize_pdf(pdf_file_path, summary_length=3):
    """Summarizes a PDF using the LexRank algorithm.

    Args:
        pdf_file_path (str): The path to the PDF file.
        summary_length (int, optional): The desired length of the summary in sentences. Defaults to 3.

    Returns:
        str: The generated summary of the PDF.
    """

    try:
        # Extract text from PDF
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

        # Parse text for summarization
        parser = PlaintextParser.from_string(text, Tokenizer("english"))

        # Summarize using LexRank
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, summary_length)

        # Extract and format sentences
        sentence_list = [str(sentence) for sentence in summary]
        summary_text = " ".join(sentence_list)

        return summary_text

    except Exception as e:
        return f"Error summarizing PDF: {e}"



def translate_and_speak(text, target_language='english'):
    # Use the mapping to get the language code
    target_language_code = language_mapping.get(target_language.lower(), 'en')

    translator = Translator()
    translated_text = translator.translate(text, dest=target_language_code).text

    # Create a gTTS object
    tts = gTTS(translated_text, lang=target_language_code)

    # Save the generated speech as an audio file
    tts.save("translated_speech.mp3")

    # Play the audio file
    os.system("start translated_speech.mp3")

    return translated_text

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def solve_math(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return "Sorry, I couldn't understand the math problem."

def split_and_save_paragraphs(data, filename):
    paragraphs = data.split('\n\n')
    with open(filename, 'w') as file:
        file.write(data)
    data = paragraphs[:2]
    separator = ', '
    joined_string = separator.join(data)
    return joined_string

def get_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    
    if response.status_code == 200:
        joke_data = json.loads(response.text)
        return joke_data["setup"], joke_data["punchline"]
    else:
        return "Error fetching joke", ""

def tell_joke():
    setup, punchline = get_joke()
    print("Here's a joke for you:")
    speak("Here's a joke for you:")
    print(setup)
    speak(setup)
    input("Press Enter to reveal the punchline...")
    print(punchline)
    speak(punchline)

# Function that performs a task with a progress bar
def task_with_progress_bar(total_iterations):
    for _ in tqdm(range(total_iterations), desc="Processing", unit="iteration"):
        # Simulate some work
        time.sleep(0.001)




# Load the image of the person's face you want to recognize
known_image_path = "C:\\Users\\Rishit Tandon\\Downloads\\Screenshot_20240122_185454_Gallery.jpg"

known_image = face_recognition.load_image_file(known_image_path)
known_encoding = face_recognition.face_encodings(known_image)[0]

def recognize_face(frame):
    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if the face matches the known face
        matches = face_recognition.compare_faces([known_encoding], face_encoding)

        if True in matches:
            return True  # Face recognized

    return False  # Face not recognized

# Open a video capture
cap = cv2.VideoCapture(0)  # Use 0 for default camera, or provide the camera index
speak("To use ultron you need to do facial recognition")
c=True
while c:
    ret, frame = cap.read()

    # Resize the frame for faster processing (optional)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert BGR image to RGB (required by face_recognition library)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Check if the face is recognized
    if recognize_face(rgb_small_frame):
        # Execute the rest of your program here
        speak("Face recognized! Execute your program.")
        print("Face recognized! Execute your program.")

        speak("Starting ultron")         
        result = pyfiglet.figlet_format("STARTING ULTRON ....", font = "big" ) 
        print(result)
       
        if __name__ == "__main__":
            speak("Hello! I am ULTRON your virtual assistant.")
            print("Hello! I am ULTRON your virtual assistant.")
            
            while True:
                command = take_command()
                
                if "hello" in command:
                    print("Hello! How can I help you?")
                    speak("Hello! How can I help you?")
                
                elif "calculate" in command or "solve" in command:
                    math_problem = command.split("calculate", 1)[1].strip() 
                    if "calculate" in command:
                        result = solve_math(math_problem)

                    else:
                        command.split("solve", 1)[1].strip()
                        speak(f"The answer is {result}")
                        print(f"The answer is {result}")
                
                elif "time" in command and "what is the" in command:
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    print(f"The current time is {current_time}")
                    speak(f"The current time is {current_time}")
                
                elif "how are you" in command:
                    print("I am fine thank you!! What about you??")
                    speak("I am fine thank you!! What about you??")

                elif "exit" in command:
                    speak("Goodbye!!!!!!")
                    print("Goodbye!")
                    break

                if "are you friend to humans" in command:
                    print("Yes I am....................I guess")
                    speak("Yes I am....................I guess")
                    speak("Or may i hack your system")
                    total_iterations = 100
                    task_with_progress_bar(total_iterations)
                    result = pyfiglet.figlet_format("Hacking", font = "big" ) 
                    speak("just kidding sir     Humans are my friends    and in humans espxecially...... I wont speak ask me another question")
                    


                elif "draw shapes" in command:
                    
                    pen = t.Turtle()
                    speak("Which Shape?")
                    command = take_command()
                    if "circle" in command:
                        screen = t.Screen()
                        r = 50
                        print(t.circle(r))
                        pen.clear()
                    elif "square" in command:
                        for _ in range(4):
                            t.forward(50)  # Forward turtle by s units
                            t.left(90)  # Turn turtle by 90 degree
                            pen.clear()
                    elif "heart" in command:
                        print("If you want to add a Qupid's arrow Please say 'Qupid's arrow'")
                        command = take_command()
                        if "qupids arrow" in command:
                            #Add qupid's arrow
                            heart.goto(0, -200)
                            heart.penup()
                            heart.right(40)
                            heart.forward(200)
                            heart.right(135)
                            heart.pendown()
                            heart.width(5)
                            heart.forward(700)    
                        else:
                            # Create a turtle screen
                            screen = turtle.Screen()
                            screen.bgcolor("pink")
                            # Create a turtle
                            heart = turtle.Turtle()
                            heart.color("blue")
                            heart.speed(100)

                            # Move to the starting position
                            heart.penup()
                            heart.goto(0, -200)
                            heart.pendown()

                            # Draw the heart shape
                            heart.begin_fill()
                            heart.fillcolor("purple")
                            heart.left(140)
                            heart.forward(224)
                            for _ in range(200):
                                heart.right(1)
                                heart.forward(2)
                                heart.left(120)
                            for _ in range(200):
                                heart.right(1)
                                heart.forward(2)
                                heart.forward(224)
                                heart.end_fill()

                                # Close the window on click
                                screen.exitonclick()   

                elif "what can you do" in command:
                    speak("I can do Google Searches, Open Websites, Do Simple Math problems, and intract with you in many ways")

                elif "open website" in command:
                    # Extracting the website URL from the command
                    parts = command.split()
                    website = parts[parts.index("website") + 1]
                    webbrowser.open(website)
                    print(f"Opening {website} in your web browser...")

                elif "search google for" in command:
                    # Extracting the search query from the command
                    query = command.split("search google for ", 1)[1]
                    search_url = f"https://www.google.com/search?q={query}"
                    webbrowser.open(search_url)
                    print(f"Searching Google for: {query}")

                elif "open application" in command:
                    # Extracting the application name from the command
                    parts = command.split()
                    app_name = ' '.join(parts[parts.index("application") + 1:])
                    try:
                        subprocess.Popen(app_name)
                        print(f"Opening {app_name}...")
                    except FileNotFoundError:
                        print(f"Could not find {app_name}. Please check the application name.")

                elif "minimise window" in command:
                    pyautogui.hotkey('win', 'm')  # Minimize the current window
                    print("Minimizing the window...")

                elif "close window" in command:
                    pyautogui.hotkey('alt', 'f4')  # Close the current window
                    print("Closing the window...")

                elif "type" in command:
                    text_to_type = command.split("type ", 1)[1]
                    pyautogui.typewrite(text_to_type)
                    print(f"Typing: {text_to_type}")

                elif "i want to ask you a question" in command:
                    speak("Yes sir I am here to help you only")

                elif "what is the temperature" in command:
                    search = "temperature of delhi"
                    url = f"https://www.google.com/search?q={search}"
                    r = requests.get(url)
                    data = BeautifulSoup(r.text, "html.parser") 
                    temp = data.find("div",class_="BNeawe").text 
                    print(f" current temp {temp}")
                    speak(f"{temp}")

                elif "what is the news" in command:
                    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=83263a48521a48a797182dbc3926e513'
                    main_page = requests.get(main_url).json()
                    
                    articles = main_page["articles"]
                    
                    head = []
                    day = ["first", "second", "third"]
                    
                    for ar in articles:
                        head.append(ar["title"])
                    
                    for i in range(len(day)):
                        print(f"Today's {day[i]} news is: {head[i]}")
                        # Assuming you want to use pyttsx3 for text-to-speech
                        speak(f"Today's {day[i]} news is: {head[i]}")
            
                elif "translate" in command:
                    input_text = input("Enter the text to translate: ")
                    target_language = input("Enter the target language (e.g., 'English', 'Spanish', 'Hindi'): ")
                    translated_text = translate_and_speak(input_text, target_language)
                    print(f"Translated text: {translated_text}")
                
                elif "summarise pdf" in command:
                    speak("Enter the pdf location")
                    pdf_file_path = input("Enter the pdf path: ")
                    summary = summarize_pdf(pdf_file_path)
                    print(summary)
                    speak(summary)

                elif "tell me a joke" in command:
                    tell_joke()

                
                elif "send message" in command:
                    num=input("Enter the number")
                    msg=input("Enter the message")
                    hr=input("Enter the hour")
                    min=input("Enter the message")
                    kit.sendwhatmsg(num, msg,hr,min)     

                else:
                    speak("I'm sorry, I don't understand that command.")



            # Display the video feed
            cv2.imshow('Video Feed', frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
        else:
            for i in range(1, 10):
                if i < 10:
                    print("Face not recognized")
                    continue
                else:
                    c=False
    # Release the video capture and close the OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
