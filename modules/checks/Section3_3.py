#!/usr/bin/python
from modules.utils.PasswordExemptionsHelper import *
from modules.utils.AbstractCheck import *
from config.ChecksConfig import *
import sys
import os
sys.path.append("../..")


class Check(AbstractCheck):


    def run_check(self, OSName, OSVersion):
        try:
            checkFile = os.path.basename(__file__[:-3])
            if 'Ubuntu' in osName or 'Debian' in osName:
                logFile=CONFIG[checkFile]["SYSLOG_FILE"]
            else:
                logFile=CONFIG[checkFile]["MESSAGES_FILE"]
            if os.path.isfile(logFile):
                self.pass_check(CONFIG[checkFile]["PASS_COMMENT"])
            else:
                self.fail_check(CONFIG[checkFile]["FAIL_COMMENT"])
        except:
            self.handle_error(checkFile, sys.exc_info())
