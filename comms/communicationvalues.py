# ================================================================================
# !/usr/bin/python
# TITLE           : communicationvalues.py
# DESCRIPTION     : Operational commands and values for serial communication
# AUTHOR          : Eve Meier <eve.meier@stud.hslu.ch>
# DATE            : 23.11.2017
# USAGE           :
# VERSION         : 0.1
# USAGE           :
# NOTES           :
# PYTHON_VERSION  :
# OPENCV_VERSION  :
# ================================================================================

# import the necessary packages
import logging
import time

# import config.confighandler as cfg
# from logging.config import fileConfig
from threading import Thread
from serialcommunicationhandler import SerialCommunicationHandler


class CommunicationValues:
    class __CommunicationValues:
        def __init__(self):
            # fileConfig(cfg.get_logging_config_fullpath())
            # self.__log = logging.getLogger()
            print("CommunicationValues init")
            self.op_hello = None
            self.op_state = None
            self.op_position = "None"
            self.__serialcom = None
            self.timeout = 0.3
            self.retrycounter = 20
            time.sleep(1)
            self.__start()

        def get_hello_blocking(self):
            hellocounter = 0
            while self.op_hello is None:
                if hellocounter < self.retrycounter:
                    time.sleep(self.timeout)
                    hellocounter += 1
                else:
                    print("timeout hello blocking...")
                    break
            return self.op_hello

        def get_hello(self):
            return self.op_hello

        def get_state(self):
            return self.op_state

        def get_position(self):
            return self.op_position

        def send_hello(self):
            self.__serialcom.send("hello", 1)
            hellocounter = 0
            while self.op_hello is None:
                if hellocounter < self.retrycounter:
                    time.sleep(self.timeout)
                    self.__serialcom.send("hello", 1)
                    hellocounter += 1
                else:
                    print("hello message not acknowledged")
                    break

        def send_state(self):
            self.__serialcom.send("state", 1)
            statecounter = 0
            while self.op_state is None:
                if statecounter < self.retrycounter:
                    time.sleep(self.timeout)
                    self.__serialcom.send("state", 1)
                    statecounter += 1
                else:
                    print("state signal not acknowledged")
                    break

        def send_position(self, position):
            self.__serialcom.send("position", position)
            positioncounter = 0
            while self.op_position is None:
                if positioncounter < self.retrycounter:
                    time.sleep(self.timeout)
                    self.__serialcom.send("position", position)
                    positioncounter += 1
                else:
                    print("position not acknowledged")
                    break

        def __handleoperations(self):
            while True:
                operation, value = self.__serialcom.receive()
                print("got op:" + str(operation) + " val: " + str(value))
                if operation == "hello":
                    if value == '1':
                        self.op_hello = 1
                elif operation == "state":
                    if value == '1':
                        self.op_state = 1
                elif operation == "position":
                    self.op_position = str(value)
                else:
                    print("got unknown operation: " + str(operation) + " with val: " + str(value))

        def __start(self):
            self.__serialcom = SerialCommunicationHandler().start()
            thread = Thread(target=self.__handleoperations, args=())
            thread.daemon = True
            thread.start()
            return self


    instance = None


    def __new__(cls, *args, **kwargs):
        if CommunicationValues.instance is None:
            CommunicationValues.instance = CommunicationValues.__CommunicationValues()
        return CommunicationValues.instance


    def __getattr__(self, name):
        return getattr(self.instance, name)


    def __setattr__(self, name):
        return setattr(self.instance, name)
