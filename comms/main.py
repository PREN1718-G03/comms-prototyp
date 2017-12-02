import time

# from communicationvalues import CommunicationValues

# auf Raspi pip install serial
from comms.communicationvalues import CommunicationValues


class testibus():
    def __init__(self):
        self.serialcom = None
        print("startibus")
        self.los()

    def los(self):
        self.serialcom = CommunicationValues()
        print("run")
        self.serialcom.send_hello()
        hellostate = self.serialcom.get_hello_blocking()  # await hello response or timeout...

        if hellostate == '1' or hellostate == 1:
            print("serial communication established!")
        else:
            print("not able to setup communication with Freedom-Board!!")


if __name__ == '__main__':
    testibus()
    # keep alive till poweroff
    while True:
        pass
