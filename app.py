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
def get_message_text(message):
    return "Hi HackRice TeamMMMMMMMMMM"

## Send text message to recipient
def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response) ## Sends the 'response' parameter to the user
    return "Message sent"

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
       recipient_id, message = retrieve_id_and_message(output)
       response_sent_text = get_message_text(message)
       send_message(recipient_id, response_sent_text)
       '''
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id'] ## Facebook Messenger ID for user so we know where to send response back to

                ## retrieving the user message and logging it
                message_script = message['message'].get('text').lower()

                ## getting the response message and logging it
                response_sent_text = get_message_text(message_script)

                ## send the message
                send_message(recipient_id, response_sent_text)
        '''

    return "Message Processed"

## Retreving the user id and message
def retrieve_id_and_message(output):
    for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id']
                message_script = message['message'].get('text').lower()

                return recipient_id, message_script

## Ensures that the below code is only evaluated when the file is executed, and ignored if the file is imported
if __name__ == "__main__":
    app.run() ## Runs application