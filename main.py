import pyttsx3
import requests
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import pywhatkit as kit
import subprocess as sp
import pprint


NEWS_API_KEY = '776cfbb09d1b49f9b95e543629025a26'
OPENWEATHER_APP_ID = '71f43f01e42bb8a185452555e2e0754c'
paths = {
    'notepad': "C:\\Windows\\notepad.exe",
    'word': "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\"
}
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice', voices[0].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am jarvis Sir. Please tell me how may i help you")

def takeCommand():
    #It takes microphone input from users and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        print("Recognizing...")
        query = r.recognize_google(audio,language='en-in')
        print(f"User said : {query}\n")
        return query

def take_user_input():
    """Takes user input, recognizes it using speech Recognition module and converts it into text"""

    r=sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening')

def send_whatsapp_message(number,message):
    kit.sendwhatmsg_instantly(f"+91{number}", message)

def find_my_ip():
    ip_address =  requests.get('https://api64.ipify.org/?format=json').json()
    return ip_address["ip"]
def get_latest_news():
     news_headlines = []
     res = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
     articles = res["articles"]
     for article in articles:
         news_headlines.append(article["title"])
     return news_headlines[:5]

def get_weather_report(city):
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric").json()
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃"

def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]

def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']

def open_notepad():
    os.startfile(paths['notepad'])



def open_camera():
    sp.run('start microsoft.windows.camera:', shell= True)

if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand().lower()

    # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
        elif 'open cricbuzz' in query:
            webbrowser.open("cricbuzz.com")

        elif 'play music' in query:
            music_dir='E:\\song'
            songs=os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,songs[random.randint(0,len(songs)-1)]))
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"Sir,the time is {strTime}")
        elif 'send whatsapp message' in query:
            speak('on what number should i send the message sir? please enter in the console: ')
            number = input("Enter the number: ")
            speak("What is the message sir? ")
            message=takeCommand().lower()
            send_whatsapp_message(number,message)
            speak("i've sent the message sir.")
        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f"your IP Address is {ip_address}.\nFor your convenience ,I am printing it on the screen sir")
            print(f'your IP Address is {ip_address}')
        elif 'open notepad' in query:
            open_notepad()

        elif 'open camera' in query:
            open_camera()
        elif 'news' in query:
            speak(f"i'm reading out the latest news headlines, sir")

            speak("For your convenience,I am printing it on the screen sir.")
            print(*get_latest_news())
            speak(get_latest_news())

        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Getting weather report for your city {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
            speak(f"Also, the weather report talks about {weather}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")
        elif 'joke' in query:
            speak(f"Hope you like this one sir")
            joke = get_random_joke()
            speak(joke)
            speak("For your convenience, I am printing it on the screen sir.")
            print(*joke)

        elif "advice" in query:
            speak(f"Here's an advice for you, sir")
            advice = get_random_advice()
            speak(advice)
            speak("For your convenience, I am printing it on the screen sir.")
            print(*advice)

        elif "thank you for your service" in query:
            speak("You most welcome sir, please call me whenever you need me sir.")
            exit()
        elif "how are you" in query:
            speak("i'm fine ,you're very kind to ask especially in these tempestuous times.")
