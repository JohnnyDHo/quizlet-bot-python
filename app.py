## Python libraries that we need to import for our bot
from flask import Flask, request
from pymessenger.bot import Bot  ## pymessenger is a Python wrapper for the Facebook Messenger API
import os

questions = ["q1", "q2"]
answers = ["a1", "a2"]
users_history_database = {}

app = Flask(__name__)  ## This is how we create an instance of the Flask class for our app

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']  ## Replace 'VERIFY_TOKEN' with your verify token
bot = Bot(ACCESS_TOKEN)  ## Create an instance of the bot

## Ensures that the below code is only evaluated when the file is executed, and ignored if the file is imported
if __name__ == "__main__":
    app.run()  ## Runs application


def verify_fb_token(token_sent):
    ## Verifies that the token sent by Facebook matches the token sent locally
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


## Send text message to recipient
def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)  ## Sends the 'response' parameter to the user
    return "Message sent"


## This endpoint will receive messages
@app.route("/webhook/", methods=['GET', 'POST'])
def receive_message():
    global questions, answers, users_history_database

    print("MESSAGE RECEIVED")
    ## Handle GET requests
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")  ## Facebook requires a verify token when receiving messages
        return verify_fb_token(token_sent)

    ## Handle POST requests
    else:
        output = request.get_json()  ## get whatever message a user sent the bot
        print("retrieve message")
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    message = message['message'].get('text').lower()

                    if recipient_id not in users_history_database:
                        users_history_database[recipient_id] = Quiz(questions, answers)
                        print("id not existss")

                    else:
                        print("id already exists")

                    print(recipient_id)
                    print(type(users_history_database[recipient_id]))

                    print("i'm here")
                    run_program(recipient_id, message)




    # response_sent_text = get_message_text(message)
    # send_message(recipient_id, response_sent_text)

    return "Message Processed"


def run_program(id, message):
    global users_history_database
    print("program running!!!!!")

    if 'start quiz' in message:
        print("quiz starting now")
        send_message(id, users_history_database[id].start_quiz())

    elif users_history_database[id].onGoing():
        print("quiz ongoing")
        if "end quiz" in message:
            print("end quiz")
            send_message(id, users_history_database[id].end_quiz())
        else:
            print("checking & sending another question")
            send_message(id, users_history_database[id].check_answer())
            send_message(id, users_history_database[id].get_question())

    else:
        print("not correct input")
        send_message(id, "input not correct")




'''
## Retreving the user id and message (used at the beginning)
def retrieve_id_and_message(output):
    print("retrieve message")
    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id']
                message_script = message['message'].get('text').lower()
                return recipient_id, message_script
'''

## Retreiving the file (used in the modules)
def retrieve_file():
    output = request.get_json()  ## get whatever message a user sent the bot
    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                if message['message'].get('attachments'):
                    for att in message['message'].get('attachments'):
                        print (type(att))
                else:
                    print ("Sorry!")


## Reading quiz files
def read_file(f):
    file = f.readlines()
    for index in range(0, len(file) - 1):
        file[index] = file[index][:len(file[index]) - 1]
        print (file[index])

    questions = []
    answers = []

    for question_index in range(0, len(file), 2):
        answers.append(file[question_index])
    for answer_index in range(1, len(file), 2):
        answers.append(file[answer_index])

    return questions, answers


class Quiz():
    def __init__(self, questions, answers):
        self.questions = questions
        self.answers = answers

        self.quiz_history = []
        self.total_accuracy = 0.0
        self.num_quizzes = 0

        self.question_index = -1
        self.num_correct = 0
        self.num_asked = 0

        self.ongoing = False

    def start_quiz(self):
        print ("quiz started")
        self.question_index = -1
        self.num_correct = 0
        self.num_asked = 0
        self.ongoing = True
        return self.get_question()

    def end_quiz(self):
        # Terminate the quiz
        self.update_history()

        self.question_index = -1
        self.num_correct = 0
        self.num_asked = 0

        self.num_quizzes += 1
        return "Quiz ended."

    def update_history(self):

        current_accuracy = self.num_correct / float(self.num_asked)
        self.quiz_history.append([self.num_correct, self.num_asked, current_accuracy])
        self.total_accuracy = (self.total_accuracy * self.num_quizzes + current_accuracy) / (self.num_quizzes + 1)

    def get_question(self):
        self.question_index += 1
        return self.questions[self.question_index]

    def check_answer(self, message):
        if message == self.answers[self.question_index]:
            self.num_correct += 1
            self.num_asked += 1
            return "Correct!"
        else:
            self.num_asked += 1
            return "Incorrect"

    def onGoing(self):
        return self.ongoing

    def print_history(self):
        print (self.quiz_history)
