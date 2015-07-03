#!/usr/bin/env python2
# encoding=utf8
import os
import os.path
import sys
reload(sys)  
sys.setdefaultencoding('utf8')
sys.path.append(os.path.join(os.path.dirname(__file__), 'pyAIML/'))
import telebot
import time
from datetime import datetime 
import pyAIML
import atexit


TOKEN = os.environ['TELEGRAM_TOKEN']
AIMLName = "comperBot"
BootName = "belinda"
BRAINNAME = "brain.sav"

k = pyAIML.Kernel()
if os.path.isfile(BRAINNAME):
    k.loadBrain(BRAINNAME)
k.setTextEncoding("UTF-8")
k.learn(os.path.join(os.path.dirname(__file__), 'AIML/', AIMLName + "/") + "*.aiml")
k.loadSubs(os.path.join(os.path.dirname(__file__), 'AIML/', AIMLName + "/") + AIMLName+ ".ini")
k.setBotPredicate("bot_name", BootName)



atexit.register(lambda : k.saveBrain(BRAINNAME))

def listener(*messages):
    f = open('chat.log', 'a')
    """
    When new message get will call this function.
    :param messages:
    :return:
    """
    for m in messages:
        chatid = m.chat.id
        if m.content_type == 'text':
            text = m.text
            response = k.respond(text, chatid)
            tb.send_message(chatid, "Escribiste: " + text)
            tb.send_message(chatid, response)
            f.write(str(datetime.now()) + "\t Chat: " + str(chatid) + "\t Msg: " +  text + "\t Respuesta: " + response + "\n")


tb = telebot.TeleBot(TOKEN)
tb.get_update()  # cache exist message
tb.set_update_listener(listener) #register listener
tb.polling(3)
while True:
    time.sleep(2)
