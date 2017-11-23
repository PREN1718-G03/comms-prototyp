import time
from communicationvalues import CommunicationValues

# auf Raspi pip install serial

def main():
    comm = CommunicationValues()
    print 'run'
    comm.send_hello()

main()