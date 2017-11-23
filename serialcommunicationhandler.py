# ================================================================================
# !/usr/bin/python
# TITLE           : serialcommunicationhandler.py
# DESCRIPTION     : Handler for serial communication with FreedomBoard
# AUTHOR          : Moro Marco I.BSCI_F14.1301 <marco.moro@stud.hslu.ch>
# DATE            : 30.01.2017
# USAGE           : comm = SerialCommunicationHandler().start()
# VERSION         : 0.1
# USAGE           :
# NOTES           :  Tx GPIO14 - BOARD-Layout: Pin8 Rx GPIO15 - BOARD-Layout: Pin10
# PYTHON_VERSION  : 3.4.2
# OPENCV_VERSION  : 3.1.0
# ================================================================================

# import the necessary packages
import logging
import serial
import queue
import time
import common.config.confighandler as cfg

from threading import Thread
from logging.config import fileConfig


class SerialCommunicationHandler(object):
    class __SerialCommunicationHandler:
        def __init__(self):
            fileConfig(cfg.get_logging_config_fullpath())
            self.__log = logging.getLogger()
            self.serialcom = None
            self.data_send = queue.Queue()
            self.data_receive = queue.Queue()
            self.__initserialcom()

        def __initserialcom(self):
            """
            This function will initialize the corresponding GPIO-Pins for serial
            """
            self.__log.info("Serial communication initialization started")
            self.serialcom = serial.Serial()
            self.serialcom.baudrate = 9600
            self.serialcom.port = '/dev/serial0'
            self.serialcom.open()

        def __txhandle(self):
            try:
                while self.serialcom.is_open:
                    time.sleep(0.05)  # wait 50ms to prevent buffer overflow on FRDM
                    while not self.data_send.empty():
                        currentqueueitem = self.data_send.get()
                        self.serialcom.write(currentqueueitem.encode('utf-8'))
                        self.__log.info("value sent: " + str(currentqueueitem.strip('\n')))
                else:
                    self.__reconnectcommunication()
            except serial.SerialException as e:
                self.__log.error("serial connection lost..." + str(e.strerror))
                if self.serialcom.is_open():
                    self.__reconnectcommunication()

        def __rxhandle(self):
            try:
                while self.serialcom.is_open:
                    time.sleep(0.01)  # wait 10ms to retrieve next value to reduce CPU load
                    currentreceiveitem = self.serialcom.readline()
                    currentqueueitem_op, currentqueueitem_value = self.__encodestring(currentreceiveitem)
                    self.data_receive.put([currentqueueitem_op, currentqueueitem_value])
                    self.__log.debug("value received: " + str(currentqueueitem_op) + "," + str(currentqueueitem_value))
                else:
                    self.__reconnectcommunication()
            except serial.SerialException as e:
                self.__log.error("serial connection lost..." + str(e))
                if self.serialcom.is_open:
                    self.__reconnectcommunication()

        def __reconnectcommunication(self):
            self.start()

        def send(self, operation, value):
            decodedvalue = self.__decodestring(operation, value)
            self.data_send.put(decodedvalue + '\n')

        def receive(self):
            operation, opval = self.data_receive.get()
            return operation, opval

        def start(self):
            t_read = Thread(target=self.__rxhandle, args=())
            t_write = Thread(target=self.__txhandle, args=())
            t_read.daemon = True
            t_write.daemon = True
            t_read.start()
            t_write.start()
            return self

        def __encodestring(self, inputvalue):
            try:
                operation, opval = inputvalue.split(b',')
                operation = operation.decode()
                opval = opval.decode()
                return operation.rstrip(), opval.rstrip()
            except:
                self.__log.debug("org: " + str(inputvalue))
                return "ERROR", "ERROR"

        def __decodestring(self, operation, opval):
            combinedvalue = operation + "," + str(opval)
            return combinedvalue

    instance = None

    def __new__(cls, *args, **kwargs):
        if not SerialCommunicationHandler.instance:
            SerialCommunicationHandler.instance = SerialCommunicationHandler.__SerialCommunicationHandler()
        return SerialCommunicationHandler.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
return setattr(self.instance, name)