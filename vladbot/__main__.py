#!/usr/bin/env python2
import sys
import MumbleConnection
import IRCConnection
import ConsoleConnection
import time
import ConfigParser
import os.path
import vladbot
import datetime
from difflib import SequenceMatcher
from wikiapi import WikiApi
import subprocess
import re
from bs4 import BeautifulSoup
import urllib2



irc = None
mumble = None
console = None


def mumbleTextMessageCallback(sender, message):
    line = "mumble: " + sender + ": " + message
    console.sendTextMessage(line)
    timequestion1 = similar("@vladbot qu'elle jour nous somme ?", message)
    timequestion2 = similar("@vladbot qu'elle heure est t'il ?", message)
    polites = similar("@vladbot merci", message) 
    whereisvlad = similar("ou est vlad ?", message)
    recherche = similar("@vladbot wiki", message)
    rechercheimage = similar("@vladbot image", message)
    stackover = similar("@vladbot stackover", message)
    if(timequestion1 > 0.7 or timequestion2 > 0.7 or "qu'elle heure" in message or "qu'elle jour" in message):
        jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        mois = ["Janvier", u"Février", "Mars", "Avril", "Mai", "Juin", "Juillet", u"Août", "Septembtre", "Octobre", "Novembre", "Décembre"]
        now = datetime.datetime.now()
        d = str('%02d' % now.month)
        y = str(now.year)
        h = str('%02d' % now.hour)
        m = str('%02d' % now.minute)
        jours = jours[time.localtime()[6]]
        mois = mois[time.localtime()[1]-1]
        mumble.sendTextMessage("nous sommes le "+ jours + " " + d + " "+ mois + " " + y + " il est " + h + ":" + m)
    if(polites > 0.7):
        mumble.sendTextMessage("de rien :)")
    if(whereisvlad > 0.5):
        mumble.sendTextMessage("je ne c'est pas ... certainement entrain de construire une navette spacial...")
    if(recherche > 0.7 or "@vladbot wiki" in message):
        recherche = message.split("wiki")
        print recherche[1]
        wiki = WikiApi()
        wiki = WikiApi({ 'locale' : 'fr'}) # to specify your locale, 'en' is default

        results = wiki.find(recherche[1])
        article = wiki.get_article(results[0])
        mumble.sendTextMessage(article.summary)
    if(stackover > 0.7 or "@vladbot stackover" in message):
        recherche = message.split("stackover")
        print recherche[1].strip()

        proc = subprocess.Popen(['socli', '-q', recherche[1].strip()], stdout=subprocess.PIPE)
        for lines in proc.stdout:
            time.sleep(1)
            if lines.rstrip() is not None or lines.rstrip() is not "":
                mumble.sendTextMessage(lines.rstrip())

    if(rechercheimage > 0.7 or "@vladbot image" in message):
        mumble.sendTextMessage('en cours de recherche...')
        recherche = message.split("image")

        proc = subprocess.Popen(['python3', 'selenium_bot.py', recherche[1]], stdout=subprocess.PIPE)
        line = proc.stdout.readline()
        soup = BeautifulSoup(line, "lxml")
        compteur = 0
        for tag in soup.findAll('img'):
            v = tag.get('src')  # get's "src", else "dfr_src", if both are missing - None
            if v is not None:
                compteur = compteur + 1
                if compteur > 0 and "http://" in v or "https://" in v or "data:" in v:
                    mumble.sendTextMessage('<img src="'+v+'"/>')
                    time.sleep(2)
                if compteur > 5:
                    break

            if v is None:
                continue
                print("v is NONE")


def similar(w1, w2):
    w1 = w1 + ' ' * (len(w2) - len(w1))
    w2 = w2 + ' ' * (len(w1) - len(w2))
    return sum(1 if i == j else 0 for i, j in zip(w1, w2)) / float(len(w1))

def consoleTextMessageCallback(sender, message):
    line = "console: " + message
    mumble.sendTextMessage(line)


def mumbleConnected():
    pass


def mumbleDisconnected():
    line = "connection to mumble lost. reconnect in 5 seconds."
    console.sendTextMessage(line)
    time.sleep(5)
    mumble.start()


def mumbleConnectionFailed():
    line = "connection to mumble failed. retrying in 15 seconds."
    console.sendTextMessage(line)
    time.sleep(15)
    mumble.start()


def main():
    print("vladbot mumble bot " + vladbot.VERSION)

    global mumble
    global irc
    global console

    loglevel = 3

    if len(sys.argv) > 1:
        # load the user-specified conffile
        conffiles = [sys.argv[1]]
    else:
        # try finding a confile at one of the default paths
        conffiles = ["vladbot.conf", "/etc/vladbot.conf"]

    # try all of the possible conffile paths
    for conffile in conffiles:
        if os.path.isfile(conffile):
            break
    else:
        if len(conffiles) == 1:
            raise Exception("conffile not found (" + conffiles[0] + ")")
        else:
            raise Exception("conffile not found at any of these paths: " +
                            ", ".join(conffiles))

    # read the conffile from the identified path
    print("loading conf file " + conffile)
    cparser = ConfigParser.ConfigParser()
    cparser.read(conffile)

    # configuration for the mumble connection
    mblservername = cparser.get('mumble', 'server')
    mblport = int(cparser.get('mumble', 'port'))
    mblnick = cparser.get('mumble', 'nickname')
    mblchannel = cparser.get('mumble', 'channel')
    mblpassword = cparser.get('mumble', 'password')
    mblloglevel = int(cparser.get('mumble', 'loglevel'))

    # create server connections
    # hostname, port, nickname, channel, password, name, loglevel
    mumble = MumbleConnection.MumbleConnection(
        mblservername,
        mblport,
        mblnick,
        mblchannel,
        mblpassword,
        "mumble",
        mblloglevel)


    console = ConsoleConnection.ConsoleConnection(
        "utf-8",
        "console",
        loglevel)

    # register text callback functions
    mumble.registerTextCallback(mumbleTextMessageCallback)
    console.registerTextCallback(consoleTextMessageCallback)

    # register connection-established callback functions
    mumble.registerConnectionEstablishedCallback(mumbleConnected)


    # register connection-lost callback functions
    mumble.registerConnectionLostCallback(mumbleDisconnected)

    # register connection-failed callback functions
    mumble.registerConnectionFailedCallback(mumbleConnectionFailed)

    # start the connections.
    # they will be self-sustaining due to the callback functions.
    mumble.start()

    # start the console connection, outside a thread (as main loop)
    console.run()


if __name__ == "__main__":
    main()
