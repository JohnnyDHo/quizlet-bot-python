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
q5 = "Question 5: answer a5"
a5 = "a5"

questions = [q1, q2, q3, q4, q5]
answers = [a1, a2, a3, a4, a5]
state = "None"
correct_count = 0
q_index = 0

def verify_fb_token(token_sent):
    # Verifies that the token sent by Facebook matches the token sent locally
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

# Chooses a message to send to the user
def correct_response():
    global correct_count
    correct_count += 1
    return "Correct."

def incorrect_response():
    return "Incorrect."

def run_program(recipient_id, message):
    global state, q_index, correct_count
    if message == "start quiz":
        q_index = 0
        state = "quiz"
        send_message(recipient_id, questions[q_index])
    elif state == "quiz":
        if "end quiz" in message:
            state = "done quiz"
            send_message(recipient_id, "Your quiz has been terminated. Send \"Get Result\" to see your result.")
        else:
            if message == answers[q_index]:
                send_message(recipient_id, correct_response())
            else:
                send_message(recipient_id, "You response is " + message + ". The correct answer is " + answers[q_index])

            q_index += 1

            if q_index > len(questions) - 1:
                state = "done quiz"
                send_message(recipient_id, "You've reached the end of the quiz.")
                send_message(recipient_id, "Send \"Get Result\" to see your result.")
            else:
                send_message(recipient_id, questions[q_index])

    elif message == "get result":
        q_index = 0
        send_message(recipient_id, "Your got " + correct_count + "/" + str(len(questions)) + " correct.")
    else:
        send_message(recipient_id, "Send \"start quiz\" to start quiz")

# Send text message to recipient
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
        print("GET request gets called")
        token_sent = request.args.get("hub.verify_token")  # Facebook requires a verify token when receiving messages
        return verify_fb_token(token_sent)

    # Handle POST requests
    else:
        recipient_id, message = retrieve_id_and_message()

        run_program(recipient_id, message)

        return "Message Processed"

# Ensures that the below code is only evaluated when the file is executed, and ignored if the file is imported
if __name__ == "__main__":
    app.run() ## Runs application