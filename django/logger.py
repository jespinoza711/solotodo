"""
Capture print statments and write them to a log file
but still allow them to be printed on the screen.
"""

import sys
import time
from solonotebooks import settings

class Logger:
    def __init__(self, stdout, filename):
        self.stdout = stdout
        self.logfile = file(filename, 'w')
        self.logfile.write('Hora de registro: %s\n\n' % time.ctime())
    def write(self, text):
        self.stdout.write(text)
        self.logfile.write(text)
        self.logfile.flush()
    def close(self):
        """Does this work or not?"""
        self.stdout.close()
        self.logfile.close()
        
    def change_log_file(self, new_file):
        #self.logfile.close()
        self.logfile = file(new_file, 'w')
        self.logfile.write('Hora de registro: %s\n\n' % time.ctime())
        
    def default_stdout(self):
        return self.stdout
