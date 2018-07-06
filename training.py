# -*- coding: utf-8 -*-
#!/usr/bin/python3
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
import logging
# Enable info level logging
logging.basicConfig(level=logging.ERROR)
# Train the chat bot using the ChatterBot Corpus of conversation dialog
chatbot = ChatBot("TourismBot")

chatbot.set_trainer(ChatterBotCorpusTrainer)
chatbot.train("chatterbot.corpus.malayalam")	# Start by training our bot with the ChatterBot corpus data

