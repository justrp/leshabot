#!/usr/bin/env python
# -*- coding: utf-8 -*-


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import File

import logging
from os.path import basename
import configparser


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
CONF = configparser.ConfigParser()
CONF.read('conf.ini')

def start(bot, update):
    update.message.reply_text("Send me picture")

def echo(bot, update):
    update.message.reply_text("This was not picture")

def getPhoto(bot, update):
    logger.info('Someone had send me photo')
    update.message.reply_text("Thanks")
    picture = bot.getFile(update.message.photo[-1]['file_id'])
    filename = basename(picture['file_path'])
    File.download(picture, CONF['BOT']['DOWNLOADFOLDER'] + filename)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    updater = Updater(CONF['BOT']['TOKEN'])

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.photo, getPhoto))
    dp.add_error_handler(error)


    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()
