# Python libraries that we need to import for our bot
from flask import Flask, request
from pymessenger.bot import Bot ## pymessenger is a Python wrapper for the Facebook Messenger API
import os

app = Flask(__name__) # This is how we create an instance of the Flask class for our app

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN'] # Replace 'VERIFY_TOKEN' with your verify token
bot = Bot(ACCESS_TOKEN) # Create an instance of the bot

# ======================== Don't mess with the stuff Above!!! ========================


q1 = "Question 1: answer a1"
a1 = "a1"
q2 = "Question 2: answer a2"
a2 = "a2"
q3 = "Question 3: answer a3"
a3 = "a3"
q4 = "Question 4: answer a4"
a4 = "a4"
q5 = "Question 5: answer a5"
a5 = "a5"

questions = [q1, q2, q3, q4, q5]
answers = [a1, a2, a3, a4, a5]

# state = "None"
# correct_count = 0
# q_index = 0

users = {
    # recipient-id : [state, correct_count, q_index]
}

# Chooses a message to send to the user
def correct_response(recipient_id):
    global users
    users[recipient_id]["correct_count"] += 1
    return "Correct."

def run_program(recipient_id, message):
    global users, questions, answers

    if recipient_id not in users:
        users[recipient_id] = {}
        users[recipient_id]["state"] = "None"
        users[recipient_id]["correct_count"] = 0
        users[recipient_id]["q_index"] = 0
        send_message(recipient_id, "Hi, there. Your user ID is: " + str(recipient_id))
        print(str(users))

    if users[recipient_id]["state"] == "None":
        if message == "start quiz":
            users[recipient_id]["state"] = "start quiz"
            print(str(users))
            send_message(recipient_id, questions[users[recipient_id]["q_index"]])
        else:
            send_message(recipient_id, "Send \"start quiz\" to start quiz")

    elif users[recipient_id]["state"] == "start quiz":
        if "end quiz" in message:
            users[recipient_id]["state"] = "done quiz"
            users[recipient_id]["q_index"] = 0
            send_message(recipient_id, "Your quiz has been terminated. Send \"Get Result\" to see your result.")
        else:
            if message == answers[users[recipient_id]["q_index"]]:
                send_message(recipient_id, correct_response())
            else:
                send_message(recipient_id, "You response is " + message + ". The correct answer is " + answers[users[recipient_id]["q_index"]])

            users[recipient_id]["q_index"] += 1

            if users[recipient_id]["q_index"] > len(questions) - 1:
                users[recipient_id]["state"] = "done quiz"
                users[recipient_id]["q_index"] = 0
                send_message(recipient_id, "You've reached the end of the quiz.")
                send_message(recipient_id, "Send \"Get Result\" to see your result.")
            else:
                send_message(recipient_id, questions[users[recipient_id]["q_index"]])

    elif users[recipient_id]["state"] == "done quiz" and message == "get result":
        send_message(recipient_id, "Your got " + str(users[recipient_id]["correct_count"]) + "/" + str(len(questions)) + " correct.")




# ======================== Don't mess with the stuff below!!! ========================

def verify_fb_token(token_sent):
    # Verifies that the token sent by Facebook matches the token sent locally
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response) # Sends the 'response' parameter to the user
    return "Message sent"

def retrieve_id_and_message():
    print("retrieve function gets called")
    recipient_id = ""
    message = ""
    output = request.get_json()  # get whatever message a user sent the bot
    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id']
                message = message['message'].get('text').lower()
    return recipient_id, message

# This endpoint will receive messages
@app.route("/webhook/", methods=['GET', 'POST'])
def receive_message():
    # Handle GET requests
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")  # Facebook requires a verify token when receiving messages
        return verify_fb_token(token_sent)

    # Handle POST requests
    else:
        recipient_id, message = retrieve_id_and_message()
        if recipient_id != "":
            run_program(recipient_id, message)
        return "Message Processed"

# Ensures that the below code is only evaluated when the file is executed, and ignored if the file is imported
if __name__ == "__main__":
    app.run() ## Runs application