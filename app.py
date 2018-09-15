# Python libraries that we need to import for our bot
from flask import Flask, request
from pymessenger.bot import Bot ## pymessenger is a Python wrapper for the Facebook Messenger API
import os

app = Flask(__name__) # This is how we create an instance of the Flask class for our app

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN'] # Replace 'VERIFY_TOKEN' with your verify token
bot = Bot(ACCESS_TOKEN) # Create an instance of the bot

q1 = "Question 1: answer a1"
a1 = "a1"
q2 = "Question 2: answer a2"
a2 = "a2"
q3 = "Question 3: answer a3"
a3 = "a3"
q4 = "Question 4: answer a4"
a4 = "a4"

vocabs = {
    q1: a1,
    q2: a2,
    q3: a3,
    q4: a4
}


def verify_fb_token(token_sent):
    # Verifies that the token sent by Facebook matches the token sent locally
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

# Chooses a message to send to the user
def send_question(q):
    return vocabs[q]

def correct_response(correct_count):
    correct_count += 1
    print(correct_count)
    return "Correct"

def incorrect_response():
    return "Incorrect"

@app.route("/webhook/", methods=['GET', 'POST'])
def start_quiz(recipient_id):
    correct_count = 0
    for q in vocabs:
        send_message(recipient_id, q)
        print("message sent")
        recipient_id, message = retrieve_id_and_message()
        if "quit" in message:
            break
        elif vocabs[q] in message:
            send_message(recipient_id, correct_response(correct_count))
        else:
            send_message(recipient_id, incorrect_response())

    send_message(recipient_id, correct_count)

# Send text message to recipient
def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response) # Sends the 'response' parameter to the user
    return "Message sent"

# This endpoint will receive messages

@app.route("/webhook/", methods=['GET', 'POST'])
def receive_message():
    print("receive_message function gets called")
    recipient_id, message = retrieve_id_and_message()
    print("id received: " + recipient_id)
    send_message(recipient_id, "Please send \'start quiz\' to begin.") # this gets called every time a message is sent

    # If user sends text
    recipient_id, message = retrieve_id_and_message()
    if "start quiz" in message:
        start_quiz(recipient_id)

    return "Message Processed"

@app.route("/webhook/", methods=['GET', 'POST'])
def retrieve_id_and_message():
    print("retrieve function gets called")
    # Handle GET requests
    if request.method == 'GET':
        print("GET request gets called")
        token_sent = request.args.get("hub.verify_token")  # Facebook requires a verify token when receiving messages
        return verify_fb_token(token_sent)

    # Handle POST requests
    else:
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

# Ensures that the below code is only evaluated when the file is executed, and ignored if the file is imported
if __name__ == "__main__":
    app.run() ## Runs application