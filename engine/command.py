import pyttsx3
import speech_recognition as sr
import eel
import time


def speak(text):
    
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
       
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        print(f"Received query: {query}")
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    
    query = query.strip().lower()  # Normalize query
    print(f"Normalized query: {query}")  # Print normalized query for debugging

    try:
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, WhatsApp
            contact_no, name = findContact(query)
            if contact_no != 0:
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()
                if not preferance:
                    speak("I didn't catch that. Please try again.")
                    return

                if "whatsapp" in preferance:  # Ensure this check is working as expected
                    print("WhatsApp option selected.")
                    message = ""
                    if "send message" in query:
                        message = "message"
                        speak("What message should I send?")
                        query = takecommand()
                        if not query:
                            speak("I didn't catch that. Please try again.")
                            return
                    
                    elif "phone call" in query:
                        message = "call"
                    elif "video call" in query:
                        message = "video call"
                    else:
                        speak("Invalid WhatsApp action. Please specify 'send message', 'phone call', or 'video call'.")
                    
                    if message:  # Proceed only if message is set
                        speak(f"{message} initiated on WhatsApp with {name}.")
                        WhatsApp(contact_no, query, message, name)
                    else:
                        speak("Something went wrong with WhatsApp action.")
                else:
                    speak("Invalid preference. Please choose either mobile or WhatsApp.")

            else:
                speak("Contact not found. Please try again.")
        
        else:
            print("error")
           
    except Exception as e:
        print(f"An error occurred: {e}")
        eel.DisplayMessage(f"Error: {e}")
    
    eel.ShowHood()