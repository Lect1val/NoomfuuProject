# Noomfuu Chatbot
# Import Library
import json
import os
from flask import Flask
from flask import request
from flask import make_response
import UseSentiment

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

    # Call generating_answer function to classify the question
    answer_from_bot = generating_answer(data_from_dailogflow_raw)

    # Make a respond back to Dailogflow
    r = make_response(answer_from_bot)
    r.headers['Content-Type'] = 'application/json'  # Setting Content Type

    return r

def generating_answer(data_from_dailogflow):

    # Print intent that recived from dialogflow.
    print(json.dumps(data_from_dailogflow, indent=4, ensure_ascii=False))

    # Getting intent name form intent that recived from dialogflow.
    intent_group_question_str = data_from_dailogflow["queryResult"]["intent"]["displayName"]

    # Select function for answering question
    if intent_group_question_str == "NegativeEmotion - yes - want - problem":
        answer_str = NegativeEmotion_problem(data_from_dailogflow)
        return data_from_dailogflow
    elif intent_group_question_str == "Default Welcome Intent":
        answer_str = Default_Welcome_Intent(data_from_dailogflow)
        return data_from_dailogflow
    elif intent_group_question_str == "addJournal.content":
        answer_str = add_journal(data_from_dailogflow)
    else: answer_str = "นุ่มฟูไม่เข้าใจ"

    # Build answer dict
    answer_from_bot = {"fulfillmentText": answer_str}
    
    # Convert dict to JSON
    answer_from_bot = json.dumps(answer_from_bot, indent=4)

    return answer_from_bot

def NegativeEmotion_problem(input_from_user):
    user_problem = input_from_user["queryResult"]["queryText"]
    userID = input_from_user["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    messages = []
    messages = db.collection(u'User').document(userID).collection(u'message').order_by(u'messageID', direction=firestore.Query.DESCENDING).limit(1)
    for doc in messages.stream():
        message_list = []
        messageID = int(doc.get('messageID'))
        message_list.append({
            u'messageid': doc.get('messageID'),
            u'content': doc.get('content'),
            u'emotion': doc.get('emotion'),
            u'timestamp': doc.get('timestamp')
        }) 
    
    try:
        message_list
    except NameError:
        message_list = None

    analyzed_word = str(UseSentiment.useSentiment(str(user_problem)))
    if analyzed_word == "pos":
        emotion = "1"
    elif analyzed_word == "neg":
        emotion = "-1"

    if message_list is not None:
        messageID += 1
        messageID = str(messageID)
        db.collection('User').document(f'{userID}/message/{messageID}').set({
            u'messageID': messageID,
            u'content': user_problem,
            u'emotion': emotion,
            u'timestamp': firestore.SERVER_TIMESTAMP
        })
        pass
    elif message_list is None:
        messageID = "1"
        db.collection('User').document(f'{userID}/message/1').set({
            u'messageID': messageID,
            u'content': user_problem,
            u'emotion': emotion,
            u'timestamp': firestore.SERVER_TIMESTAMP
        })
        pass
    
def Default_Welcome_Intent(input_from_user):
    userID = input_from_user["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    if is_user_exist(userID):
        pass
    else:
        initial_user_information(input_from_user)
        pass

def initial_user_information(input_from_user):
    userID = input_from_user["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    db.collection('User').document(f'{userID}').set({
        u'userID': userID,
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

def add_journal(input_from_user):
    user_journal = input_from_user["queryResult"]["queryText"]
    userID = input_from_user["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    journals = []
    journals = db.collection(u'User').document(userID).collection(u'journal').order_by(u'journalID', direction=firestore.Query.DESCENDING).limit(1)
    for doc in journals.stream():
        journal_list = []
        journalID = int(doc.get('journalID'))
        journal_list.append({
            u'messageid': doc.get('journalID'),
            u'content': doc.get('content'),
            u'emotion': doc.get('emotion'),
            u'timestamp': doc.get('timestamp')
        }) 
    
    try:
        journal_list
    except NameError:
        journal_list = None

    analyzed_word = str(UseSentiment.useSentiment(str(user_journal)))
    if analyzed_word == "pos":
        emotion = "1"
        answer_str = "นุ่มฟูบันทึกเรื่องดีๆอันนี้ไว้แล้วนะคะ วันไหนที่รู้สึกไม่ดีก็อย่าลืมกดเมนูด้านล่างเข้ามาดูได้นะ"
    elif analyzed_word == "neg":
        emotion = "-1"
        answer_str = "ดูเหมือนจะไม่ใช่เรื่องดีเท่าไรเลย ไม่เป็นไรนะคะ สักวันหนึ่งต้องมีเรื่องดี ๆ เกิดขึ้นแน่นอน"

    if journal_list is not None:
        journalID += 1
        journalID = str(journalID)
        db.collection('User').document(f'{userID}/journal/{journalID}').set({
            u'journalID': journalID,
            u'content': user_journal,
            u'emotion': emotion,
            u'timestamp': firestore.SERVER_TIMESTAMP
        })
        return answer_str
    elif journal_list is None:
        journalID = "1"
        db.collection('User').document(f'{userID}/journal/1').set({
            u'journalID': journalID,
            u'content': user_journal,
            u'emotion': emotion,
            u'timestamp': firestore.SERVER_TIMESTAMP
        })
        return answer_str

if __name__ == '__main__':
    app.run()
    """
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
    """
