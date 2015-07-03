#!/usr/bin/env python2
# encoding=utf8
"""
start imports
"""


"""
General utils imports
"""
import os
import os.path
import atexit
import sys
reload(sys) 

"""
Time Managmente imports
"""
import time
from datetime import datetime 
 

"""
set aditional path
"""
sys.path.append(os.path.join(os.path.dirname(__file__), 'pyAIML/'))

"""
import bot specific code
"""
import pyAIML
import telebot



"""
set General Options
"""

"""
Set Sys Options
Can't modify
"""
sys.setdefaultencoding('utf8')

"""
Set Boot options
you can modify
"""
TOKEN = os.environ['TELEGRAM_TOKEN']
AIMLName = "comperBot"
BootName = "belinda"
BRAINNAME = "brain.sav"


"""
code core
"""

"""
Set Aiml Brain, 
recovery if exist, fetch new predicates and set Data
"""
k = pyAIML.Kernel()
if os.path.isfile(BRAINNAME):
    k.loadBrain(BRAINNAME)
k.setTextEncoding("UTF-8")
k.learn(os.path.join(os.path.dirname(__file__), 'AIML/', AIMLName + "/") + "*.aiml")
k.loadSubs(os.path.join(os.path.dirname(__file__), 'AIML/', AIMLName + "/") + AIMLName+ ".ini")
k.setBotPredicate("bot_name", BootName)

"""
create trigger for saving the brian status
"""
atexit.register(lambda : k.saveBrain(BRAINNAME))

"""
Define listener
"""
def listener(*messages):
    """
    When new message get will call this function.
    :param messages:
    :return:
    """
    f = open('chat.log', 'a')
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
