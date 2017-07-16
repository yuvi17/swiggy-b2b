from flask import *
from .SpeechRecognizer import *
from nltk import *
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
serverApp = Flask(__name__)
questions = ["Order for your restaurant,Two Large Cheese Burst Pizza , total amount Rupees 500","xyz"]
serverApp.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
train_set = open('app/train.csv',"r").read().splitlines()
train = [];

for t in train_set:
    s = (t.split(",")[0],t.split(",")[1])
    train.append(s)
cl = NaiveBayesClassifier(train)
recognizer = SpeechRecognizer()
@serverApp.route('/test')
def test():
    print(__file__)
    return "test response"

@serverApp.route("/getTextFromSpeech/<filename>")
def getTextFromSpeech(filename):
    print(filename)
    return recognizer.recognize_file(filename)

@serverApp.route("/request-speech/<phoneno>")
def requestSpeechApi(phoneno):
    session[phoneno] = 0
    print(len(questions))
    return "{0}".format(len(questions))

@serverApp.route("/processText/<text>")
def processText(text):
    response = cl.classify(text)
    print response
    if response == 'negative':
        questions[1] = "Thanks for partnering with us, we will come back with another order shortly."
    elif response == 'positive':
        questions[1] = "Rider named Sunny will reach you in 20 minutes .His number is 8 0 0 2 2 2 4 1 6 2. Thank You for partnering with us."
    
    return "success"

@serverApp.route("/fetchQuestion/<phoneno>/<index>")
def fetchQuestion(phoneno,index):
    if(int(index) < len(questions)):
        return questions[int(index)]
    return "placed your order"
