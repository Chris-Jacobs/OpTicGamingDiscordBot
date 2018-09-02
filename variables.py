import queue
import datetime
import time
import sqlite3
conn = sqlite3.connect('keys.db')
c = conn.cursor()
username, password, user_agent, twitchKey, client_secret, client_id, ytKey, imgurID, imgurSecret, schedulerbase, token,tokenTest, modUsername, modPassword, modSecret, modClient, twitterKey, twitterSecret, twitterToken, twitterTokenSecret, localIP, dbUser, dbPassword, externalIP  = c.execute("SELECT * FROM Keys").fetchone()
c.close()

modMailChannel = None
postsChannel = None
subreddit = "OpTicGaming"
serverID = 305374394266681345
modMailChannelID = 309392299664867328
postID = 357559384529698816
voiceID = 360589014325264395
test = False
if test:
    serverID = 252969515200020501
    modMailChannelID = 309394244932599818
    postID = 407635043163308032
    voiceID = 440226989316636675
    token = tokenTest

sayings = {}

modMail = []
voice = {}
retrieveTime = int(time.time() - 40)
lastID = "8aeoo4"
try:
    with open('id.txt', 'r') as f:
        id = f.read()
        if len(id) == 6:
            lastID = id
except Exception:
    pass
print(lastID)
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
