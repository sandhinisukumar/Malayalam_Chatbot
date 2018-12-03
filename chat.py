# -*- coding: utf-8 -*-
#!/usr/bin/python3
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from chatterbot import ChatBot
from flask import Flask, render_template, request
from chatterbot.input import InputAdapter
from chatterbot.output import OutputAdapter
from chatterbot.comparisons import levenshtein_distance
app = Flask(__name__)
# to enable verbose logging
import logging
# logging.basicConfig(level=logging.INFO) 
# Create a new instance of a ChatBot
chatbot = ChatBot(
        "TourismBot",  # These are the adapters that are required to build a chatbot
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    output_adapter='chatterbot.output.OutputAdapter',
        output_format="text",   # The output format is "text"
    statement_comparison_function=levenshtein_distance,    # The sentence comparison is calculated by using Levenshtein distance function
    # These are the logic adapters that are required for normal operation        
    logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch' 
            },
            {
                'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                'threshold': 0.5,                
                'default_response': 'വെരെ ഏതെങ്കിലും അറിയാനുണ്ടോ?'
            }
    ],
    
      
    )
@app.route("/")
def home():
    return render_template("index3.html")
@app.route("/get")
def get_bot_response():
    while True:        # The following loop will execute each time the user enters input
        try:
            response = request.args.get('msg')
            return str(chatbot.get_response(response))        # Select a response to the input statement


        except(KeyboardInterrupt, EOFError, SystemExit):        # Press ctrl-c or ctrl-d on the keyboard to exit
            print('\nനന്ദി!\n')
            break
if __name__ == "__main__":
    app.run()
