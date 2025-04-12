# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from wxpy import *
from requests import get
from requests import post
from platform import system
from os import chdir
from random import choice
from threading import Thread
import configparser
import time
import sys

# Function to get daily motivational quotes
def get_message():
    r = get("http://open.iciba.com/dsapi/")
    note = r.json()['note']
    content = r.json()['content']
    return note, content

# Function to send a message to the girlfriend
def send_message(your_message):
    try:
        # Find the girlfriend's WeChat contact by name
        my_friend = bot.friends().search(my_lady_wechat_name)[0]

        # Send the message to the girlfriend
        my_friend.send(your_message)
    except:
        # If an error occurs, send a message to the file transfer assistant
        bot.file_helper.send(u"Error in sending message to girlfriend, check the issue!")

# Function to send messages at specified times of the day
def start_care():
    # Initialize the message variable
    message = ""

    # Infinite loop to continuously check and send messages
    while True:
        # Print the current time to indicate the script is running
        print("Monitoring, time: %s" % time.ctime())

        # Get the current time in HH:MM format
        now_time = time.ctime()[-13:-8]

        # Send morning greeting message
        if now_time == say_good_morning:
            message = choice(str_list_good_morning)
            if flag_wx_emoj:
                message += choice(str_list_emoj)
            send_message(message)
            print("Sent morning greeting to girlfriend: %s" % time.ctime())

        # Send lunch greeting message
        elif now_time == say_good_lunch:
            message = choice(str_list_good_lunch)
            if flag_wx_emoj:
                message += choice(str_list_emoj)
            send_message(message)
            print("Sent lunch greeting to girlfriend: %s" % time.ctime())

        # Send dinner greeting message
        elif now_time == say_good_dinner:
            message = choice(str_list_good_dinner)
            if flag_wx_emoj:
                message += choice(str_list_emoj)
            send_message(message)
            print("Sent dinner greeting to girlfriend: %s" % time.ctime())

        # Send bedtime greeting message
        elif now_time == say_good_dream:
            if flag_learn_english:
                note, content = get_message()
                message = choice(str_list_good_dream) + "\n\n" + "Let's learn English together:\n" + "Original: " + content + "\n\nTranslation: " + note
            else:
                message = choice(str_list_good_dream)
            if flag_wx_emoj:
                message += choice(str_list_emoj)
            send_message(message)
            print("Sent bedtime greeting to girlfriend: %s" % time.ctime())

        # Send festival greetings
        festival_month = time.strftime('%m', time.localtime())
        festival_day = time.strftime('%d', time.localtime())

        if festival_month == '02' and festival_day == '14' and now_time == "08:00":
            send_message(str_Valentine)
            print("Sent Valentine's Day wishes to girlfriend: %s" % time.ctime())

        elif festival_month == '03' and festival_day == '08' and now_time == "08:00":
            send_message(str_Women)
            print("Sent Women's Day wishes to girlfriend: %s" % time.ctime())

        elif festival_month == '12' and festival_day == '24' and now_time == "00:00":
            send_message(str_Christmas_Eve)
            print("Sent Christmas Eve wishes to girlfriend: %s" % time.ctime())

        elif festival_month == '12' and festival_day == '25' and now_time == "00:00":
            send_message(str_Christmas)
            print("Sent Christmas wishes to girlfriend: %s" % time.ctime())

        # Send birthday wishes
        if festival_month == birthday_month and festival_day == birthday_day and now_time == "00:00":
            send_message(str_birthday)
            print("Sent birthday wishes to girlfriend: %s" % time.ctime())

        # Check every 60 seconds
        time.sleep(60)

if __name__ == "__main__":
    # Set the current directory as the working directory if needed
    # chdir(sys.path[0])

    # Start the WeChat bot based on the operating system
    if 'Windows' in system():
        bot = Bot()
    elif 'Darwin' in system():
        bot = Bot()
    elif 'Linux' in system():
        bot = Bot(console_qr=2, cache_path=True)
    else:
        print("Unable to recognize your operating system, please set it manually")

    # Read configuration file
    cf = configparser.ConfigParser()
    cf.read("./config.ini", encoding='UTF-8')

    # Set the girlfriend's WeChat name
    my_lady_wechat_name = cf.get("configuration", "my_lady_wechat_name")

    # Set times for morning, lunch, dinner, and bedtime greetings
    say_good_morning = cf.get("configuration", "say_good_morning")
    say_good_lunch = cf.get("configuration", "say_good_lunch")
    say_good_dinner = cf.get("configuration", "say_good_dinner")
    say_good_dream = cf.get("configuration", "say_good_dream")

    # Set girlfriend's birthday information
    birthday_month = cf.get("configuration", "birthday_month")
    birthday_day = cf.get("configuration", "birthday_day")

    # Read greeting messages from files
    str_list_good_morning = []
    with open("./remind_sentence/sentence_good_morning.txt", "r", encoding='UTF-8') as f:
        str_list_good_morning = f.readlines()
    print(str_list_good_morning)

    str_list_good_lunch = []
    with open("./remind_sentence/sentence_good_lunch.txt", "r", encoding='UTF-8') as f:
        str_list_good_lunch = f.readlines()
    print(str_list_good_lunch)

    str_list_good_dinner = []
    with open("./remind_sentence/sentence_good_dinner.txt", "r", encoding='UTF-8') as f:
        str_list_good_dinner = f.readlines()
    print(str_list_good_dinner)

    str_list_good_dream = []
    with open("./remind_sentence/sentence_good_dream.txt", "r", encoding='UTF-8') as f:
        str_list_good_dream = f.readlines()
    print(str_list_good_dream)

    # Set whether to include daily English learning in bedtime messages
    flag_learn_english = (cf.get("configuration", "flag_learn_english") == '1')
    print(flag_learn_english)

    # Set whether to include emoji in messages
    str_emoj = "(•‾̑⌣‾̑•)✧˖°----(๑´ڡ`๑)----(๑¯ิε ¯ิ๑)----(๑•́ ₃ •̀๑)----( ∙̆ .̯ ∙̆ )----(๑˘ ˘๑)----(●′ω`●)----(●･̆⍛･̆●)----ಥ_ಥ----_(:qゝ∠)----(´；ω；`)----( `)3')----Σ((( つ•̀ω•́)つ----╰(*´︶`*)╯----( ´´ิ∀´ิ` )----(´∩｀。)----( ื▿ ื)----(｡ŏ_ŏ)----( •ิ _ •ิ )----ヽ(*΄◞ิ౪◟ิ‵ *)----( ˘ ³˘)----(; ´_ゝ`)----(*ˉ﹃ˉ)----(◍'౪`◍)ﾉﾞ----(｡◝‿◜｡)----(ಠ .̫.̫ ಠ)----(´◞⊖◟`)----(。≖ˇェˇ≖｡)----(◕ܫ◕)----(｀◕‸◕´+)----(▼ _ ▼)----( ◉ืൠ◉ื)----ㄟ(◑‿◐ )ㄏ----(●'◡'●)ﾉ♥----(｡◕ˇ∀ˇ◕）----( ◔ ڼ ◔ )----( ´◔ ‸◔`)----(☍﹏⁰)----(♥◠‿◠)----ლ(╹◡╹ლ )----(๑꒪◞౪◟꒪๑)"
    str_list_emoj = str_emoj.split('----')
    flag_wx_emoj = (cf.get("configuration", "flag_wx_emoj") == '1')
    print(str_list_emoj)

    # Set festival wishes
    str_Valentine = cf.get("configuration", "str_Valentine")
    print(str_Valentine)

    str_Women = cf.get("configuration", "str_Women")
    print(str_Women)

    str_Christmas_Eve = cf.get("configuration", "str_Christmas_Eve")
    print(str_Christmas_Eve)

    str_Christmas = cf.get("configuration", "str_Christmas")
    print(str_Christmas)

    str_birthday = cf.get("configuration", "str_birthday")
    print(str_birthday)

    # Start the monitoring thread
    t = Thread(target=start_care, name='start_care')
    t.start()

    # Listener to receive messages from the girlfriend
    my_girl_friend = bot.friends().search(my_lady_wechat_name)[0]
    @bot.register(chats=my_girl_friend, except_self=False)
    def print_others(msg):
        # Print the received message
        print(msg.text)

        # Perform simple sentiment analysis
        postData = {'data': msg.text}
        response = post('https://bosonnlp.com/analysis/sentiment?analysisType=', data=postData)
        data = response.text

        # Sentiment score (closer to 1 means better mood, closer to 0 means worse mood)
        now_mod_rank = (data.split(',')[0]).replace('[[', '')
        print("Message from girlfriend: %s\nSentiment score: %s\nCloser to 1 means better mood, closer to 0 means worse mood, sentiment result is for reference only!\n\n" % (msg.text, now_mod_rank))

        # Send sentiment analysis result to the file transfer assistant
        mood_message = u"Message from girlfriend: " + msg.text + "\nSentiment score: " + now_mod_rank + "\nCloser to 1 means better mood, closer to 0 means worse mood, sentiment result is for reference only!\n\n"
        bot.file_helper.send(mood_message)
