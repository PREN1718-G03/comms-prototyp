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

#import config.confighandler as cfg
#from logging.config import fileConfig
from threading import Thread
from serialcommunicationhandler import SerialCommunicationHandler


class CommunicationValues:
    class __CommunicationValues:
        def __init__(self):
            #fileConfig(cfg.get_logging_config_fullpath())
            self.__log = logging.getLogger()
            self.op_hello = None
            self.op_state = None
            self.op_position = "None"
            self.__serialcomm = None
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
                    self.__log.error("timeout hello blocking...")
                    break
            return self.op_hello

        def get_hello(self):
            return self.op_hello

        def send_hello(self):
            self.__serialcomm.send("hello", 1)
            hellocounter = 0
            while self.op_hello is None:
                if hellocounter < self.retrycounter:
                    time.sleep(self.timeout)
                    self.__serialcomm.send("hello", 1)
                    hellocounter += 1
                else:
                    self.__log.error("hello message not acknowledged")
                    break

        def send_state(self):
            self.__serialcomm.send("state", 1)
            statecounter = 0
            while self.op_start is None:
                if statecounter < self.retrycounter:
                    time.sleep(self.timeout)
                    self.__serialcomm.send("start", 1)
                    statecounter += 1
                else:
                    self.__log.error("state signal not acknowledged")
                    break

        def send_position(self, position):
            self.__serialcomm.send("position", position)
            positioncounter = 0
            while self.op_course is None:
                if positioncounter < self.retrycounter:
                    time.sleep(self.timeout)
                    self.__serialcomm.send("position", position)
                    positioncounter += 1
                else:
                    self.__log.error("position not acknowledged")
                    break

        def __handleoperations(self):
            while True:
                operation, value = self.__serialcomm.receive()
                self.__log.info("got op:" + str(operation) + " val: " + str(value))
                if operation == "hello":
                    if value == '1':
                        self.op_hello = 1
                elif operation == "state":
                    if value == '1':
                        self.op_start = 1
                elif operation == "position":
                    self.op_course = str(value)
                else:
                    self.__log.debug("got unknown operation: " + str(operation) + " with val: " + str(value))

        def __start(self):
            self.__serialcomm = SerialCommunicationHandler().start()
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