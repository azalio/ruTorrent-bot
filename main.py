# main.py
# ruTorrent Bot for add torrent and monitoring your seedmachine
# command list:
# /start
# /help
# /info
# /config
# /hash
#
# TO DO:
# After the description setted with the BotFather user will send the /start command
# Now starts the setting process where the bot will ask first the host, port, user and password for logging in to
# your rutorrent page.
# Future changes to this setting can be done by using /config where the keyboard change to set HOST and PORT
# So selecting Host bot will ask the url and after that the keyboard return to the specific one for config until
# you select EXIT
# To add magnet you only need to send the magnet link without any command

# add more command like:
# /torrent add .torrent file
# /status to see the status of all existing torrent
# DONE /hash to add a torrent based on his hash
# add the option to have multiple session


import handleTorrent
# xmlrpc module for rtorrent communication
# import xmlrpc.client
from time import sleep
import logging
from logging.handlers import RotatingFileHandler
import threading
import botDef
import sys


logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
# # Create a file handler where log is located
# handler = RotatingFileHandler('rutorrent.log', mode='a', maxBytes=5 * 1024 * 1024,
#                               backupCount=5, encoding=None, delay=0)
# create file handler which logs even debug messages
# handler.setLevel(logging.INFO)
# # create console handler with a higher log level
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
# # Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s(%(lineno)d) %(message)s')
# handler.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
# logger.addHandler(handler)
logger.addHandler(ch)

logger.debug('Log initialized')

last_update = 0
lastMsgId = 0
botName = 'ruTorrentPy'

commands = {
    'start': '/start',
    'info': '/info',
    'help': '/help',
    'config': '/config',
    'hash': '/hash'
}


def main(argv=None):
    if argv is None or len(argv) <= 1:
        logger.debug("Begin main()")
        init()


def init():
    # xmlrpc settings
    # server = xmlrpc.client.ServerProxy(HOST)
    logger.debug("Begin init()")
    # Infinite Loop
    updateloop()
    return


def updateloop():
    while True:
        try:
            manageupdates()
            sleep(1)
        except Exception:
            # Error
            logger.exception("Exit from loop!")
            logger.error("Exit from loop!")
            return


def manageupdates():
    botDef.update()
    # If newer than the initial
    if botDef.LAST_UPDATE_ID < botDef.update_id:
        if botDef.text:
            # thread = threading.Thread(target=setanswer, args=(botDef.text,botDef.chat_id,))
            # logger.info("Start new thread from " + str(botDef.chat_id))
            # thread.start()
            setanswer(botDef.text, botDef.chat_id)
        botDef.LAST_UPDATE_ID = botDef.update_id


def setanswer(text, chat_id):
    answer = getcommand(text, chat_id)
    if answer:
        botDef.bot.sendMessage(chat_id=chat_id, text=answer)


def getcommand(msg, chat_id):
    name_file = "chat_id_file/" + str(chat_id) + ".pkl"
    f = open(name_file, "a+")
    f.close()
    if msg:
        command = msg.split()[:1]
        command = str(command)
        par = msg.split()[1:]
        par = str(par)
        if "/" in command:
            logger.debug('Command: ' + command)
        else:
            logger.debug('Message: ' + command)
        if commands['help'] in command:
            answer = botDef.helpTxt
            logger.debug('Answer: helpTxt')
        elif commands['info'] in command:
            answer = botDef.infoTxt
            logger.debug('Answer: infoTxt')
        elif commands['start'] in command:
            logger.debug('Call: fistConfig')
            botDef.bot.sendMessage(chat_id=chat_id, text=botDef.startTxt)
            answer = botDef.firstconfig()
        elif chat_id in botDef.chat_id_f_config:
            answer = botDef.firstconfig()
            logger.debug('Answer: firstconfig')
        elif commands['config'] in command:
            logger.debug('Call: config')
            answer = botDef.config()
        elif chat_id in botDef.chat_id_host_config:
            answer = botDef.sethost()
            logger.debug('Call: sethost')
        elif chat_id in botDef.chat_id_port_config:
            answer = botDef.setport()
            logger.debug('Call: setport')
        elif chat_id in botDef.chat_id_user_config:
            answer = botDef.setusername()
            logger.debug('Call: serUsername')
        elif chat_id in botDef.chat_id_password_config:
            answer = botDef.setpassword()
            logger.debug('Call: setpassword')
        elif chat_id in botDef.chat_id_config:
            logger.debug('Call: config')
            answer = botDef.config()
        elif commands['hash'] in command:
            if par[1:-1] == "":
                answer = "Put a hash after the /hash command!"
            else:
                answer = handleTorrent.addmagnet(handleTorrent.hash2magnet(par), chat_id)
        elif command[2:8] == 'magnet':
            magnet = command[2:-2]
            answer = handleTorrent.addmagnet(magnet, chat_id)
            logger.debug('Answer: Manget added')
        else:
            answer = 'No command or magnet found. Press /help for the list of the supported commands'
            logger.debug('No command')
        return answer


if __name__ == '__main__':
    main()
