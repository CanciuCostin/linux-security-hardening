#!/usr/bin/python
from modules.utils.PasswordExemptionsHelper import *
from modules.utils.AbstractCheck import *
from config.ChecksConfig import *
import sys
import os
sys.path.append("../..")


class Check(AbstractCheck):

    def isModuleUsed(self,moduleName):
        for directory in CONFIG[checkFile]["LIBS_PATHS"]:
                if os.path.exists(directory):
                    files=os.listdir(directory)
                    for fileName in files:
                        if fileName == moduleName:
                            return True
        return False


    def run_check(self, OSName, OSVersion):
        try:
            checkFile = os.path.basename(__file__[:-3])
            if isModuleUsed('pam_tally2.so'):
                if os.path.isfile(CONFIG[checkFile]["TALLY_FILE"]):
                    self.pass_check(CONFIG[checkFile]["PASS_COMMENT"])
                else:
                    self.fail_check(CONFIG[checkFile]["FAIL_COMMENT"])
            else:
                self.pass_check(CONFIG[checkFile]["PASS_COMMENT_TALLY2"])
        except:
            self.handle_error(checkFile, sys.exc_info())
