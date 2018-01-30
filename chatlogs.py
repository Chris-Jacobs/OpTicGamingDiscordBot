#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive
import datetime
import variables
import asyncio
import os
import queue

class Log:
    def __init__(self, localFile, serverName, channelName):
        self.newMessages = []
        self.messages = []
        self.localFile = localFile
        self.serverName = serverName
        self.channelName = channelName
        self.googleDocFile  = None
        f = open(localFile, "w")
        f.close()
    def makeLog(self):
        self.googleFile = 0
    def addMessage(self, msg):
        self.messages.append(msg)
        self.newMessages.append(msg)
    async def writeToFile(self):
        f = open(self.localFile, "a")
        for message in self.newMessages:
            f.write(formatMessage(message))
        f.close()
        self.newMessages = []
    async def uploadFile(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)
        if (self.googleDocFile == None):
            self.googleDocFile = getOrCreateFile(self.serverName, self.channelName);
            #Find Appropriate folder
            #make folder
        #Write to folder
        self.googleDocFile.SetContentFile(self.localFile);
        self.googleDocFile.Upload();

def getOrCreateFile(server, channel):
    date = datetime.datetime.now().date()
    dir = []
    dir.append('/r/OpTicGaming')
    dir.append('Discord')
    dir.append(str(date.year))
    dir.append(variables.months[date.month])
    dir.append(date.day)
    folder = getItem(listFolder('root'), dir[0])
    for x in xrange(1, dir.amount()):
        f = getItem(listFolder(folder['id']), dir[x])
        if f is None:
            f = createFolder(folder, dir[x])
        folder = f
    id = folder['id']
    name = server + "_" + channel
    file = getItem(listFolder(folder['id']), name)
    if file is None:
        file = drive.CreateFile({'title': name, "parents":  [{"kind": "drive#fileLink","id": id}]})
    return file 
            
def formatMessage(message):
    name = message.author.name
    s = str(message.timestamp) + " - " + name + " :" + message.content + "\n"
    return s
async def log():
    variables.logging = True
    while variables.messages.empty() is False:
        #printQueue(variables.messages)
        message = variables.messages.get()
        channel = message.channel
        server = channel.server
        try:
            log = variables.logs[channel]
        except KeyError:
            s = server.name + "_" + channel.name
            log = Log("logs/" + s + ".txt", channel.name, server.name)
        log.addMessage(message)
        variables.logs[channel] = log
    variables.logging = False

def listFolder(parent):
  filelist=[]
  file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % parent}).GetList()
  #print(file_list)
  #for f in file_list:
  #  if f['mimeType']=='application/vnd.google-apps.folder': # if folder
  #      filelist.append({"id":f['id'],"title":f['title'],"list":ListFolder(f['id'])})
   # else:
   #     filelist.append(f['title'])
  return file_list

def getItem(file_list, name):
    if file_list is None:
        return None
    for file in file_list:
        if (file['title'] == name):
            return file
    return None

def createFolder(parent, name):
    folder = drive.CreateFile({'title': name,
                               "parents": [{'id': parent['id']}],
                               "mimeType": "application/vnd.google-apps.folder"})
    folder.Upload()
    return folder



#ListFolder('root');
#file1 = drive.CreateFile({'title': 'Hello.txt'})
#file1.Upload() # Upload the file.
#file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

#print(listFolder('root'))
#print(ListFolder('root'))
#og = getFolder(listFolder('root'), '/r/OpTicGaming')
#print(og);
#discord = getFolder(listFolder(og['id']), 'Discord')
#chatlogs = getFolder(listFolder(discord['id']), 'chat-logs')
#currentYear = getFolder(listFolder(chatlogs['id']),str(date.year))
#currentMonth = getFolder(listFolder(currentYear['id']), variables.months[date.month])
#print(getFolder(listFolder(currentYear['id']), variables.months[date.month + 1]))
#print(chatlogs)
#print(date)
#currentDay = createFolder(currentMonth, str(date.day) )

#file1 = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": id}],'title': 'Hello.txt' })
#file1.SetContentString("Test")
#file1.Upload()

