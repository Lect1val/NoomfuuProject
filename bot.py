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

db = firestore.client()

# Flask
app = Flask(__name__)
@app.route('/', methods=['POST']) #Using post as a method
# @app.route('/')


def MainFunction():

    #Getting intent from Dailogflow
    question_from_dailogflow_raw = request.get_json(silent=True, force=True)
    user_text = question_from_dailogflow_raw["queryResult"]

    #Call generating_answer function to classify the question
    answer_from_bot = generating_answer(question_from_dailogflow_raw)
    
    #Make a respond back to Dailogflow
    r = make_response(answer_from_bot)
    r.headers['Content-Type'] = 'application/json' #Setting Content Type

    #return r
    return user_text

def generating_answer(question_from_dailogflow_dict):
    
    #Print intent that recived from dialogflow.
    print(json.dumps(question_from_dailogflow_dict, indent=4 ,ensure_ascii=False))

    #Getting intent name form intent that recived from dialogflow.
    intent_group_question_str = question_from_dailogflow_dict["queryResult"]["intent"]["displayName"] 
    print(intent_group_question_str)
    #Select function for answering question
    if intent_group_question_str == "NegativeEmotion - yes - want - problem":
        # answer_str = "นุ่มฟูเข้าใจว่าคุณคงเหนื่อยมากใช่ไหม แต่ไม่เป็นไรนะ พักบ้างก็ได้ นุ่มฟูเป็นกำลังใจให้นะ"
        # print(answer_str)
        answer_str = follow_up_NegativeEmotion_problem(question_from_dailogflow_dict)
    else: answer_str = "นุ่มฟูไม่เข้าใจ"

    print(intent_group_question_str)
    #Build answer dict 
    answer_from_bot = {"fulfillmentText": answer_str}
    
    #Convert dict to JSON   
    answer_from_bot = json.dumps(answer_from_bot, indent=4) 
    
    return answer_from_bot

def follow_up_NegativeEmotion_problem(input_from_user):
    user_problem = input_from_user["queryResult"]["queryText"]
    userID = input_from_user["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    db.collection('User').document(f'{userID}/message/problem').set({
        u'content' : {user_problem}
    })
    function_answer = "นุ่มฟูเข้าใจว่าคุณคงเหนื่อยมากใช่ไหม แต่ไม่เป็นไรนะ พักบ้างก็ได้ นุ่มฟูเป็นกำลังใจให้นะ"
    return function_answer



#Flask
if __name__ == '__main__':
    app.run()
    """
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
    """
