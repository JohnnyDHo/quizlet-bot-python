# Python libraries that we need to import for our bot
from flask import Flask, request
from pymessenger.bot import Bot ## pymessenger is a Python wrapper for the Facebook Messenger API
import os

app = Flask(__name__) # This is how we create an instance of the Flask class for our app

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN'] # Replace 'VERIFY_TOKEN' with your verify token
bot = Bot(ACCESS_TOKEN) # Create an instance of the bot

quiz_ongoing = None

q1 = "q1"
a1 = "a1"
q2 = "q2"
a2 = "a2"

vocabs = {
    q1: a1,
    q2: a2
}

def verify_fb_token(token_sent):
    # Verifies that the token sent by Facebook matches the token sent locally
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

# Chooses a message to send to the user
def send_question(q):
    return vocabs[q]

def correct_response():
    return "Correct"

def incorrect_response():
    return "Incorrect"

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

                # If user sends text
                if vocabs[q1] in message['message'].get('text').lower():
                    response_sent_text = q1
                    send_message(recipient_id, response_sent_text)
                elif vocabs[q2] in message['message'].get('text').lower():
                    response_sent_text = q2
                    send_message(recipient_id, response_sent_text)

    return "Message Processed"

# Ensures that the below code is only evaluated when the file is executed, and ignored if the file is imported
if __name__ == "__main__":
    app.run() ## Runs application