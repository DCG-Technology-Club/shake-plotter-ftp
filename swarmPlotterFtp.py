from ftplib import FTP
import os
from pathlib import Path
import datetime
import time
import argparse
import requests




# -------------------- MAKE FILE NAME -------------------- #
def makeFileName():
    dateString = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
    currentFileName = dateString + ".png"
    return currentFileName

# -------------------- FILE PATH -------------------- #
def makeFilePath(fileType):
    if fileType == "10M":
        fileName = makeFileName()
        filePathString10m = '/home/pi/Shake/10mPlots' + fileName
        filePath10m = Path(filePathString10m)
        return filePathString10m, filePath10m, fileName

    elif fileType == "24H":
        fileName = makeFileName()
        filePathString24h = '/home/pi/Shake/24hPlots' + fileName
        filePath24h = Path(filePathString24h)
        return filePathString24h, filePath24h, fileName


# -------------------- MAKE PLOT -------------------- #
def makePlot():
    string, path, name = makeFilePath("10M")
    os.system("java -jar /home/pi/Shake/swarmPlotter.jar -p wave -t -10i -c RDDB2_EHZ_AM_00 -s wws:rs.local:16032 -z America/Puerto_Rico " + string)
    registerImage("PLOT", name)

# -------------------- MAKE HELI -------------------- #
def makeHeli():
    string, path, name = makeFilePath("24H")
    os.system("java -jar /home/pi/Shake/swarmPlotter.jar -p heli -t -24h -c RDDB2_EHZ_AM_00 -s wws:caps.raspberryshakedata.com:16022 -z America/Puerto_Rico " + string)
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
    #message = "Registering image: " imageType + " " + imageName
    #print(message)
    x = requests.post(url, data = dataObj, headers = headers)

    print(x.status_code)

# -------------------- PARSER INITIALIZATION -------------------- #
parser = argparse.ArgumentParser()
parser.add_argument("-H", "--heli", help="Output Helicorder (24h)", action="store_true")
parser.add_argument("-P", "--plot", help="Output Plot (10min)", action="store_true")

# Read arguments from the command line
args = parser.parse_args()

# Check for --version or -V
if args.heli: #Do Heli
    print("Heli mode!")
    makeHeli()

elif args.plot: #Do Plot
    print("Plot mode!")
    makePlot()

#with FTP('dcg.edu.pr', 'drive', 'T3chn0l0gy!') as ftp, open(filePath24h, 'rb') as file, ('STOR ' + fileName) as ftpCmd:
    #print(ftp.storbinary(ftpCmd, file))