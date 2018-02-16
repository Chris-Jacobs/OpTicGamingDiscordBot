import queue
import datetime
import time
import sqlite3
conn = sqlite3.connect('keys.db')
c = conn.cursor()
username, password, user_agent, twitchKey, client_secret, client_id, ytKey, imgurID, imgurSecret, schedulerbase, token,tokenTest  = c.execute("SELECT * FROM Keys").fetchone()
c.close()
print(username)

modMailChannel = None
postsChannel = None
subreddit = "OpTicGaming"
serverID = 305374394266681345
modMailChannelID = 309392299664867328
postID = 357559384529698816
#testing
#serverID = 252969515200020501
#modMailChannelID = 309394244932599818
#postID = 407635043163308032
modMail = []
retrieveTime = int(time.time() - 40)
#retrieveTime = 1517287992
timeout = 15
textCommands = {}
contentFilter = []
counter = 0

logs = {}
messages = queue.Queue()
logging = False

currencyStart = 100
currency = {

}


dark = False
purge = []

removalReasons = {}


bets = []
wagers = {}
blacklist = {}
freq = {}
monthFreq = {}
weekFreq = {}
months = {
    1:'January ',
    2:'February ',
    3:'March ',
    4:'April ',
    5:'May ',
    6:'June ',
    7:'July ',
    8:'August ',
    9:'September ',
    10:'October ',
    11:'November ',
    12:'December '
}
