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
                            if fields[0] == 'PASS_MAX_DAYS' and int(fields[1]) in range(1, CONFIG[checkFile]["PASS_MAX_AGE"] + 1):
                                self.fail_check(CONFIG[checkFile]["FAIL_COMMENT"])
                                return
            self.pass_check(CONFIG[checkFile]["PASS_COMMENT"])
        except:
            self.handle_error(checkFile, sys.exc_info())
