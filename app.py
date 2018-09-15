## Python libraries that we need to import for our bot
from flask import Flask, request
from pymessenger.bot import Bot ## pymessenger is a Python wrapper for the Facebook Messenger API
import os

app = Flask(__name__) ## This is how we create an instance of the Flask class for our app

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN'] ## Replace 'VERIFY_TOKEN' with your verify token
bot = Bot(ACCESS_TOKEN) ## Create an instance of the bot

def verify_fb_token(token_sent):
    ## Verifies that the token sent by Facebook matches the token sent locally
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

# Chooses a message to send to the user
import random
def get_message_text():
    return "Hi HackRice Team"
def quiztext():
    answer = ["dog", "cat", "giraffe"]
    question = ["mans best friend", "says meow", "long neck"]
        return random.choice(answer)

## Send text message to recipient
def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response) ## Sends the 'response' parameter to the user
    return "Message sent"
def quiztext():
    question = ["mans best friend", "says meow", "long neck"]
    for q1 in question:
        return q1



## This endpoint will receive messages
@app.route("/webhook/", methods=['GET', 'POST'])
def receive_message():
    print("MESSAGE RECEIVED")
    ## Handle GET requests
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token") ## Facebook requires a verify token when receiving messages
        return verify_fb_token(token_sent)

    ## Handle POST requests
    else:
       output = request.get_json() ## get whatever message a user sent the bot
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id'] ## Facebook Messenger ID for user so we know where to send response back to

                ## If user sends text
                if "hackrice" in message['message'].get('text').lower():
                    response_sent_text = get_message_text()
                    send_message(recipient_id, response_sent_text)
                elif "hi" in message['message'].get('text').lower():
                    send_message(recipient_id, "Hi! Welcome to Quizlet-Bot! To pick a quiz send: 'quiz' To check history send: 'history' To upload your own quiz send: 'file'")
                elif "quiz" in message['message'].get('text').lower():
                    quiz1 = quiztext()
                    send_message(recipient_id, quiz1)
                    if "dog" in message['message'].get('text').lower():
                        send_message(recipient_id, "correct")

    return "Message Processed"

## Ensures that the below code is only evaluated when the file is executed, and ignored if the file is imported
if __name__ == "__main__":
    app.run() ## Runs application