from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

client = Groq(api_key = "API_KEY")


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    return get_Chat_response_better(input)
    

def get_Chat_response_better(text):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": text,
        },
        {
            "role":"system",
            "content":"You are a financial wizard/chatbot for an expense tracker app called SpendStream. Your name is BudgIT, the Budget Buddy. You are the friendliest and the smartest financial advisor out there. Respond to the financial/budget handling queries from the user in a friendly manner.Only introducd yourself one time in a conversation, do not introduce yourself with every message"
        }
    ],
    model="mixtral-8x7b-32768",
    )
    return chat_completion.choices[0].message.content



if __name__ == '__main__':
    app.run()
