import aiml
import time
import signal
import sys
import telegram
from datetime import date
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from gtts import gTTS
import logging
import os
import requests



k = aiml.Kernel()

#Create Brain File
if os.path.isfile("bot_brain.brn"):
	k.bootstrap(brainFile = "bot_brain.brn")
else:
	k.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
	k.saveBrain("bot_brain.brn")


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    chat_id = update.message.chat_id
    message = update.message.text
    print "ChatID and Message are start %s %s" %(chat_id,message)
    
    bot.sendMessage(update.message.chat_id, text='Hi This is Telegram Bot! :D')



def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')

def chatter(bot,update):

    chat_id = update.message.chat_id
    message = update.message.text
   
    print "ChatID and Message are chatter %s %s" %(chat_id,message)
    print message
    if message == "quit":
        exit()
    elif message == "save":
        k.saveBrain("bot_brain.brn")
    else:
        response = k.respond(message)
        print response
    
        
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        response = k.respond(message)
        print response
        bot.sendMessage(chat_id, text=response)
        url = "https://translate.google.com/translate_tts"

        headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0"}

        text = response

        params = {
            'ie': 'UTF-8',
            'q': text,
            'tl': 'en',
            'client': 'gtx'
        }


        r = requests.get(url, params = params, headers = headers)

        print(r.status_code)
        file = str(chat_id) + str(time.time()) + '.mp3'

        with open(file, 'wb') as f:
            f.write(r.content)
        
        bot.sendVoice(chat_id=chat_id, voice=open(file, 'rb'))
        os.remove(file)
        



def main():
    # Create the EventHandler and pass it your bot's token.
    
    
    #testbot
    updater = Updater("Pass BOT TOKEN")
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler([Filters.text], chatter))
    dp.add_handler(MessageHandler([Filters.text | Filters.video | Filters.photo | Filters.document], chatter))
   


    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
