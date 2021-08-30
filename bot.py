# Noomfuu Chatbot
# Import Library
import json
import os
from flask import Flask
from flask import request
from flask import make_response

from sentimentmodel import useSentiment

# ----Firebase----
from random import randint
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate(
    "noomfuuproject-f3b69-firebase-adminsdk-mpbf0-0db0cba4ee.json")
firebase_admin.initialize_app(cred)
# -------------------------------------

db = firestore.client()

# Flask
app = Flask(__name__)


@app.route('/', methods=['POST'])  # Using post as a method
# @app.route('/')
def MainFunction():

    # Getting intent from Dailogflow
    data_from_dailogflow_raw = request.get_json(silent=True, force=True)
    #user_text = data_from_dailogflow_raw["queryResult"]

    # Call generating_answer function to classify the question
    answer_from_bot = generating_answer(data_from_dailogflow_raw)

    # Make a respond back to Dailogflow
    r = make_response(answer_from_bot)
    r.headers['Content-Type'] = 'application/json'  # Setting Content Type

    return r
    # return user_text

#
def generating_answer(data_from_dailogflow):

    # Print intent that recived from dialogflow.
    print(json.dumps(data_from_dailogflow, indent=4, ensure_ascii=False))

    # Getting intent name form intent that recived from dialogflow.
    intent_group_question_str = data_from_dailogflow["queryResult"]["intent"]["displayName"]

    # Select function for answering question
    if intent_group_question_str == "NegativeEmotion.yes.want.problem":
        answer_str = NegativeEmotion_problem(data_from_dailogflow)
    if intent_group_question_str == "Default Welcome Intent":
        answer_str = Default_Welcome_Intent(data_from_dailogflow)
    else:
        answer_str = "นุ่มฟูไม่เข้าใจ"

    # Build answer dict
    answer_from_bot = {"fulfillmentText": answer_str}

    # Convert dict to JSON
    answer_from_bot = json.dumps(answer_from_bot, indent=4)

    return answer_from_bot


def NegativeEmotion_problem(input_from_user):
    user_problem = input_from_user["queryResult"]["queryText"]
    userID = input_from_user["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    db.collection('User').document(f'{userID}/message/problem').set({
        u'content': {user_problem}
    })
    function_answer = "เราเข้าใจความรู้สึกของเธอนะ ไม่เป็นไรนะ ลองถอยออกมาจากสิ่งที่ทำให้เครียดบ้าง เป็นกำลังใจให้เสมอนะ"
    return function_answer

def Default_Welcome_Intent(input_from_user):
    userID = input_from_user["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    function_answer = ""
    if is_user_exist(userID):
        return function_answer
    else:
        initial_user_information(input_from_user)
        return function_answer

def initial_user_information(input_from_user):
    userID = input_from_user["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    db.collection('User').document(f'{userID}').set({
        u'lineName': "",
        u'firstName': "", 
        u'lastName': "",
        u'nickName': "",
        u'Email': "",
        u'TelNo': "",
        u'contactNote': ""
    })
    pass

def is_user_exist(userID): 
    doc_ref = db.collection(u'User').document(userID)
    doc = doc_ref.get()
    exist = False
    if doc.exists:
        exist = True
    else:
        exist = False
    return exist

def use_sentiment(word):
    answer_function = useSentiment(word)
    return answer_function

# Flask

# @app.route('/assessment')
# def index():
#     return render_template('LIFF/assessment2Q.html')


if __name__ == '__main__':
    app.run()
    """
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
    """
