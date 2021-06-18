from __future__ import unicode_literals
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

import os
import sys
import validators
import getCovid19Stat
import getYoutubeDL
#import getInstagram

path = "./video/video.mp4"
# saved_reel_path = "./insta/reel.mp4"
# saved_hashtag_path = "./insta/"
# saved_profile_path = "./insta/"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def isValidCommand(args):
    if (len(args) > 2):
        return False
    elif (validators.url(args[0])):
        return True
    return True


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2("Hi {}".format(user.mention_markdown_v2()),
                                     )

# /vid url -->> Get Video using youtube-dl


def getVideo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if (isValidCommand(context.args)):
        # Get message_id of the message below
        try:
            msg_status_downloading = context.bot.send_message(
                chat_id=chat_id, text="Downloading your video...")
        except Exception as e:
            context.bot.send_message(
                chat_id=chat_id, text="Error: {}".format(e))

        getYoutubeDL.getVideo(context.args[0])
        
        if (os.path.exists(path)):
            video = open(path, 'rb')
            #print(msg_status_downloading)
            update.message.reply_video(video=video)
            context.bot.delete_message(
            chat_id=chat_id, message_id=msg_status_downloading['message_id'])

        print("Video sent")
    else:
        update.message.reply_html(text='''<b>URL is invalid</b>''')

# /cv --> Get Covid19 Stats (in Vietnam)
def cv(update: Update, context: CallbackContext):
    msg = getCovid19Stat.getCovid19Stats()
    update.message.reply_html(
        text=msg,
    )

# def ig(update: Update, context: CallbackContext):
#     chat_id = update.message.chat_id
#     if (isValidCommand(context.args)):
#         # Get message_id of the message below
#         try:
#             msg_status_downloading = context.bot.send_message(
#                 chat_id=chat_id, text="Downloading Instagram stuffs...")
#         except Exception as e:
#             context.bot.send_message(
#                 chat_id=chat_id, text="Error: {}".format(e))

#         getInstagram.getInsta(context.args[0])
        
#         if (os.path.exists(path)):
#             video = open(saved_reel_path, 'rb')
#             #print(msg_status_downloading)
#             update.message.reply_video(video=video)
#             context.bot.delete_message(
#             chat_id=chat_id, message_id=msg_status_downloading['message_id'])

#         print("Insta stuffs sent")
#     else:
#         update.message.reply_html(text='''<b>URL is invalid</b>''')

def test(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text="HI")


def main() -> None:
    # Execute "python3 bot.py <BOT_TOKEN>"
    #print("TOKEN ", sys.argv[1])
    BOT_TOKEN = str(sys.argv[1])
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("vid", getVideo))
    dispatcher.add_handler(CommandHandler("cv", cv))
    dispatcher.add_handler(CommandHandler("tt", test))
    # Start the Bot
    updater.start_polling()
    # CTRL + C to STOP
    updater.idle()


if __name__ == '__main__':
    main()
