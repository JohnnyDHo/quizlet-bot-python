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

correct_count = 0

def verify_fb_token(token_sent):
    # Verifies that the token sent by Facebook matches the token sent locally
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

# Chooses a message to send to the user
def send_question(q):
    return vocabs[q]

def correct_response():
    correct_count += 1
    print correct_count
    return "Correct"

def incorrect_response():
    return "Incorrect"

def start_quiz():
    for q in vocabs:
        send_message(recipient_id, q)
        if "quit" in message['message'].get('text').lower():
            break
        if vocabs[q] in message['message'].get('text').lower():
            return correct_response()
        else:
            return incorrect_response()

    send_message(recipient_id, correct_count)

# Send text message to recipient
def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response) # Sends the 'response' parameter to the user
    return "Message sent"

# This endpoint will receive messages


@app.route("/webhook/", methods=['GET', 'POST'])
def receive_message():
    print("MESSAGE RECEIVED")
    # Handle GET requests
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token") # Facebook requires a verify token when receiving messages
        return verify_fb_token(token_sent)

    # Handle POST requests
    else:
        output = request.get_json() # get whatever message a user sent the bot
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id'] # Facebook Messenger ID for user so we know where to send response back to
                    print("id received: " + recipient_id)
                send_message(recipient_id, "Please send \'start quiz\' to begin.")

                # If user sends text
                if "start quiz" in message['message'].get('text').lower():
                    start_quiz()


    return "Message Processed"

# Ensures that the below code is only evaluated when the file is executed, and ignored if the file is imported
if __name__ == "__main__":
    app.run() ## Runs application