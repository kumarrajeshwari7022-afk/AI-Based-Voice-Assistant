import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import os


# ============================================================
#                 AI-BASED VOICE ASSISTANT
# ============================================================

# -------------------- Initialize ----------------------------

# Text-to-Speech engine
engine = pyttsx3.init()

# Set speaking speed
engine.setProperty("rate", 160)

# Set volume
engine.setProperty("volume", 1.0)


# -------------------- Speak Function ------------------------

def speak(text):
    """
    Converts text into speech and also displays it
    on the terminal.
    """
    print("Assistant:", text)

    engine.say(text)
    engine.runAndWait()


# -------------------- Welcome Message -----------------------

def welcome_message():
    """
    Displays and speaks the welcome message.
    """
    print("\n" + "=" * 55)
    print("        🤖 AI-BASED VOICE ASSISTANT")
    print("=" * 55)
    print("Say commands such as:")
    print("  • What is the time?")
    print("  • Open Notepad")
    print("  • Open Calculator")
    print("  • Search Wikipedia for Python")
    print("  • Search Google for AI")
    print("  • Open YouTube")
    print("  • Exit")
    print("=" * 55 + "\n")

    speak("Hello! I am your AI voice assistant.")
    speak("How can I help you today?")


# -------------------- Listen Function -----------------------

def listen():
    """
    Captures voice from the microphone and converts
    it into text using SpeechRecognition.
    """

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:

            print("\n🎤 Listening...")
            
            # Adjust microphone according to surrounding noise
            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            # Listen to the user
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        print("🔄 Recognizing...")

        # Convert speech into text
        command = recognizer.recognize_google(audio)

        command = command.lower()

        print("You:", command)

        return command

    except sr.WaitTimeoutError:
        print("⏱️ No speech detected.")
        return ""

    except sr.UnknownValueError:
        speak("Sorry, I could not understand your voice.")
        return ""

    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""

    except Exception as error:
        print("Microphone error:", error)
        speak("There was a problem with the microphone.")
        return ""


# -------------------- Tell Time ------------------------------

def tell_time():
    """
    Gets the current system time and speaks it.
    """

    current_time = datetime.datetime.now().strftime(
        "%I:%M %p"
    )

    speak(f"The current time is {current_time}.")


# -------------------- Open Applications ---------------------

def open_application(command):
    """
    Opens applications based on the user's command.
    """

    if "notepad" in command:

        speak("Opening Notepad.")
        os.system("notepad")

    elif "calculator" in command or "calc" in command:

        speak("Opening Calculator.")
        os.system("calc")

    else:

        speak(
            "I currently support Notepad and Calculator."
        )


# -------------------- Open Websites --------------------------

def open_website(command):
    """
    Opens commonly requested websites.
    """

    if "youtube" in command:

        speak("Opening YouTube.")
        webbrowser.open(
            "https://www.youtube.com"
        )

    elif "google" in command:

        speak("Opening Google.")
        webbrowser.open(
            "https://www.google.com"
        )

    else:

        speak("I don't know that website.")


# -------------------- Wikipedia Search ----------------------

def search_wikipedia(command):
    """
    Searches Wikipedia and reads a short summary.
    """

    try:

        # Remove unnecessary words
        search_topic = command.replace(
            "search wikipedia for",
            ""
        )

        search_topic = search_topic.replace(
            "search wikipedia",
            ""
        )

        search_topic = search_topic.replace(
            "wikipedia",
            ""
        )

        search_topic = search_topic.strip()

        if search_topic == "":
            speak(
                "Please tell me what you want to search on Wikipedia."
            )
            return

        speak(
            f"Searching Wikipedia for {search_topic}."
        )

        # Get Wikipedia summary
        result = wikipedia.summary(
            search_topic,
            sentences=2
        )

        print("\nWikipedia Result:")
        print(result)

        speak("According to Wikipedia:")
        speak(result)

    except wikipedia.exceptions.DisambiguationError:

        speak(
            "There are multiple results for that topic. "
            "Please be more specific."
        )

    except wikipedia.exceptions.PageError:

        speak(
            "Sorry, I could not find information about that topic."
        )

    except Exception:

        speak(
            "Sorry, I could not search Wikipedia right now."
        )


# -------------------- Google Search -------------------------

def google_search(command):
    """
    Searches Google using the user's voice command.
    """

    search_query = command.replace(
        "search google for",
        ""
    )

    search_query = search_query.replace(
        "search for",
        ""
    )

    search_query = search_query.replace(
        "search",
        ""
    )

    search_query = search_query.strip()

    if search_query == "":
        speak("What would you like me to search for?")
        return

    speak(
        f"Searching Google for {search_query}."
    )

    url = (
        "https://www.google.com/search?q="
        + search_query.replace(" ", "+")
    )

    webbrowser.open(url)


# -------------------- Help Function -------------------------

def show_help():
    """
    Displays available commands.
    """

    print("\nAvailable Commands:")
    print("-" * 40)
    print("1. What is the time?")
    print("2. Open Notepad")
    print("3. Open Calculator")
    print("4. Open Google")
    print("5. Open YouTube")
    print("6. Search Wikipedia for Python")
    print("7. Search Google for Artificial Intelligence")
    print("8. Help")
    print("9. Exit / Stop")
    print("-" * 40)

    speak(
        "I can tell the time, open applications, "
        "search Wikipedia or Google, and open websites."
    )


# -------------------- Process Command -----------------------

def process_command(command):
    """
    Identifies the user's command and calls
    the appropriate function.

    Returns True to continue.
    Returns False to stop the assistant.
    """

    if command == "":
        return True

    # -------- Time --------

    elif "time" in command:

        tell_time()

    # -------- Applications --------

    elif "open notepad" in command:

        open_application(command)

    elif "open calculator" in command:

        open_application(command)

    # -------- Websites --------

    elif "open youtube" in command:

        open_website(command)

    elif "open google" in command:

        open_website(command)

    # -------- Wikipedia --------

    elif "wikipedia" in command:

        search_wikipedia(command)

    # -------- Google Search --------

    elif (
        "search google" in command
        or "search for" in command
    ):

        google_search(command)

    # -------- Help --------

    elif "help" in command:

        show_help()

    # -------- Exit --------

    elif (
        "exit" in command
        or "stop" in command
        or "quit" in command
        or "goodbye" in command
    ):

        speak(
            "Thank you for using the AI voice assistant. Goodbye!"
        )

        return False

    # -------- Unknown command --------

    else:

        speak(
            "Sorry, I don't understand that command."
        )

        speak(
            "You can say help to hear the available commands."
        )

    return True


# -------------------- Main Program --------------------------

def main():

    welcome_message()

    while True:

        command = listen()

        should_continue = process_command(command)

        if not should_continue:
            break


# -------------------- Program Start -------------------------

if __name__ == "__main__":
    main()