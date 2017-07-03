import queue
token = "" #if real
modMailServerID = 305374394266681345
modMailChannelID = 309392299664867328
username = "Crim_Bot"
password = ""
subreddit = "OpTicGaming"
user_agent = "PyOGSidebar 1.0"
twitchKey = ""
client_secret = ""
client_id = ""
#token = "" #if testing
#subreddit = "OpTicGamingSandbox"
#modMailServerID = 252969515200020501
#modMailChannelID = 309394244932599818

modMailChannel = None

modMail = []
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
