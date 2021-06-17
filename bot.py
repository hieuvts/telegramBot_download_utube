from __future__ import unicode_literals
import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.files.video import Video
import youtube_dl
import os
import sys
import requests
import json
from datetime import datetime
import validators

youtube_video_path = "./video/video.mp4"
covid19_VN_stats_api = "https://api.apify.com/v2/key-value-stores/EaCBL1JNntjR3EakU/records/LATEST?disableRedirect=true"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def isValidCommand(args):
    print("args", args[0])
    if (len(args) > 2):
        print("Args > 2")
        return False
    elif (validators.url(args[0])):
        return True
    return True
# Get stats from Covid19api.com
def getResponse(url):
    response = requests.get(url)
    data = json.loads(response.text)
    return data

def compose_message(data):
    lastUpdated = data['lastUpdatedAtApify'].split('T')
    activeCase = data['treated']
    deathsCase = data['deceased']
    confirmedCase = data['infected']
    recoveredCase = data['recovered']

    lastUpdated = datetime.strptime(lastUpdated[0], '%Y-%m-%d')
    lastUpdated = lastUpdated.strftime("%d/%m/%Y")


    my_message = '''
    🗓  Cập nhật: {}
🦠  Số ca nhiễm: {}
<strong><em>⚰️  Số ca tử vong: {}</em></strong>
✅  Số ca hồi phục: {}
<em>🚨  Số ca đang điều trị: {}</em>
    '''.format(lastUpdated, confirmedCase, deathsCase, recoveredCase, activeCase)
    return my_message


def downloadVideo(url):
    if (os.path.exists(youtube_video_path)):
        os.remove(youtube_video_path)
        print("Removed old video!")
    ydl_opts = {'outtmpl': youtube_video_path}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2("Hi {}".format(user.mention_markdown_v2()),
    )

def getVideo(update: Update, context: CallbackContext):
    if (isValidCommand(context.args)):
        downloadVideo(context.args[0])
        if (os.path.exists(youtube_video_path)):
            video = open(youtube_video_path, 'rb')
            update.message.reply_video(video=video)
        print("Video sent")
    else:
        update.message.reply_html(text='''<b>URL is invalid</b>''')
def cv(update: Update, context: CallbackContext):
    data = getResponse(covid19_VN_stats_api)
    #Compose a message to send to telegram
    message = compose_message(data)
    update.message.reply_html(
        text=message,
    )


def main() -> None:
    updater = Updater(str(sys.argv[1]), use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("vid", getVideo))
    dispatcher.add_handler(CommandHandler("cv", cv))
    # Start the Bot
    updater.start_polling()
    #CTRL + C to STOP
    updater.idle()


if __name__ == '__main__':
    main()