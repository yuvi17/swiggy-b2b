import requests
from gtts import gTTS
import os
from speech_recognition import *
from translate import translator

recognizer = Recognizer()
phno = 'xxab'

def start():
    r = requests.get('http://localhost:5000/request-speech/{0}'.format(phno))
    print(r.text)
    n =  int(r.text)
    startLoop(2)
def startLoop(n):
    i = 0
    while i < n:
        r = requests.get('http://localhost:5000/fetchQuestion/{0}/{1}'.format(phno,i))
        # text = translator('en','hi',r.text)
        #print(text)
        text = r.text
        tts = gTTS(text=text, lang='hi')
        tts.save("resp.mp3")
        os.system("afplay resp.mp3")
        # engine.say(text)
        if i < n-1:
            with Microphone() as source:
                audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                print(text)
                new_r = requests.get('http://localhost:5000/processText/{0}'.format(text))
                status = new_r.text
                if status == "success":
                    i = i+1
            except:
                print("error")
                tts = gTTS(text="Could not catch you there!, Please repeat", lang = "hi")
                tts.save('Error.mp3')
                os.system("afplay Error.mp3")
        else:
            i=i+1
    # if i == n:
    #     r = requests.post('http://localhost:9000/postorder',data={"name":"order1","price":100})
    #     print(r.text)
    #print(type(json))
if __name__ == "__main__":
    start()
