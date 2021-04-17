#Noomfuu Chatbot 
#Import Library
import json
import os
from flask import Flask
from flask import request
from flask import make_response

#----Firebase----
from random import randint
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("noomfuuproject-f3b69-firebase-adminsdk-mpbf0-0db0cba4ee.json")
firebase_admin.initialize_app(cred)
#-------------------------------------

# Flask
app = Flask(__name__)
@app.route('/', methods=['POST']) #Using post as a method
#@app.route('/')

def MainFunction():
    return "Noomfuu Hello"

#Flask
if __name__ == '__main__':
    app.run()
    """
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
    """
