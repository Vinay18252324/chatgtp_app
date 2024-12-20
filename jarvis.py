import pyttsx3
import speech_recognition as sr
import wikipedia
from datetime import datetime
from googlesearch import search

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Function to speak the text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to get the current time
def get_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

# Function to get the current date
def get_date():
    now = datetime.now()
    return now.strftime("%Y-%m-%d")

# Function to search Google and provide the top link
def google_search(query):
    try:
        # Ensuring query is valid and not empty
        if not query:
            return "The search query was empty, please try again."

        print(f"Searching Google for: {query}")
        results = list(search(query, num_results=3))  # Convert the generator to a list
        
        if results:
            top_result = results[0]  # Fetch the top search result
            return f"The top search result is: {top_result}"
        else:
            return "No results found."
    except Exception as e:
        print(f"Error during search: {str(e)}")
        return "Sorry, I couldn't perform the search."

# Function to take command and process it
def take_command():
    command = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        command.adjust_for_ambient_noise(source)
        command.pause_threshold = 1
        audio = command.listen(source)

        try:
            print("Recognizing...")
            query = command.recognize_google(audio, language="en-in")
            print("You said:", query)

            # If the user asks for the time
            if 'time' in query.lower():
                speak(f"The current time is {get_time()}")

            # If the user asks for the date
            elif 'date' in query.lower():
                speak(f"Today's date is {get_date()}")

            # If the user asks for general information (Wikipedia)
            elif 'what is' in query.lower() or 'who is' in query.lower():
                speak("Searching Wikipedia...")
                query = query.replace("what is", "").replace("who is", "")
                try:
                    result = wikipedia.summary(query, sentences=2)
                    speak(result)
                except wikipedia.exceptions.DisambiguationError as e:
                    speak("There were multiple results, please be more specific.")
                except wikipedia.exceptions.HTTPTimeoutError:
                    speak("Sorry, I'm having trouble connecting to Wikipedia.")
                except Exception as e:
                    speak("Sorry, I couldn't find an answer to your question.")

            # If the user asks for something general (Google search)
            else:
                speak("Searching Google...")
                result = google_search(query)
                speak(f"Here is what I found: {result}")

        except Exception as e:
            print("Sorry, I couldn't hear that.")
            speak("Sorry, I couldn't hear that. Please try again.")
            return None
        return query

# Greet and start the assistant
speak("Hello, I am your AI assistant. How can I assist you today?")
take_command()
