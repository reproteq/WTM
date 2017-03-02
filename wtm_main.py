#!/usr/bin/python
######################
# IMPORT MODULES
###################
import sys, os
#############
DN = open('./debug.log', 'w')
ERRLOG = open(os.devnull, 'w')
OUTLOG = open(os.devnull, 'w')

#############
# COLORS #
#############
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple
C = '\033[36m'  # cyan
GR = '\033[37m'  # gray
###############
# BANNER #
###############
def ban():
    print W + " +----------------------------------------------------------------------+"+ W
    print W + " | "+ G," _ _ _ ",P, " _ ", O," ___ ", B," _ ", R," _____ ", GR," _____ ", P," _____ " + W + "                 | " 
    print W + " | "+ G,"| | | |",P, "|_|", O,"|  _|", B,"|_|", R,"|_   _|", GR,"|_   _|", P,"|     | ",B,"_ _ ",O," ___ " + W + "   | " 
    print W + " | "+ G,"| | | |",P, "| |", O,"|  _|", B,"| |", R,"  | |  ", GR,"  | |  ", P,"| | | |", B,"| | |",O,"|  _|"+ W + "   | " 
    print W + " | "+ G,"|_____|",P, "|_|", O,"|_|  ", B,"|_|", R,"  |_|  ", GR,"  |_|  ", P,"|_|_|_|", B,"|___|",O,"|_|  "+ W + "   | " 
    print W + " +----------------------------------------------------------------------+"+ W
    print (W + ' | '+ O + 'Brute Force with GPU Cuda'),
    print (G + ' W'+ P + 'i' + O + 'f'+ B + 'i' + R +'T'+ GR + 'T'+ P + 'M' + B + 'u' + O + 'r'+ GR+' v1.2 / 2016-21-12 '+ C+'PwRby: '+ GR +'TT '+ P +'MUR '+W+'|')
    print W + " ------------------------------------------------------------------------"+ W


    return
#############
#global retbssid

#####################
# CONSTANT DEFINITIONS
menu_actions  = {}  
 
######################
#  MAIN MENU FUNCTIONS
#####################
 
######################
# DEF MAIN
#####################
def main_menu():
    os.system('clear')
    ban()
    import wtm_settings
    
    myglobalistbssid = wtm_settings.myglobalistbssid[0]
    myglobalistessid = wtm_settings.myglobalistessid[0]
    myglobalistchan = wtm_settings.myglobalistchan[0]
    myglobalistencrypt = wtm_settings.myglobalistencrypt[0]
    myglobalistwps = wtm_settings.myglobalistwps[0]
    myglobalistiface = wtm_settings.myglobalistiface[0] 
    myglobalistclients = wtm_settings.myglobalistclients
    myglobalistfilename = wtm_settings.myglobalistfilename[0]

    print " "
    print W + " +--------------------------+--------------------------+----------------+"
    print W + " | BSSID: " + G + str(myglobalistbssid) + W + "  ESSID: " + G + str(myglobalistessid) 
    print W + " | IFACE: "+ G + str(myglobalistiface) + W + "  CHANNEL: " + G + str(myglobalistchan) + W + " CRYPT: "+ G + str(myglobalistencrypt) + W + " WPS: " + G + str(myglobalistwps)
    print W + " | FILE: " + G + str(myglobalistfilename)
    print W + " +--------------------------+--------------------------+----------------+"
    print " "

    print GR,"Please choose the menu you want to start:"
    print (GR + ' ['+ G +'A'+ GR +']' + B +"  Attack ")
    print (GR + ' ['+ G +'S'+ GR +']' + B +"  Scan ")
    print (GR + ' ['+ G +'O'+ GR +']' + B +"  Open Handshake ")
    print (GR + ' ['+ G +'L'+ GR +']' + B +"  List Cores Pyrit ")
    print (GR + ' ['+ G +'G'+ GR +']' + B +"  GPU Server Pyrit Cloud ")
    print (GR + ' ['+ G +'P'+ GR +']' + B +"  Password Cheker ")
    print (GR + ' ['+ G +'C'+ GR +']' + B +"  Calc Time PMKS ")
    print (GR + ' ['+ G +'B'+ GR +']' + B +"  Back ")
    print (GR + ' ['+ G +'E'+ GR +']' + B +"  Exit ")
    choice = raw_input(" >>  ")
    exec_menu(choice)
 
    return
 
######################
# DEF EXECUTE MENU
#####################
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            menu_actions['main_menu']()
    return

######################
# DEF MENU A ATTACK
#####################
def menuA():
    print "Hello Menu Attack !\n"
    import wtm_settings ,wtm_attack
    myglobalistfilename = wtm_settings.myglobalistfilename[0]
    myglobalistwps = wtm_settings.myglobalistwps[0]
    myglobalistbssid = wtm_settings.myglobalistbssid[0]
    myglobalistessid = wtm_settings.myglobalistessid[0]
    RUN_CONFIG = wtm_attack.RunConfiguration()

    if myglobalistfilename == '' and myglobalistwps != '':
        engine = wtm_attack.RunEngine(RUN_CONFIG)
        engine = wtm_attack.RunEngine(RUN_CONFIG).get_iface()
        #engine = wtm_attack.RunEngine(RUN_CONFIG).StartWPS() 

        lowbssid = myglobalistbssid[:8]
        for line in open("patts.csv"):
            if lowbssid in line:
                pines = line.split(',')[4].lower().split(' ')
                for pin in pines:
                    engine = wtm_attack.RunEngine(RUN_CONFIG).attack_wps(pin) 
         
        #engine = wtm_attack.RunEngine(RUN_CONFIG).exit_gracefully(1)

    if myglobalistfilename != '' :  
        engine = wtm_attack.RunEngine(RUN_CONFIG) 
        engine = wtm_attack.RunEngine(RUN_CONFIG).StartWPA() 
    
    else:
         print (O + 'Attack finalizado, seleccione otro objetivo ... '+ B)       
        

    print (GR + ' ['+ G +'B'+ GR +']' + B +"  Back ")
    print (GR + ' ['+ G +'E'+ GR +']' + B +"  Exit ")
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return
 
######################
# DEF MENUS SCAN
#####################
def menuS():
    print "Hello MenuS !\n"
    import wtm_wkmod
    engine = wtm_wkmod.RunEngine(wtm_wkmod.RUN_CONFIG)
    engine.Start()    
    print (GR + ' ['+ G +'B'+ GR +']' + B +"  Back ")
    print (GR + ' ['+ G +'E'+ GR +']' + B +"  Exit ")
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return
##############
# MENU O
###############
def menuO():
    global filename, filtro
    import string
    import os
    import subprocess
    from subprocess import Popen, PIPE
    filtro = raw_input( GR + "[+] Si quieres filtrar los resultados, introduce parte del nombre o pulsa enter :  ")
    lineas = []
    if filtro == '':
        proc = Popen(['/bin/ls','-1tr','./hs/'], stdout=PIPE, stderr=DN)
    else:
        proc = Popen(['/bin/ls -1tr ./hs/ | grep '+filtro ], stdout=PIPE, stderr=DN , shell=True )
    i = 0
    menuoptions = []
    for line in proc.communicate()[0].split('\n'):  ##fallo en el bucle s
        if len(line) == 0: continue
        menuoptions.append(line)
    if len(menuoptions) == 1:
        filename = menuoptions[0]  # si solo hay uno, continuamos  
    elif len(menuoptions) > 1:
        print GR + " [+]" + W + " capturas encontradas " + G + " :" + W
    if len(menuoptions) == 1:
        filename = menuoptions[0]
    else:
        for i, menuopcion in enumerate(menuoptions):
            print "  %s. %s" % (G + str(i + 1) + W, G + ' \t'+menuopcion.replace('_','\t').replace('.cap','') + W)
        ri = raw_input("%s [+]%s Selecciona el %snumero%s de la captura (%s1-%d%s): %s" % \
                           (GR, W, G, W, G, len(menuoptions), W, G))
        i = int(ri)
        filename = menuoptions[i - 1] 
    print "Seleccionado el fichero: "+filename
    global bssid, essid
    # Call pyrit to "Analyze" the cap file's handshakes.
    cmd = ['pyrit','-r', './hs/'+filename,'analyze']
    proc = Popen(cmd, stdout=PIPE, stderr=DN)
    proc.wait()
    hit_essid = False
    for line in proc.communicate()[0].split('\n'):
        print line
        
        # Iterate over every line of output by Pyrit
        if line == '' or line == None: continue
        if line.find("AccessPoint") != -1:
            #print line
            partes = line.split()
	    bssid = partes[2]
            bssid = bssid.upper()
            print G + "BSSID seleccionado " + bssid
            essid = partes[3]
            essid = essid.replace("('","")
            essid = essid.replace("'):","")
            print G + "ESSID seleccionado: " +essid

    #time.sleep(13)
    import wtm_settings
         
    wtm_settings.fsetbssid(bssid)     # global init before used in other imported modules
    wtm_settings.fsetessid(essid) 
    wtm_settings.fsetfilename(filename) 
    wtm_settings.fsetrutacap("./hs/") 
    wtm_settings.fsetencrypt("WPA")

    exec_menu("back")
    print "\n"
    print (GR + ' ['+ G +'B'+ GR +']' + B +"  Back ")
    print (GR + ' ['+ G +'E'+ GR +']' + B +"  Exit ")
    return filename
##############
# MENU L
###############
def menuL():
    os.system("pyrit list_cores \n")
    print (GR + ' ['+ G +'B'+ GR +']' + B +"  Back ")
    print (GR + ' ['+ G +'E'+ GR +']' + B +"  Exit ")
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return

##############
# MENU G
###############
def menuG():
    print "GPU SERVER PYRIT"
 
    print (GR + ' ['+ G +'B'+ GR +']' + B +"  Back ")
    print (GR + ' ['+ G +'E'+ GR +']' + B +"  Exit ")
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


##############
# MENU P
###############
def menuP():

    print "Menu D PassWord Check!\n"
    import wtm_settings
    bssid = wtm_settings.myglobalistbssid[0]

    if bssid =='00:00:00:00:00:00':
        print R, ("No se encontro Handshake, cargar desde menu open hs")
        import time
        time.sleep(3)
        exec exec_menu("menuO")
    else:
        global rutacap
        rutacap = "./hs/"
        print("Introduce password")
        pas_char = raw_input(R + "\n")
        print(G +"Caracteres "+ pas_char + "\n")
        os.system("echo "+ pas_char +" | pyrit -r "+rutacap+filename+" -e '"+ essid +"' -b "+ bssid +" --all-handshakes --aes -i - attack_passthrough")
        print (GR + ' ['+ G +'B'+ GR +']' + B +"  Back ")
        print (GR + ' ['+ G +'E'+ GR +']' + B +"  Exit ")
        choice = raw_input(" >>  ")
        exec_menu(choice)
    return

##############
# MENU C
###############
def menuC():
    print (GR +'Calc Time Pmks \n')
    print (B + 'Introduce la velocidad de computacion pmks de tu maquina'+ W)
    mypmks = input('')
    print '\n' 
    print (B + 'Introduce el numero de combinaciones posibles' + W) 
    mylenpsswd  = float(input(''))
    print '\n' 
    rtimeseg = mylenpsswd / mypmks
    rtimemin = mylenpsswd / mypmks / 60
    rtimehor = mylenpsswd / mypmks / 60 / 60
    rtimedia = mylenpsswd / mypmks / 60 / 60 / 24
    rtimemes = mylenpsswd / mypmks / 60 / 60 / 24 / 30
    rtimeano = mylenpsswd / mypmks / 60 / 60 / 24 / 30 / 12

    print (W + 'Tiempo estimado en segundos ' + G + str(rtimeseg)+W )
    print (W + 'Tiempo estimado en minutos ' + G + str(rtimemin) +W) 
    print (W + 'Tiempo estimado en horas ' + O + str(rtimehor)+W )
    print (W + 'Tiempo estimado en dias ' + O + str(rtimedia) +W)
    print (W + 'Tiempo estimado en meses ' + R + str(rtimemes)+W )
    print (W + 'Tiempo estimado en anos ' + R + str(rtimeano) +W)
    
    print '\n'
    print (GR + ' ['+ G +'B'+ GR +']' + B +"  Back ")
    print (GR + ' ['+ G +'E'+ GR +']' + B +"  Exit ")
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


 
######################
# DEF BACK MENU
#####################
def back():
    menu_actions['main_menu']()
 
######################
# DEF EXIT MENU
#####################
def exit():
    sys.exit()
 

######################
# MENU DEFINITIONS
#####################
menu_actions = {
    'main_menu': main_menu,
    'a': menuA,
    's': menuS,
    'o': menuO,
    'l': menuL,
    'g': menuG,
    'p': menuP,
    'c': menuC,
    'b': back,
    'e': exit,
}
 
######################
# MAIN PROGRAM 
#####################
# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()


