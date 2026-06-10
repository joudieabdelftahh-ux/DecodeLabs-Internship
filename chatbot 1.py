
from http.client import responses
import random
import string



rules = [
 
  {"keywords": ["hello", "hi", "hey"], "responses": ["Hello! Welcome!"]},
  {"keywords": ["bye", "goodbye"],     "responses": ["Goodbye! See you!"]},
  {"keywords": ["joke", "funny"],      "responses": ["Why did the programmer quit..."]},
  {"keywords": ["name"], "responses": ["I am a ruleBased bot."]},
  {"keywords": ["how are you"], "responses": ["I'm good, and you?"]},
  {"keywords": ["what do you do"], "responses": ["I don't do much as this is a simple program."]}
]

# Empty input
def get_responses(user_input):
    if not user_input.strip():
        return "Please enter something."

#input cleaaning
def clean_input(user_input):
    return user_input.strip(), user_input.translate(str.maketrans('', '', string.punctuation))
#the brain
def get_response(user_input):
    lower = clean_input(user_input)

    # 1  match first
    for rule in rules:
        for keyword in rule["keywords"]:
            if keyword == lower:        
                return random.choice(rule["responses"])

    # 2 Keyword contained in input
    for rule in rules:
        for keyword in rule["keywords"]:
            if keyword in lower:
                return random.choice(rule["responses"])

    return "I don't understand that."

# Loop
while True:
    user_input = input("You: ")
    if clean_input(user_input) in ["bye", "exit", "quit", "goodbye"]:
        print("Bot: Goodbye!")
        break
    print("Bot:", get_response(user_input))