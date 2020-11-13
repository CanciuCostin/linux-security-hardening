#!/usr/bin/python
from modules.utils.PasswordExemptionsHelper import *
from modules.utils.AbstractCheck import *
from config.ChecksConfig import *
import sys
import os
sys.path.append("../..")


class Check(AbstractCheck):

    def is_policy_set(self):
        isAuthSet,isAccountSet=False,False
        with open(CONFIG[checkFile]["PAM_OTHER"],'r') as fileInput:
            for line in fileInput:
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    fields = line.split()
                    if len(fields) >= 3:
                        if fields[0] == 'auth' and fields[1] == 'required' and 'pam_deny.so' in fields[2]:
                            isAuthSet=True
                        if fields[0] == 'account' and fields[1] == 'required' and 'pam_deny.so' in fields[2]:
                            isAccountSet=True

        return True if isAuthSet and isAccountSet else False


    def run_check(self, OSName, OSVersion):
        try:
            checkFile = os.path.basename(__file__[:-3])
            if self.is_policy_set():
                self.pass_check(CONFIG[checkFile]["PASS_COMMENT"])
            else:
                self.fail_check(CONFIG[checkFile]["FAIL_COMMENT"])
        except:
            self.handle_error(checkFile, sys.exc_info())
