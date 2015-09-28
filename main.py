# main.py
# ruTorrent Bot for add torrent and monitorate your seedmachine
# command list:
# /start
# /help
# /info
# /config
# /hash
#
# TO DO:
# After the description setted with the BotFather user will send the /start command
# Now starts the setting process where the bot will ask first the host, port, user and password for logging in to your rutorrent page.
# Future changes to this setting can be done by using /config where the keyboard change to set HOST and PORT
# So selecting Host bot will ask the url and after that the kwybord return to the sepcific one for config until you select EXIT
# To add magnet you only need to send the magnet link without any command

# add more command like:
# /torrent add .torrent file
# /status to see the status of all existing torrent
# DONE /hash to add a torrent based on his hash
# add the option to have multiple session

import logging, coloredlogs
#import auxiliary_module
from logging.handlers import RotatingFileHandler
# requests module for basic http post
import requests
from requests.auth import HTTPBasicAuth
# telegram module for easy work with bot conf
import telegram
# file used to store sensible data, like API key
import config
import init
import botDef
import handleTorrent
# xmlrpc module for rtorrent communication
import xmlrpc.client
from time import sleep


logger = {}
last_update = 0
lastMsgId = 0
botName = 'ruTorrentPy'
# token = config.TOKEN
# ADDRESS = config.ADDRESS
# USERNAME = config.USERNAME
# PASSWORD = config.PASSWORD

commands = {
'start': '/start',
'info': '/info',
'help': '/help',
'config': '/config',
'hash': '/hash'
}

def main(argv=None):
    SetLogger()
    if argv is None or len(argv) <= 1:
        Init()

def SetLogger():
    global logger
    logger = logging.getLogger(__name__)
    # NOSET DEBUG INFO WARNING ERROR CRITICAL
    logger.setLevel(logging.DEBUG)
    # Create a file handler where log is located
    handler = RotatingFileHandler('rutorrent.log', mode='a', maxBytes=5 * 1024 * 1024,
                                  backupCount=5, encoding=None, delay=0)
    handler.setLevel(logging.DEBUG)
    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s(%(lineno)d) %(message)s')
    handler.setFormatter(formatter)
    # Add the handlers to the logger
    logger.addHandler(handler)

    logger.info('Log inizialized')

def Init():
    # xmlrpc settings
    # server = xmlrpc.client.ServerProxy(HOST)
    logger.info("-- Init -- BOT creation")
    # Infinite Loop
    UpdateLoop()
    return

def UpdateLoop():
    while True:
        try:
            ManageUpdates()
            sleep(0.5)
        except Exception:
            # Error
            # logging.exception()
            logger.error("Exit from loop!")


# def ManageUpdates():
#     # global LAST_UPDATE_ID
#     LAST_UPDATE_ID = bot.LAST_UPDATE_ID
#     # Fetch last message
#     updates = bot.getUpdates(offset=LAST_UPDATE_ID)
#     if(not updates):
#         logger.error("Couldn't get updates")
#         return
#     for update in updates:
#         command = update.message.text
#         chat_id = update.message.chat.id
#         update_id = update.update_id
#         answer = ''
#         init.config_start(chat_id)
#         # If newer than the initial
#         if LAST_UPDATE_ID < update_id:
#             if command:
#                 answer = GetCommand(command)
#                 if(answer):
#                     bot.sendMessage(chat_id=chat_id, text=answer)
#                 LAST_UPDATE_ID = update_id
#
#             if LAST_UPDATE_ID < update_id:  # If newer than the initial
#                                             # LAST_UPDATE_ID
#                 if text:
#                     rutorrent = magnet(text)
#                     bot.sendMessage(chat_id=chat_id, text="Torrent Addedd, Hurray! :D")
#                     LAST_UPDATE_ID = update_id

def ManageUpdates():
    botDef.update()
    answer = ''
    # # If newer than the initial
    # if bot.LAST_UPDATE_ID < bot.update_id:
    #     if bot.command:
    #         answer = GetCommand(bot.command)
    #         if(answer):
    #             bot.sendMessage(chat_id=chat_id, text=answer)
    #         LAST_UPDATE_ID = update_id
    #
    #     if LAST_UPDATE_ID < update_id:  # If newer than the initial
    #                                     # LAST_UPDATE_ID
    #         if text:
    #             rutorrent = magnet(text)
    #             bot.sendMessage(chat_id=chat_id, text="Torrent Addedd, Hurray! :D")
    #             LAST_UPDATE_ID = update_id


def GetCommand(msg):
    answer = ''
    if(msg):
        command = msg.split()[:1]
        command = str(command)
        par = msg.split()[1:]
        par = str(par)
        if("/" in command):
            logger.debug('Command: ' + command)
        else:
            logger.debug('Message: ' + command)
        if(commands['help'] in command):
            answer = helpTxt
            logger.debug('Answer: helpTxt')
        elif(commands['info'] in command):
            answer = infoTxt
            logger.debug('Answer: infoTxt')
        elif(commands['start'] in command):
            answer = startTxt
            logger.debug('Answer: startTxt')
        elif(commands['hash'] in command):
            addMagnet(Hash2Magnet(par))
            answer = "Hash added succesfully"
        elif(command[2:8] == 'magnet'):
            addMagnet(command)
            answer = 'Magnet added succesfully!'
            logger.debug('Answer: Manget added')
        elif(commands['host'] in command):
            if(par == '[]'):
                answer = config.HOST
                logger.debug('Answer: Host replay')
            else:
                answer = 'Host set'
                logger.debug('Answer: Host set')
        else:
            answer = 'No command or magnet found'
            logger.debug('No command')
    return answer


if __name__ == '__main__':
    main()
