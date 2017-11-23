# ================================================================================
# !/usr/bin/python
# TITLE           : communicationvalues.py
# DESCRIPTION     : Operational commands and values for serial communication
# AUTHOR          : Moro Marco I.BSCI_F14.1301 <marco.moro@stud.hslu.ch>
# DATE            : 30.01.2017
# USAGE           :
# VERSION         : 0.1
# USAGE           :
# NOTES           :
# PYTHON_VERSION  : 3.4.2
# OPENCV_VERSION  : 3.1.0
# ================================================================================

# import the necessary packages
import logging
import time

import common.config.confighandler as cfg
from threading import Thread
from logging.config import fileConfig
from common.communication.serialcommunicationhandler import SerialCommunicationHandler


class CommunicationValues:
    class __CommunicationValues:
        def __init__(self):
            fileConfig(cfg.get_logging_config_fullpath())
            self.__log = logging.getLogger()
            self.op_hello = None
            self.op_start = None
            self.op_course = None
            self.op_tof_l_i = 0
            self.op_tof_l_s = 0
            self.op_tof_r_i = 0
            self.op_tof_r_s = 0
            self.op_tof_f_i = 0
            self.op_tof_f_s = 0
            self.op_raupe_l_i = 0
            self.op_raupe_l_s = 0
            self.op_raupe_r_i = 0
            self.op_raupe_r_s = 0
            self.op_gyro_n = 0
            self.op_gyro_g = 0
            self.op_gyroskop_i = 0
            self.op_gyroskop_s = 0
            self.op_servo_s = 0
            self.op_servo_i = 0
            self.op_kpG = 0
            self.op_kiG = 0
            self.op_kdG = 0
            self.op_kpT = 0
            self.op_kiT = 0
            self.op_kdT = 0
            self.op_letter = None
            self.op_parcstate = None
            self.op_errstate = "None"
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

        def get_course_blocking(self):
            coursecounter = 0
            while self.op_course is None:
                if coursecounter < self.retrycounter:
                    time.sleep(self.timeout)
                    coursecounter += 1
                else:
                    self.__log.error("timeout hello blocking...")
                    break
            return self.op_course

        def get_hello(self):
            return self.op_hello

        def get_start(self):
            return self.op_start

        def get_course(self):
            return self.op_course

        def get_tof_left(self):
            return self.op_tof_l_i

        def get_tof_right(self):
            return self.op_tof_r_i

        def get_tof_front(self):
            return self.op_tof_f_i

        def get_raupe_left(self):
            return self.op_raupe_l_i

        def get_raupe_right(self):
            return self.op_raupe_r_i

        def get_gyro_n(self):
            return self.op_gyro_n

        def get_gyro_g(self):
            return self.op_gyro_g

        def get_gyroskop(self):
            return self.op_gyroskop_i

        def get_servo(self):
            return self.op_servo_i

        def get_letter(self):
            return self.op_letter

        # PiD Werte
        # k Konstante, p Proportional, i Integral, d Differenzial, G Gyro, T ToF
        def get_kpG(self):
            return self.op_kpG

        def get_kiG(self):
            return self.op_kiG

        def get_kdG(self):
            return self.op_kdG

        def get_kpT(self):
            return self.op_kpT

        def get_kiT(self):
            return self.op_kiT

        def get_kdT(self):
            return self.op_kdT

        def get_parcstate(self):
            return self.op_parcstate

        def get_error(self):
            return self.op_errstate

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

        def send_start(self):
            self.__serialcomm.send("start", 1)
            startcounter = 0
            while self.op_start is None:
                if startcounter < self.retrycounter:
                    time.sleep(self.timeout)
                    self.__serialcomm.send("start", 1)
                    startcounter += 1
                else:
                    self.__log.error("start signal not acknowledged")
                    break

        def send_course(self, course):
            self.__serialcomm.send("course", course)
            coursecounter = 0
            while self.op_course is None:
                if coursecounter < self.retrycounter:
                    time.sleep(self.timeout)
                    self.__serialcomm.send("course", course)
                    coursecounter += 1
                else:
                    self.__log.error("course selection not acknowledged")
                    break

        def send_letter(self, detectedletter):
            self.__serialcomm.send("letter", detectedletter)
            lettercounter = 0
            while self.op_letter is None:
                if lettercounter < self.retrycounter:
                    time.sleep(self.timeout)
                    self.__serialcomm.send("letter", detectedletter)
                    lettercounter += 1
                else:
                    self.__log.error("letter not acknowledged")
                    break

        def send_tof_left(self, value):
            if self.op_tof_l_s != value:
                value = int(value)
                if value < 0:
                    value = 0
                elif value > 600:
                    value = 600
                self.__serialcomm.send("tof_l_s", value)

        #Depricated, we only send left
        def send_tof_right(self, value):
            if self.op_tof_r_s != value:
                value = int(value)
                if value < 0:
                    value = 0
                elif value > 600:
                    value = 600
                self.__serialcomm.send("tof_r_s", value)

        def send_tof_front(self, value):
            if self.op_tof_f_s != value:
                value = int(value)
                if value < 0:
                    value = 0
                elif value > 600:
                    value = 600
                self.__serialcomm.send("tof_f_s", value)

        def send_raupe_left(self, value):
            if self.op_raupe_l_s != value:
                value = int(value)
                if value < -100:
                    value = -100
                elif value > 100:
                    value = 100
                value = int(value / 100 * 127)
                self.__serialcomm.send("raupe_l_s", value)

        #Depricated, we only send left
        def send_raupe_right(self, value):
            if self.op_raupe_r_s != value:
                value = int(value)
                if value < -100:
                    value = -100
                elif value > 100:
                    value = 100
                value = int(value / 100 * 127)
                self.__serialcomm.send("raupe_r_s", value)

        def send_gyroskop(self, value):
            if self.op_gyroskop_s != value:
                value = int(value)
                if value < 0:
                    value = 0
                elif value > 100:
                    value = 100
                value = int(value / 100 * 127)
                self.__serialcomm.send("gyroskop_s", value)

        def send_servo(self, value):
            if self.op_servo_s != value:
                value = int(value)
                if value < 0:
                    value = 0
                elif value > 180:
                    value = 180
                self.__serialcomm.send("servo_s", value)

        def send_kpG(self, value):
            if self.op_kpG != value:
                value = int(value)
                if value < 0:
                    value = 0
                elif value > 255:
                    value = 255
                self.op_kpG = value
                self.__serialcomm.send("kpG", value)

        def send_kiG(self, value):
            if self.op_kiG != value:
                value = int(value)
                if value < 0:
                    value = 0
                elif value > 255:
                    value = 255
                self.op_kiG = value
                self.__serialcomm.send("kiG", value)

        def send_kdG(self, value):
            if self.op_kdG != value:
                value = int(value)
                if value < 0:
                    value = 0
                elif value > 255:
                    value = 255
                self.op_kdG = value
                self.__serialcomm.send("kdG", value)

        def send_kpT(self, value):
            if self.op_kpT != value:
                value = int(value)
                if value < 0:
                    value = 0
                elif value > 255:
                    value = 255
                self.op_kpT = value
                self.__serialcomm.send("kpT", value)

        def send_kiT(self, value):
            if self.op_kiT != value:
                value = int(value)
                if value < 0:
                    value = 0
                elif value > 255:
                    value = 255
                self.op_kiT = value
                self.__serialcomm.send("kiT", value)

        def send_kdT(self, value):
            if self.op_kdT != value:
                value = int(value)
                if value < 0:
                    value = 0
                elif value > 255:
                    value = 255
                self.op_kdT = value
                self.__serialcomm.send("kdT", value)

        def send_error(self, value):
            if self.op_errstate != value:
                self.__serialcomm.send("errstate", value)

        def __handleoperations(self):
            while True:
                operation, value = self.__serialcomm.receive()
                self.__log.info("got op:" + str(operation) + " val: " + str(value))
                if operation == "hello":
                    if value == '1':
                        self.op_hello = 1
                elif operation == "start":
                    if value == '1':
                        self.op_start = 1
                elif operation == "course":
                    self.op_course = str(value)
                elif operation == "tof_l_i":
                    self.op_tof_l_i = value
                elif operation == "tof_r_i":
                    self.op_tof_r_i = value
                elif operation == "tof_f_i":
                    self.op_tof_f_i = value
                elif operation == "raupe_l_i":
                    value = int(int(value) / 127 * 100)
                    self.op_raupe_l_i = value
                elif operation == "raupe_r_i":
                    value = int(int(value) / 127 * 100)
                    self.op_raupe_r_i = value
                elif operation == "gyro_n":
                    self.op_gyro_n = value
                elif operation == "gyro_g":
                    self.op_gyro_g = value
                elif operation == "gyroskop_i":
                    value = int(int(value) / 127 * 100)
                    self.op_gyroskop_i = value
                elif operation == "servo_i":
                    self.op_servo_i = value
                elif operation == "letter":
                    self.op_letter = value
                elif operation == "parcstate":
                    self.op_parcstate = value
                elif operation == "errstate":
                    self.op_errstate = value
                    if value != '0':
                        self.__log.error("got error from FRDM: " + value)
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