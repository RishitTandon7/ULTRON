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
from bs4 import BeautifulSoup
import requests
#from googletrans import Translator
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
import psutil
import subprocess
import time
import itertools
from datetime import datetime  # Change this line
import face_recognition
import cv2
import pyttsx3  # For text-to-speech (Ultron's voice engine)
import pyfiglet  # For ASCII art formatting
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageOps
import threading
import random
import math
from tkinter import *
import tkinter.font as tkFont
from datetime import datetime, timedelta
import numpy as np
import ollama_service as ollama
from img_reg import process_image



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

def interact_with_ai():
    speak("You are now talking to the AI assistant. Please say your query.")
    user_query = take_command()
    print(f"User said: {user_query}")
    speak("Do you want a long or precise reply? Please say 'long' or 'precise'.")
    response_type = take_command().lower()
    print(f"User chose: {response_type}")
    # Call the AI function
    response = ollama.get_ollama_response(user_query, response_type)
    speak(response)
    print(response)

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
    """Display message popup and speak text"""
    MessagePopup(text)  # Create popup for Ultron's response
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



# Initialize Ultron's voice engine
engine = pyttsx3.init()

# Ultron's speak function for text-to-speech
def speak(text):
    """Display message popup and speak text"""
    MessagePopup(text)  # Create popup for Ultron's response
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# OS Operations and related functions
def os_operations():
    speak("You've selected OS Operations. Here are the options:")
    print("1. List Processes - Show running processes.")
    print("2. Terminate Process - Terminate a specific process.")
    print("3. Create File - Create a new file.")
    print("4. Delete File - Delete an existing file.")
    print("5. Find File - Locate a file.")
    print("6. Back - Go back to the main menu.")

    choice = take_command()
    
    if 'one' in choice or 'list processe' in choice or 'show running processes' in choice:
        processes = psutil.process_iter(['pid', 'name'])
        speak("Listing all running processes.")
        for process in processes:
            print(process.info)
    elif 'two' in choice or 'terminate a specific process' in choice or 'Terminate Process' in choice:
        speak("Please say the name of the process to terminate.")
        process_name = take_command()
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == process_name:
                proc.terminate()
                speak(f"Process '{process_name}' terminated.")
                print(f"Process '{process_name}' terminated.")
                return
        speak(f"Process '{process_name}' not found.")
    elif 'three' in choice or 'create file' in choice:
        speak("Please say the name of the file to create.")
        filename = take_command()
        with open(filename, 'w') as f:
            f.write("File created.")
        speak(f"File '{filename}' created successfully.")
    elif 'four' in choice or 'delete' in choice:
        speak("Please say the name of the file to delete.")
        filename = take_command()
        try:
            os.remove(filename)
            speak(f"File '{filename}' deleted successfully.")
        except FileNotFoundError:
            speak(f"File '{filename}' not found.")
    elif 'five' in choice or 'find' in choice:
        speak("Please say the name of the file to find.")
        filename = take_command()
        found = False
        for root, dirs, files in os.walk('.'):
            if filename in files:
                speak(f"File '{filename}' found at: {os.path.join(root, filename)}")
                print(f"File '{filename}' found at: {os.path.join(root, filename)}")
                found = True
                break
        if not found:
            speak(f"File '{filename}' not found.")
    elif 'back' in choice:
        main()
    else:
        speak("Invalid selection.")
        os_operations()

# System Information Functions
def system_information_menu():
    speak("You've selected System Information. Here are the details:")
    print("1. Check CPU Usage - See the current CPU usage percentage.")
    print("2. Check Memory Usage - See the current memory usage.")
    print("3. Check Battery Status - See the current battery percentage.")

    choice = take_command()

    if 'one' in choice or 'check cpu usage' in choice:
        cpu_usage = psutil.cpu_percent(interval=1)
        speak(f"Current CPU Usage is {cpu_usage} percent.")
        print(f"Current CPU Usage: {cpu_usage}%")
        
    elif 'two' in choice or 'check memory usage' in choice:
        memory_info = psutil.virtual_memory()
        print(f"Total Memory: {memory_info.total / (1024 * 1024)} MB")
        print(f"Available Memory: {memory_info.available / (1024 * 1024)} MB")
        speak(f"Total Memory: {memory_info.total / (1024 * 1024)} MB, Available Memory: {memory_info.available / (1024 * 1024)} MB")
    elif 'three' in choice or 'check battery status' in choice:
        battery = psutil.sensors_battery()
        if battery is not None:
            print(f"Battery Percentage: {battery.percent}%")
            speak(f"Battery Percentage: {battery.percent} percent.")
        else:
            speak("Battery information not available.")
            print("Battery information not available.")
    elif 'back' in choice:
        main()
    else:
        speak("Invalid selection.")
        system_information_menu()

# System Control Functions
def system_control_menu():
    speak("You've selected System Control. Here are the options:")
    print("1. Shutdown - Shut down the computer.")
    print("2. Restart - Restart the computer.")
    print("3. Log Off - Log off the current user.")

    choice = take_command()

    if 'one' in choice:
        speak("Shutting down the computer now.")
        os.system("shutdown /s /t 1")
    elif 'two' in choice:
        speak("Restarting the computer now.")
        os.system("shutdown /r /t 1")
    elif 'three' in choice:
        speak("Logging off the current user.")
        os.system("shutdown /l")
    elif 'back' in choice:
        main()
    else:
        speak("Invalid selection.")
        system_control_menu()

def listen_for_wake_word(wake_word="ultron"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Ultron is in rest mode. Listening for wake word...")
        while True:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                if wake_word in command:
                    speak("Yes, how can I assist you?")
                    return True  # Wake word detected, exit rest mode
            except sr.UnknownValueError:
                pass  # Ignore unrecognized speech
            except sr.RequestError:
                speak("Sorry, I'm having trouble connecting.")
                break

# Function for Ultron's main tasks
def ultron_tasks():
    speak("I'm ready for tasks. Say 'rest mode' to put me back to rest.")
    while True:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                
                if "rest mode" in command:
                    speak("Entering rest mode.")
                    return  # Exit to rest mode
                
                # Sample commands
                elif "time" in command:
                    speak("The current time is 10 AM.")
                elif "reminder" in command:
                    speak("Setting a reminder for you.")
                # Add other task handlers here

            except sr.UnknownValueError:
                pass  # Ignore unrecognized speech
            except sr.RequestError:
                speak("Sorry, I'm having trouble connecting.")
                break

def perform_ai_search(query, platform="chatgpt"):
    if platform == "chatgpt":
        # Constructing a link to ChatGPT's main website (no API)
        search_url = f"https://chat.openai.com/chat?query={query.replace(' ', '%20')}"
    elif platform == "gemini":
        # Constructing a link to Gemini's website (update with actual query format if needed)
        search_url = f"https://www.gemini.com/search?query={query.replace(' ', '%20')}"
    else:
        speak("Platform not supported.")
        return

    # Open the link in the web browser
    webbrowser.open(search_url)
    speak(f"Opening {platform} search results for: {query}")

# Main function to listen for a query and perform the search
def ultron_search():
    speak("What would you like me to search for?")
    query = recognize_speech()
    if query:
        speak(f"Searching for {query}.")
        perform_ai_search(query, platform="chatgpt")  # Or use "gemini" as desired

# Function to display the image using PIL
def display_image(image_path):
    img = cv2.imread(image_path)
    cv2.imshow("Captured Image", img)
    cv2.waitKey(0)  # Wait until a key is pressed
    cv2.destroyAllWindows()  # Close the image window

# Load the image of the person's face you want to recognize
known_image_path = r"C:\Users\Rishit Tandon\Desktop\Passport Size Photo.jpg"

known_image = face_recognition.load_image_file(known_image_path)
known_encoding = face_recognition.face_encodings(known_image)[0]

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your query...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Network error.")
        return ""


class FaceRecognitionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultron's Firewall")
        # Add initial message
        speak("Welcome to Ultron. Please complete facial recognition to proceed.")
        # Make it fullscreen
        self.root.attributes('-fullscreen', True)
        
        # Initialize video capture with specific backend
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Try DSHOW backend for Windows
        print("Initializing camera...")
        
        if not self.cap.isOpened():
            print("Failed to open camera!")
            raise Exception("Could not open video capture")
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Test camera
        ret, test_frame = self.cap.read()
        if not ret or test_frame is None:
            print("Failed to read from camera!")
            raise Exception("Could not read from camera")
        else:
            print("Camera initialized successfully!")
        
        # Initialize recognition attributes
        self.recognition_successful = False
        
        # Load known face
        self.known_image = face_recognition.load_image_file(known_image_path)
        self.known_encoding = face_recognition.face_encodings(self.known_image)[0]
        
        # Configure colors
        self.colors = {
            'bg': '#000000',      # Black
            'scan': '#00A3FF',    # Bright blue
            'accent': '#FF0099',  # Hot pink
            'success': '#00FF00', # Neon green
            'error': '#FF0000',   # Bright red
            'text': '#FFFFFF',    # White
            'dark': '#001122'     # Dark blue
        }
        
        # Make window borderless and set background
        self.root.overrideredirect(True)
        self.root.configure(bg=self.colors['bg'])
        
        # Initialize components
        self.setup_ui_components()
        
        # Add frame processing rate control
        self.process_every_n_frames = 3
        self.frame_count = 0
        
        # Initialize scan angle
        self.scan_angle = 0
        
        # Start both the frame updates and scanning animation
        self.animate_scanning_circle()
        self.update_frame()
        
        # Add keyboard binding for escape
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        
        
        
        # Add status message at the bottom
        self.status_label = tk.Label(
            self.main_frame,
            text="WAITING FOR FACIAL RECOGNITION...",
            font=('Stencil', 24, 'bold'),
            fg='#FF0099',
            bg='black'
        )
        self.status_label.pack(side=tk.BOTTOM, pady=20)
        
        # Start periodic status update
        self.update_status_message()

    def setup_ui_components(self):
        # Main container with black background
        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bigger title
        self.title_label = tk.Label(
            self.main_frame,
            text="ULTRON SECURITY SYSTEM",
            font=('Stencil', 48, 'bold'),
            fg='#00A3FF',
            bg='black'
        )
        self.title_label.pack(pady=(50, 0))
        
        # Bigger subtitle
        self.subtitle_label = tk.Label(
            self.main_frame,
            text="BIOMETRIC AUTHENTICATION REQUIRED",
            font=('Stencil', 20, 'bold'),
            fg='#FF0099',
            bg='black'
        )
        self.subtitle_label.pack(pady=(10, 50))
        
        # Create main scanning area container
        scan_container = tk.Frame(self.main_frame, bg='black')
        scan_container.pack(expand=True)
        
        # Left info panel
        left_panel = tk.Frame(scan_container, bg='black')
        left_panel.pack(side=tk.LEFT, padx=20)
        
        # Add system stats
        stats = [
            "SYSTEM: ONLINE",
            "SECURITY: ACTIVE",
            "ENCRYPTION: ENABLED",
            "PROTOCOL: LEVEL 3",
            "STATUS: SCANNING"
        ]
        
        # Bigger system stats
        for stat in stats:
            tk.Label(
                left_panel,
                text=stat,
                font=('Stencil', 14, 'bold'),
                fg='#00A3FF',
                bg='black',
                anchor='w'
            ).pack(pady=10, fill=tk.X)
        
        # Center video frame
        self.mask_size = 400  # Increased size
        self.video_frame = tk.Frame(
            scan_container,
            bg='black',
            width=self.mask_size,
            height=self.mask_size
        )
        self.video_frame.pack(side=tk.LEFT, padx=20)
        self.video_frame.pack_propagate(False)
        
        # Video label centered in frame
        self.video_label = tk.Label(self.video_frame, bg='black')
        self.video_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Face overlay
        self.face_overlay = tk.Canvas(
            self.video_frame,
            width=self.mask_size,
            height=self.mask_size,
            bg='black',
            highlightthickness=0
        )
        self.face_overlay.place(relx=0.5, rely=0.5, anchor='center')
        
        # Right info panel
        right_panel = tk.Frame(scan_container, bg='black')
        right_panel.pack(side=tk.LEFT, padx=20)
        
        # Add scan metrics
        self.scan_metrics = []
        metrics = [
            "INITIALIZING SCAN...",
            "ANALYZING INPUT...",
            "MATCHING DATABASE...",
            "VERIFYING IDENTITY...",
            "SECURITY CHECK..."
        ]
        
        # Bigger scan metrics
        for metric in metrics:
            label = tk.Label(
                right_panel,
                text=metric,
                font=('Stencil', 14, 'bold'),
                fg='#FF0099',
                bg='black',
                anchor='w'
            )
            label.pack(pady=10, fill=tk.X)
            self.scan_metrics.append(label)
        
        # Bigger status bar
        status_frame = tk.Frame(self.main_frame, bg='#001122', height=40)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=20)
        status_frame.pack_propagate(False)
        
        # Bigger status text
        self.status_text = tk.Label(
            status_frame,
            text="INITIALIZING SECURITY PROTOCOLS...",
            font=('Stencil', 16, 'bold'),
            fg='#00A3FF',
            bg='#001122'
        )
        self.status_text.pack(pady=8)
        
        # Start status animation
        self.animate_status()
        
        # Add instruction label
        instruction_label = tk.Label(
            self.main_frame,
            text="POSITION FACE IN FRAME FOR RECOGNITION",
            font=('Helvetica', 24, 'bold'),
            fg='#FF0099',
            bg='black'
        )
        instruction_label.pack(pady=(20, 40))

    def animate_status(self):
        """Animates the status bar text"""
        status_messages = [
            "SCANNING FOR THREATS...",
            "MONITORING SECURITY...",
            "CHECKING PROTOCOLS...",
            "SYSTEM ACTIVE...",
            "AWAITING AUTHENTICATION..."
        ]
        
        def update_status():
            if not self.recognition_successful:
                message = status_messages[int(time.time()) % len(status_messages)]
                self.status_text.config(text=message)
                
                # Update scan metrics with random progress
                for label in self.scan_metrics:
                    if random.random() < 0.3:  # 30% chance to update each metric
                        label.config(text=f"{label.cget('text').split(':')[0]}: {random.randint(0, 100)}%")
                
                self.root.after(1000, update_status)
        
        update_status()

    def gradient_color(self, ratio):
        """Creates a color gradient between primary and accent colors"""
        r1, g1, b1 = int(self.colors['primary'][1:3], 16), int(self.colors['primary'][3:5], 16), int(self.colors['primary'][5:7], 16)
        r2, g2, b2 = int(self.colors['accent'][1:3], 16), int(self.colors['accent'][3:5], 16), int(self.colors['accent'][5:7], 16)
        
        r = int(r1 * (1-ratio) + r2 * ratio)
        g = int(g1 * (1-ratio) + g2 * ratio)
        b = int(b1 * (1-ratio) + b2 * ratio)
        
        return f'#{r:02x}{g:02x}{b:02x}'

    def animate_scanning_circle(self):
        if not self.recognition_successful:
            self.face_overlay.delete('all')
            
            size = self.mask_size // 2
            center = size
            
            # Draw hexagonal frame
            points = []
            for i in range(6):
                angle = math.radians(i * 60 + self.scan_angle/6)
                x = center + size * math.cos(angle)
                y = center + size * math.sin(angle)
                points.extend([x, y])
            
            # Draw outer hexagon
            self.face_overlay.create_polygon(
                points, 
                outline='#00A3FF',
                fill='',
                width=2
            )
            
            # Draw inner hexagon
            inner_points = []
            inner_size = size - 20
            for i in range(6):
                angle = math.radians(i * 60 - self.scan_angle/4)
                x = center + inner_size * math.cos(angle)
                y = center + inner_size * math.sin(angle)
                inner_points.extend([x, y])
            
            self.face_overlay.create_polygon(
                inner_points,
                outline='#FF0099',
                fill='',
                width=1
            )
            
            # Draw scanning lines
            for i in range(3):
                angle = math.radians(self.scan_angle + i * 120)
                x = center + size * math.cos(angle)
                y = center + size * math.sin(angle)
                self.face_overlay.create_line(
                    center, center, x, y,
                    fill='#00A3FF',
                    width=1,
                    dash=(5, 5)
                )
            
            # Bigger tech details
            self.face_overlay.create_text(
                center-size+20, center-size+20,
                text=f"SCAN: {self.scan_angle//3}%",
                fill='#00A3FF',
                font=('Stencil', 14, 'bold'),
                anchor='w'
            )
            
            # Bigger security number
            self.face_overlay.create_text(
                center+size-20, center+size-20,
                text=f"SEC:{random.randint(100,999)}",
                fill='#FF0099',
                font=('Stencil', 14, 'bold'),
                anchor='e'
            )
            
            self.scan_angle = (self.scan_angle + 3) % 360
            self.root.after(20, self.animate_scanning_circle)

    def show_failed_recognition(self):
        """Shows animation for failed recognition"""
        self.face_overlay.delete('all')
        center = self.mask_size // 2
        
        def animate_fail(frame=0):
            self.face_overlay.delete('all')
            
            if frame <= 10:  # Warning hexagon
                size = 100 + frame * 5
                points = []
                for i in range(6):
                    angle = math.radians(i * 60)
                    x = center + size * math.cos(angle)
                    y = center + size * math.sin(angle)
                    points.extend([x, y])
                
                self.face_overlay.create_polygon(
                    points,
                    outline='#FF0000',
                    fill='',
                    width=3
                )
                
                # Warning text
                if frame % 2:  # Blinking effect
                    self.face_overlay.create_text(
                        center, center-20,
                        text="ACCESS DENIED",
                        fill='#FF0000',
                        font=('Stencil', 30, 'bold')
                    )
                    
                    self.face_overlay.create_text(
                        center, center+20,
                        text="UNAUTHORIZED USER",
                        fill='#FF0000',
                        font=('Stencil', 12)
                    )
                
                self.root.after(100, lambda: animate_fail(frame + 1))
            else:
                # Reset scanning
                self.recognition_successful = False
                self.animate_scanning_circle()
        
        animate_fail()

    def update_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret and frame is not None:
                # Flip the frame horizontally for a mirror effect
                frame = cv2.flip(frame, 1)
                
                # Resize frame to fit our circular mask
                frame = cv2.resize(frame, (self.mask_size, self.mask_size))
                
                try:
                    # Convert BGR to RGB using cv2
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Convert the image format using numpy array
                    image = np.array(rgb_frame)
                    # Convert numpy array to bytes
                    image_bytes = image.tobytes()
                    # Create PIL Image from bytes
                    pil_image = Image.frombytes('RGB', (self.mask_size, self.mask_size), image_bytes)
                    # Convert to PhotoImage
                    photo = ImageTk.PhotoImage(pil_image)
                    
                    # Update the label
                    self.video_label.configure(image=photo)
                    self.video_label.image = photo  # Keep a reference!
                    
                except Exception as e:
                    print(f"Error in image conversion: {e}")
                    
                # Rest of your face recognition code...
                self.frame_count += 1
                if self.frame_count % self.process_every_n_frames == 0:
                    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                    if not self.recognition_successful:
                        if self.recognize_face(small_frame):
                            self.recognition_successful = True
                            self.title_label.config(
                                text="IDENTITY CONFIRMED",
                                fg='#00FF00'
                            )
                            self.show_success_animation()
                            self.root.after(2000, self.start_ultron)
                        elif self.frame_count > 90:
                            self.title_label.config(
                                text="ACCESS DENIED",
                                fg='#FF0000'
                            )
                            self.show_failed_recognition()
                
                if not self.recognition_successful:
                    self.root.after(10, self.update_frame)

    def show_success_animation(self):
        """Shows a tech-style success animation"""
        self.face_overlay.delete('all')
        center = self.mask_size // 2
        
        def animate_success(frame=0):
            self.face_overlay.delete('all')
            
            if frame <= 15:  # Expanding circles with data flow
                # Draw multiple expanding circles
                for i in range(3):
                    size = (frame * 10) - (i * 20)
                    if size > 0:
                        self.face_overlay.create_oval(
                            center-size, center-size,
                            center+size, center+size,
                            outline='#00A3FF',
                            width=2
                        )
                
                # Draw scanning lines
                for i in range(8):
                    angle = (frame * 10) + (i * 45)
                    rad = math.radians(angle)
                    length = frame * 8
                    x = center + length * math.cos(rad)
                    y = center + length * math.sin(rad)
                    self.face_overlay.create_line(
                        center, center, x, y,
                        fill='#FF0099',
                        width=1,
                        dash=(3, 3)
                    )
                
                # Add tech details
                self.face_overlay.create_text(
                    center, center-10,
                    text="ACCESS GRANTED",
                    fill='#00FF00',
                    font=('Stencil', 12, 'bold')
                )
                
                self.face_overlay.create_text(
                    center, center+10,
                    text=f"SECURITY LEVEL: {random.randint(85, 99)}%",
                    fill='#00A3FF',
                    font=('Stencil', 10)
                )
                
                self.root.after(50, lambda: animate_success(frame + 1))
                
            elif frame <= 30:  # Fade out with matrix effect
                # Create matrix-style falling characters
                for i in range(10):
                    x = random.randint(0, self.mask_size)
                    y = random.randint(0, self.mask_size)
                    char = random.choice("01")
                    opacity = int(255 * (30 - frame) / 15)
                    color = f'#00FF00{opacity:02x}'
                    
                    self.face_overlay.create_text(
                        x, y,
                        text=char,
                        fill=color,
                        font=('Stencil', 14)
                    )
                
                if frame < 30:
                    self.root.after(50, lambda: animate_success(frame + 1))
                else:
                    self.root.after(500, self.start_ultron)
        
        animate_success()

    def recognize_face(self, frame):
        """Enhanced face recognition with visual feedback"""
        if not hasattr(self, 'last_speak_time'):
            self.last_speak_time = 0
        
        current_time = time.time()
        face_locations = face_recognition.face_locations(frame)
        
        if not face_locations and current_time - self.last_speak_time > 5:
            speak("No face detected. Please position your face in the frame.")
            self.last_speak_time = current_time
            return False
        
        if face_locations:
            face_encodings = face_recognition.face_encodings(frame, face_locations)
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces([self.known_encoding], face_encoding)
                if True in matches:
                    speak("Face recognized! Welcome back.")
                    return True
                elif current_time - self.last_speak_time > 5:
                    speak("Unauthorized face detected. Access denied.")
                    self.last_speak_time = current_time
        
        return False

    def start_ultron(self):
        self.cap.release()  # Release camera
        self.root.destroy()  # Close GUI
        # Start Ultron's main functionality
        self.run_ultron()

    def run_ultron(self):
        result = pyfiglet.figlet_format("STARTING ULTRON . . . .", font="big")
        print(result)
        
        speak("Face recognized! Starting Ultron")  # This will create a popup
        speak("Hello! I am ULTRON, your virtual assistant.")  # This will create a popup
        
        # Main command loop
        while True:
            command = take_command()
            if command:
                try:
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
                        speak("I can do Google Searches, Open Websites,Help you wit OS related tasks,  Do Simple Math problems, and intract with you in many ways")

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

                    
                    elif "message" in command:
                        # Get the current time
                        now = datetime.now()
                        current_hour = now.hour
                        current_minute = now.minute

                        # Debugging output
                        print(f"Current Time: {current_hour}:{current_minute}")  # Check current time
                        num = input("Enter the number: ")  # e.g., +917522865520
                        msg = input("Enter the message: ")  # e.g., Hello ma'am!
                        hr = int(input("Enter the hour (24-hour format): "))  # e.g., 15
                        min = int(input("Enter the minutes: "))  # e.g., 20
                            
                        # Check if the specified time is at least 1 minute ahead
                        if hr < current_hour or (hr == current_hour and min <= current_minute):
                            print("Error: Please enter a time that is at least one minute ahead of the current time.")
                        elif min < 0 or min > 59:
                            print("Error: Please enter a valid minute (0-59).")
                        else:
                            try:
                                kit.sendwhatmsg(num, msg, hr, min)
                            except Exception as e:
                                print(f"An error occurred: {e}")

                    elif 'os' in command:
                        os_operations()    

                    elif 'system information' in command:
                        system_information_menu()

                    elif 'system control' in command:
                        system_control_menu()

                    elif 'tell me the time' in command:
                        now = datetime.datetime.now()
                        current_time = now.strftime("%H:%M")
                        speak(f"The current time is {current_time}.")

                    elif 'ai' in command:
                        interact_with_ai()

                    if 'search in image' in command:
                        speak("What would you like to ask about the image?")
                        query = take_command().lower()  # Get voice input from the user
                        speak("Sure, capturing the image now.")
                        if query:
                            model_response = process_image(query)  # Call the process_image function from img_reg.py
                            speak(f"The model says: {model_response}")


                        
                except Exception as e:
                    print(f"Error processing command: {e}")
                    speak("I encountered an error processing that command.")


    def __del__(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()

    def draw_tech_overlay(self, left, top, right, bottom):
        """Draws tech-style overlay for face detection"""
        # Corner brackets
        size = 20
        color = self.colors['primary']
        
        # Top-left corner
        self.overlay_canvas.create_line(left, top, left + size, top, fill=color, width=2)
        self.overlay_canvas.create_line(left, top, left, top + size, fill=color, width=2)
        
        # Top-right corner
        self.overlay_canvas.create_line(right - size, top, right, top, fill=color, width=2)
        self.overlay_canvas.create_line(right, top, right, top + size, fill=color, width=2)
        
        # Bottom-left corner
        self.overlay_canvas.create_line(left, bottom - size, left, bottom, fill=color, width=2)
        self.overlay_canvas.create_line(left, bottom, left + size, bottom, fill=color, width=2)
        
        # Bottom-right corner
        self.overlay_canvas.create_line(right - size, bottom, right, bottom, fill=color, width=2)
        self.overlay_canvas.create_line(right, bottom, right, bottom - size, fill=color, width=2)
        
        # Scanning lines animation
        def animate_scan(offset=0):
            if offset < (bottom - top) and not self.recognition_successful:
                y = top + offset
                self.overlay_canvas.create_line(
                    left, y, right, y,
                    fill=self.colors['accent'],
                    width=1,
                    dash=(2, 4)
                )
                self.root.after(50, lambda: animate_scan(offset + 10))
        
        animate_scan()
        
        # Add measurement lines and data points
        margin = 40
        self.overlay_canvas.create_line(
            left - margin, top, left - 5, top,
            fill=color, dash=(2, 4), width=1
        )
        self.overlay_canvas.create_text(
            left - margin - 5, top,
            text=f"y: {top}",
            fill=color,
            font=('Stencil', 8),
            anchor='e'
        )
        
        # Add face metrics
        metrics = [
            f"SCAN ACTIVE",
            f"WIDTH: {right-left}px",
            f"HEIGHT: {bottom-top}px",
            f"CONFIDENCE: {random.randint(85, 99)}%"
        ]
        
        for i, metric in enumerate(metrics):
            self.overlay_canvas.create_text(
                right + margin,
                top + (i * 20),
                text=metric,
                fill=self.colors['primary'],
                font=('Stencil', 10),
                anchor='w'
            )

    def update_status_message(self):
        """Updates the status message periodically"""
        if not self.recognition_successful:
            messages = [
                "WAITING FOR FACIAL RECOGNITION...",
                "PLEASE POSITION YOUR FACE IN THE FRAME...",
                "SCANNING FOR AUTHORIZED USER...",
                "BIOMETRIC VERIFICATION REQUIRED..."
            ]
            current = self.status_label.cget("text")
            next_message = messages[(messages.index(current) + 1) % len(messages)]
            self.status_label.config(text=next_message)
            
            # Speak reminder every few cycles
            if next_message == messages[0]:
                speak("Please complete facial recognition to use Ultron.")
            
            self.root.after(2000, self.update_status_message)

def start_face_recognition():
    try:
        root = tk.Tk()
        app = FaceRecognitionGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Error in face recognition: {e}")

def handle_user_message(text):
    """Display user message in popup and process command"""
    MessagePopup(text, is_user=True)  # Create popup for user's message
    
    # Process the command
    if "time" in text.lower():
        current_time = datetime.now().strftime("%I:%M %p")
        response = f"The current time is {current_time}"
        speak(response)
        return response
    return None

class MessagePopup:
    def __init__(self, message, is_user=False):

        # Create popup window
        self.popup = Tk()
        self.popup.overrideredirect(True)  # Remove window decorations
        
        # Make window transparent
        self.popup.attributes('-alpha', 0.95)
        self.popup.configure(bg='#000000')
        
        # Increased window size
        screen_width = self.popup.winfo_screenwidth()
        screen_height = self.popup.winfo_screenheight()
        window_width = 600  # Increased from 400
        window_height = 180  # Increased from 120
        x_position = screen_width - window_width - 20
        y_position = screen_height - window_height - 40
        
        self.popup.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')
        
        # Create main frame with rounded corners
        self.frame = Frame(self.popup, bg='#0A1929', bd=2)
        self.frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
        
        # Message header
        header_text = "USER:" if is_user else "ULTRON:"
        header = Label(
            self.frame,
            text=header_text,
            bg='#0A1929',
            fg='#00A3FF',
            font=('Stencil', 14, 'bold')
        )
        header.place(relx=0.05, rely=0.1)
        
        # Message timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        time_label = Label(
            self.frame,
            text=timestamp,
            bg='#0A1929',
            fg='#FF0099',
            font=('Stencil', 12)
        )
        time_label.place(relx=0.75, rely=0.1)
        
        # Message content
        message_font = tkFont.Font(family='Stencil', size=12)
        self.message = Text(
            self.frame,
            wrap=WORD,
            bg='#0A1929',
            fg='#FFFFFF',
            font=message_font,
            bd=0,
            padx=10,
            pady=5
        )
        self.message.place(relx=0.05, rely=0.3, relwidth=0.9, relheight=0.5)
        self.message.insert(END, message)
        self.message.config(state=DISABLED)
        
        # Copy button

        copy_btn = Button(
            self.frame,
            text="COPY",
            command=self.copy_text,
            bg='#1A2B3C',
            fg='#00A3FF',
            font=('Stencil', 8, 'bold'),
            bd=0,
            padx=10,
            relief=FLAT
        )
        copy_btn.place(relx=0.05, rely=0.8)
        
        # Start fade out timer
        self.popup.after(5000, self.fade_out)
        
        # Bind hover events for copy button
        copy_btn.bind('<Enter>', lambda e: copy_btn.config(bg='#2A3B4C'))
        copy_btn.bind('<Leave>', lambda e: copy_btn.config(bg='#1A2B3C'))
        
        # Start the popup
        self.popup.update()
    
    def copy_text(self):
        """Copy message content to clipboard"""
        self.popup.clipboard_clear()
        self.popup.clipboard_append(self.message.get("1.0", END))
        
    def fade_out(self):
        """Gradually fade out the window"""
        alpha = self.popup.attributes('-alpha')
        if alpha > 0:
            self.popup.attributes('-alpha', alpha - 0.1)
            self.popup.after(50, self.fade_out)
        else:
            self.popup.destroy()

if __name__ == "__main__":
    start_face_recognition()

        # Start Ollama service

    ollama_service.start_ollama()
    ollama_service.wait_for_ollama()
