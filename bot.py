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
    doc_ref = db.collection(u'User').document(f'{userID}').collection(u'message').order_by(u'messageID', direction=firestore.Query.DESCENDING).limit(1)
    recentMessage = doc_ref.get()
    """
    if recentMessage.exists:
        recentMessageID = doc_ref.get("messageid")
        messageID = recentMessageID + 1
        db.collection('User').document(f'{userID}/message/{messageID}').set({
            u'messageid': {messageID},
            u'content': {user_problem},
            u'emotion': "",
            u'timestamp': firestore.SERVER_TIMESTAMP
    })
    elif:
        messageID = 1
        db.collection('User').document(f'{userID}/message/1').set({
            u'messageid': {messageID},
            u'content': {user_problem},
            u'emotion': "",
            u'timestamp': firestore.SERVER_TIMESTAMP
    })
    """
    messageID = "1"
    db.collection('User').document(f'{userID}/message/1').set({
        u'messageid': messageID,
        u'content': user_problem,
        u'emotion': "",
        u'timestamp': firestore.SERVER_TIMESTAMP
    })
    return input_from_user


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

# def getUserID(input_from_user):
#     userID = input_from_user["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
#     """
#     doc_ref = db.collection(u'User').document(f'{userID}').collection(u'message')
#     query = doc_ref.order_by(u'messageID', direction=firestore.Query.DESCENDING).limit(1)
#     result = query.get()
#     print(result)
#     """
#     #doc_ref = db.collection(u'User').document(userID).collection(u'message').order_by(u'messageID', direction=firestore.Query.DESCENDING).limit(1)
#     #doc = doc_ref.get()

#     doc_ref = db.collection(u'User').document(userID).collection(u'message').order_by(u'messageid', direction=firestore.Query.DESCENDING).limit(1)
#     messsages = []
#     for doc in doc_ref.stream():
#         print(f'in for loop => {doc.to_dict()}\n')
#         print(f'messageID = {doc.messageid}')
#         #messsages.append()
    
#     #print(messsages[0])


#     """
#     collections = db.collection('User').document('user2').collections()
#     for collection in collections:
#         for doc in collection.stream():
#             print(f'{doc.id} => {doc.to_dict()}')
#     """

#     """
#     if doc.exists:
#         print(f'Document data: {doc.to_dict()}')
#     else:
#         print(u'No such document!')
#     """
#     return "tested"



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
