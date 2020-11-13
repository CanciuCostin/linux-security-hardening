#!/usr/bin/python
import sys
import os
sys.path.append("../..")
from config.ChecksConfig import *
from modules.utils.AbstractCheck import *

class Check(AbstractCheck):
    def run_check(self, OSName, OSVersion):
        try:
            checkFile=os.path.basename(__file__[:-3])
            with open(CONFIG[checkFile]["LOGIN_DEFS"], 'r') as fileInput:
                for line in fileInput:
                    if len(line) > 0 and not line.startswith('#'):
                        fields = line.split()
                        if len(fields) >= 2:
                            if fields[0] == 'PASS_MIN_DAYS':
                                if int(fields[1]) >= CONFIG[checkFile]["PASS_MIN_AGE"]:
                                    self.pass_check(CONFIG[checkFile]["PASS_COMMENT"])
                                else:
                                    self.fail_check(CONFIG[checkFile]["FAIL_COMMENT"])
                                return                            
        except:
            self.handle_error(checkFile, sys.exc_info())
