import os
import optparse
import subprocess
from time import sleep
import re
import random

def Get_MAC(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface])
    mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))
    return mac

    
#CHECK RUFLY IF INTERFACE EXISTS FUNCTION!
def interface_check(INTERFACE_LIST, INTERFACE):
    if str(INTERFACE) in str(INTERFACE_LIST):
        return True
    else:
        return False

#GENERATING AN RANDOM MAC
def get_randommac():
    Sec = []
    GENERATED_MAC = ""
    for x in range(6):
        Sec.append(x)
        if x == 0:
            while True:               
                Sec[0] = random.randint(12, 99)
                if Sec[0] % 2 == 0:
                    GENERATED_MAC = str(Sec[0])
                    break
                else:
                    continue
        if not x == 0:
            Sec[x] = random.randint(10, 99)
            GENERATED_MAC += ":" + str(Sec[x])
    return GENERATED_MAC



def Clear():
    os.system("clear")
#Getting options of user function
def Get_Options():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="INTERFACE TO CHANGE MAC ON!")
    parser.add_option("-m", "--mac", dest="macaddres", help="ENTER MANUAL MAC! OR DONT ENTER FOR RANDOM MAC!")
    return parser.parse_args()

#Change MAC function
def Change_MAC(MAC, INTERFACE):
    try:
        print("[+] TRYING TO DISABLE " + INTERFACE + "!")
        subprocess.run("ifconfig " + INTERFACE + " down", shell=True, check=True)
        sleep(1)
    except subprocess.CalledProcessError:
        print("[-] COULDNT DISABLE " + INTERFACE + "!")
        sleep(2)
        exit(0)
    sleep(1)
    print("[+] TRYING TO CHANGE MAC TO " + str(MAC))
    sleep(1)
    try:
        subprocess.run("ifconfig " + INTERFACE + " hw ether " + MAC, shell=True, check=True)
    except subprocess.CalledProcessError:
        print("[-] COUDLNT CHANGE MAC!")
        sleep(2)
        exit(0)
    currentMAC = Get_MAC(INTERFACE)
    if currentMAC:
        print("[+] SUCCESSFULLY READ MAC!")
        sleep(1)
    else:
        print("[-] COULDNT READ MAC! PLEASE CHECK MAC MANUALLY!")
        sleep(1)
        exit()
    MAC_MATCHED = False
    if str(MAC) in str(currentMAC):
        MAC_MATCHED = True
    else:
        MAC_MATCHED = False
    if MAC_MATCHED:
        print("[+] MAC CHANGED TO " + MAC)
    else:
        print("[-] COULDNT CHANGE MAC!")
    sleep(1)
    print("[+] ENABLING " + INTERFACE + "!")
    try:
        subprocess.run("ifconfig " + INTERFACE + " up", shell=True, check=True)
    except subprocess.CalledProcessError:
        print("[-] COULDNT ENABLE " + INTERFACE)
        sleep(2)
        Clear()
        exit()

#MAIN
manual_MAC = False
(options, args) = Get_Options()
#Getting An ruff list of all the interfaces
Interface_List = subprocess.check_output("ip link", shell=True)
#Checking if user enter an interface or and manual mac
if not options.interface:
    print("[-] USE -h OR --help FOR HELP!")
    sleep(3)
    Clear()
    exit(0)
elif options.macaddres:
    manual_MAC = True
else:
    manual_MAC = False
#IF USER USED MANUAL MAC
if manual_MAC:
    if interface_check(Interface_List, options.interface):
        print("[+] INTERFACE SEEMS TO EXIST!")
        sleep(0.5)
        print("[+] TRYING TO CHANGE MAC TO " + options.macaddres)
        sleep(2)
        Change_MAC(str(options.macaddres), str(options.interface))    
    else:
        print("[-] INTERFACE DOES NOT SEEM TO EXIST!")
        sleep(2)
        exit(0)
#IF USER CHOSED RANDOM MAC
else:

    if interface_check(str(Interface_List), str(options.interface)):
        random_macc = get_randommac()
        print("[+] INTERFACE SEEMS TO EXIST")
        sleep(0.5)
        Change_MAC(random_macc, options.interface)
        sleep(2)
    else:
        print("[-] INTERFACE DOSENT SEEM TO EXIST!")
        sleep(2)
        exit(0)






    


    

