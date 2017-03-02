#!/usr/bin/python
# Settings.py

def fsetbssid(bssid):
    global myglobalistbssid
    myglobalistbssid = []
    myglobalistbssid.append(bssid)
    return 
fsetbssid("") 


def fsetessid(essid):
    global myglobalistessid
    myglobalistessid = []
    myglobalistessid.append(essid)
    return 
fsetessid("") 

def fsetchan(chan):
    global myglobalistchan
    myglobalistchan = []
    myglobalistchan.append(chan)
    return 
fsetchan("") 


def fsetencrypt(encrypt):
    global myglobalistencrypt
    myglobalistencrypt = []
    myglobalistencrypt.append(encrypt)
    return 
fsetencrypt("") 

def fsetwps(wps):
    global myglobalistwps
    myglobalistwps = []
    myglobalistwps.append(wps)
    return 
fsetwps("") 


def fsetclients(clients):
    global myglobalistclients
    myglobalistclients = []
    myglobalistclients.append(clients)
    return 
fsetclients("") 


def fsetiface(iface):
    global myglobalistiface
    myglobalistiface = []
    myglobalistiface.append(iface)
    return 
fsetiface("") 

def fsetfilename(filename):
    global myglobalistfilename
    myglobalistfilename = []
    myglobalistfilename.append(filename)
    return 
fsetfilename("")

def fsetrutacap(rutacap):
    global myglobalistrutacap
    myglobalistrutacap = []
    myglobalistrutacap.append(rutacap)
    return 
fsetrutacap("./hs/")  
