#!/usr/bin/env python2
import os
import sys
import telebot
import time
from datetime import datetime 

TOKEN = os.environ['TELEGRAM_TOKEN']


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
            tb.send_message(chatid, text)
            f.write(str(datetime.now()) + "\|Chat: " + str(chatid) + "\|Msg: " +  text + "\|\n")


tb = telebot.TeleBot(TOKEN)
tb.get_update()  # cache exist message
tb.set_update_listener(listener) #register listener
tb.polling(3)
while True:
    time.sleep(2)
