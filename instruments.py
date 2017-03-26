# -*- coding: utf-8 -*-
"""
Define a class for each instrument.
An instance of the class can be called in experiment scripts (see 'measure.py')

    Delta_Mode: Sets up a Keithley 6220 current source and 2182A nanovoltmeter in 'Delta Mode'
    
    Magnet:     Not yet done - will set up a GMW electromagnet

@author: ludbroba
"""

#  test = Delta_Mode("GPIB0::12::INSTR")

import visa
import time, math

class Delta_Mode():
    
    """ This class handles the Keithley 6220 (and 2182A through serial) in Delta mode
        Call it with delta = Delta_Mode("GPIB0::12::INSTR")
    """

    def __init__(self,visa_name):
        """ Connects to the Keithley 6220 (and 2182A through serial) in Delta mode

        Connects to Delta, and checks the identity of the two components, and
        checks that the 2182A is connected.
        Arguments:
          visa_name -- A Visa Resource ID, like "GPIB0::12::INSTR"
        """
        rm = visa.ResourceManager()
        self.delta = rm.open_resource(visa_name)

        print(self.delta.query('*IDN?'))       
        self.nanovoltmeter_check()

    def nanovoltmeter_check(self):
        
        """ Checks that the K2182A nanovoltmeter is connected"""
        
        if int(self.delta.query("SOUR:DELT:NVPR?")):
            print("2182A connected")
        else:
            raise RuntimeError('nanovoltmeter not found')
            
    def write(self,string):
        
        """Write string to DM instance """        
        
        self.delta.write(string)
        
    def read(self):        
        """ Read string from DM instance """              
        return self.delta.read()
        
    def ask(self,string):        
        """ Ask. """
        resp = self.delta.query(string)
        return resp

    def write_serial(self,string):    
        """Sends a message to Keithley current source that is passed to
           voltmeter through a serial connection """    
        self.write("SYST:COMM:SER:SEND \"{}\"".format(string))
        time.sleep(0.1)
    
    def read_serial(self):
    
        """Reads data from 2182A through 6220"""
    
        self.write("SYST:COMM:SER:ENT?")
        return self.read()
    
    def ask_serial(self,string):
    
        """A combination of write_serial(message) and read
           specific to Keithley current source and voltmeter"""
    
        self.write_serial(string)
        self.write("SYST:COMM:SER:ENT?")
        return self.read()        
            
    def _test(self,test_time):
        
        """ Runs a delta mode measurement for 'test_time' then aborts."""        
        
        self.write("*RST")
        self.write("SOUR:DELT:HIGH 1e-4")
        self.write("SOUR:DELT:DELay 100e-3")
        self.write("SOUR:DELT:COUN 1000")
        self.write("SOUR:DELT:CAB ON")
        self.write("TRAC:POIN 1000")
        self.write("SOUR:DELT:ARM")
        self.write("INIT:IMM")
        time.sleep(test_time)
        self.write("SOUR:SWE:ABOR")

   
        

class Magnet():
    
    """ Class to run the GMW electromagnet. """
    pass

