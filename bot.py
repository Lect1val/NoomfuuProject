# Noomfuu Chatbot
# Import Library
import json
import os
from flask import Flask
from flask import request
from flask import make_response

#from sentimentmodel import useSentiment

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
    elif intent_group_question_str == "getUserID":
        answer_str = getUserID(data_from_dailogflow)
        return data_from_dailogflow
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

    if message_list is not None:
        messageID += 1
        messageID = str(messageID)
        db.collection('User').document(f'{userID}/message/{messageID}').set({
            u'messageID': messageID,
            u'content': user_problem,
            u'emotion': "",
            u'timestamp': firestore.SERVER_TIMESTAMP
        })
        pass
    elif message_list is None:
        messageID = "1"
        db.collection('User').document(f'{userID}/message/1').set({
            u'messageID': messageID,
            u'content': user_problem,
            u'emotion': "",
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

def getUserID(input_from_user):
    userID = input_from_user["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    #doc_ref = db.collection(u'User').document(userID).collection(u'message').order_by(u'messageID', direction=firestore.Query.DESCENDING).limit(1)
    #doc = doc_ref.get()
    doc_ref = []
    doc_ref = db.collection(u'User').document(userID).collection(u'message').order_by(u'messageid', direction=firestore.Query.DESCENDING).limit(1)
    user4 = []
    user4 = db.collection(u'User').document(f'user4').collection(u'message').order_by(u'messageid', direction=firestore.Query.DESCENDING).limit(1)
    for doc in doc_ref.stream():
        if not doc_ref is None:
            print(f'in for loop => {doc.to_dict()}\n')  
            id = doc.get('messageid')
            print(f'{id}\n')
        elif doc_ref is None:
            print("My message is empty\n")

        mlist = []
        mlist.append({
            u'messageid': doc.get('messageid'),
            u'content': doc.get('content'),
            u'emotion': doc.get('emotion'),
            u'timestamp': doc.get('timestamp')
        })
        print(f'm1 appended list = {mlist[0]}\n')

        m2list = []
        m2list.append(db.collection(u'User').document(userID).collection(u'message').order_by(u'messageid', direction=firestore.Query.DESCENDING).limit(1))
        print(f'm2 appended list = {m2list[0]}\n')


    for docc in user4.stream():
        print("test")
        m3list = []
        m3list.append({
            u'messageid': docc.get('messageid'),
            u'content': docc.get('content'),
            u'emotion': docc.get('emotion'),
            u'timestamp': docc.get('timestamp')
        })
        print(f'm1 appended list = {m3list[0]}\n')

    try:
        mlist
    except NameError:
        mlist = None

    try:
        m3list
    except NameError:
        m3list = None
    
    if mlist is None:
        print("mlist is empty\n")
    else:
        print(f'm1 appended list = {mlist[0]}\n')
    
    # if mlist is not None:
    #     print(f'm1 appended list = {mlist[0]} (is not)\n')
    # elif mlist is None:
    #     print("mlist is empty\n")
    
    if m3list is not None:
        print(f'm3 appended list = {m3list[0]} (is not)\n')
    elif m3list is None:
        print("mlist is empty\n")

    return "tested"



"""
def use_sentiment(word):
    answer_function = useSentiment(word)
    return answer_function
"""

if __name__ == '__main__':
    app.run()
    """
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
    """
