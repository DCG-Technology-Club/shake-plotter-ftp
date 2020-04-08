from ftplib import FTP
import os
from pathlib import Path
import datetime
import time
import requests
import logging as log
from dotenv import load_dotenv
load_dotenv()


# -------------------- GET FTP DETAILS FROM .ENV -------------------- #
ftp = {
    "url" : os.environ.get("FTP_URL"),
    "user" : os.environ.get("FTP_USER"),
    "pass" : os.environ.get("FTP_PASS")
}

# -------------------- MAKE FILE NAME -------------------- #
def makeFileName():
    dateString = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    currentFileName = dateString + ".png"
    return currentFileName

# -------------------- DIRECTORY -------------------- #
def directory(folder):
    currentDirectory = os.getcwd()
    return currentDirectory + '/' + folder

# -------------------- FILE PATH -------------------- #
def makeFilePath(fileType):
    if fileType == "10M":
        fileName = makeFileName()
        homeDirectory = directory("10mPlots")
        if not os.path.exists(homeDirectory):
            os.mkdir(homeDirectory)
        filePathString10m = homeDirectory + '/' + fileName
        ftpPath = "plots"
        filePath10m = Path(filePathString10m) # Not used
        return filePathString10m, filePath10m, ftpPath, fileName

    elif fileType == "24H":
        fileName = makeFileName()
        homeDirectory = directory("24hPlots")
        if not os.path.exists(homeDirectory):
            os.mkdir(homeDirectory)
        filePathString24h = homeDirectory + '/' + fileName
        ftpPath = "helicorders"
        filePath24h = Path(filePathString24h) # Not used
        return filePathString24h, filePath24h, ftpPath, fileName

# -------------------- MAKE PLOT -------------------- #
def makePlot():
    string, localPath, ftpPath, name = makeFilePath("10M")
    os.system("java -jar " + directory("swarmPlotter.jar") + " -p wave -t -10i -c RDDB2_EHZ_AM_00 -s wws:rs.local:16032 -z America/Puerto_Rico " + string)
    if uploadFTP(localPath, ftpPath, name):
        registerImage("PLOT", name)

# -------------------- MAKE HELI -------------------- #
def makeHeli():
    string, localPath, ftpPath, name = makeFilePath("24H")
    os.system("java -jar " + directory("swarmPlotter.jar") + " -p heli -t -24h -c RDDB2_EHZ_AM_00 -s wws:caps.raspberryshakedata.com:16022 -z America/Puerto_Rico " + string)
    if uploadFTP(localPath, ftpPath, name):
        registerImage("HELI", name)

# -------------------- REGISTER IMAGE ON API -------------------- #
def registerImage(imageType, imageName):
    url = "https://api.dcg.edu.pr/Images/Create"
    headers = {
    'Content-Type':'application/x-www-form-urlencoded',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WIN64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'Content-Length':'0',
    'Host':'api.dcg.edu.pr'
    }

    dataObj="imageTypeID=" + imageType + "&imageName=" + imageName
    x = requests.post(url, data = dataObj, headers = headers)

    print(x.status_code)

# -------------------- UPLOAD FILE THROUGH FTP -------------------- #
def uploadFTP(localPath, ftpPath, fileName):
    f = FTP(ftp["url"], ftp["user"], ftp["pass"])
    file = open(localPath, 'rb')
    print(localPath)
    print(fileName)
    shakeDir = 'shake'

    if not shakeDir in f.nlst():
        f.mkd(shakeDir)
    
    f.cwd(shakeDir)

    if not ftpPath in f.nlst():
        f.mkd(ftpPath)
    f.cwd(ftpPath)

    cmd = "STOR " + fileName

    f.storbinary(cmd, file)