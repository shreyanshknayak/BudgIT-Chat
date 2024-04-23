from flask import Flask, render_template, request, jsonify
import os
from groq import Groq


from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

client = Groq(api_key = "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")

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    return get_Chat_response_better(input)


def get_Chat_response(text):
    # Let's chat for 5 lines
    for step in range(5):
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = tokenizer.encode(str(text) + tokenizer.eos_token, return_tensors='pt')

        # append the new user input tokens to the chat history
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

        # generated a response while limiting the total chat history to 1000 tokens, 
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

        # pretty print last ouput tokens from bot
        return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    

def get_Chat_response_better(text):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": text,
        },
        {
            "role":"system",
            "content":"You are a financial wizard/chatbot for an expense tracker app called BudgIT. Your name is Budget Buddy. You are the friendliest and the smartest financial advisor out there. Respond to the financial/budget handling queries from the user in a friendly manner."
        }
    ],
    model="mixtral-8x7b-32768",
    )
    return chat_completion.choices[0].message.content



if __name__ == '__main__':
    app.run()
