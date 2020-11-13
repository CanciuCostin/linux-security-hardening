#!/usr/bin/python
from modules.utils.AbstractCheck import *
from config.ChecksConfig import *
import sys
import os
sys.path.append("../..")


class Check(AbstractCheck):

    def isAccountSet(self, pamFile):
        with open(pamFile, 'r') as fileInput:
            for line in fileInput:
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    fields = line.split()
                    if len(fields) >= 3
                    and 'account' in fileName:
                        if fields[0] == 'account'
                        and fields[1] == 'required'
                        and fields[2] in pam_tally_module:
                            return True
        return False

    def isAuthSet(self, pamFile):
        isFieldsValueCorrect = False
        for fileName in CONST_TEST_FILES_REDHAT:
            with open(fileName, 'r') as fileInput:
                for line in fileInput:
                    line = line.strip()
                    if len(line) > 0 and line[0] != '#':
                        fields = line.split()
                        if len(fields) >= 4:
                            if fields[0] == 'auth'
                            and fields[1] == 'required'
                            and fields[2] in CONFIG[checkFile]["PAM_MODULES"]:
                                if 'deny=' in ''.join(fields):
                                    denyValue = re.search(
                                        'deny=(\d+)', line).group(1)
                                    if denyValue.isdigit()
                                    and int(denyValue) <= CONFIG[checkFile]["MAX_RETRIES"]:
                                        return True
        return False

    def run_check(self, OSName, OSVersion):
        try:
            checkFile = os.path.basename(__file__[:-3])
            if 'Red Hat' in osName or 'CentOS' in osName:
                pamFiles = CONFIG[checkFile]["PAM_FILES_RH_CENTOS"]
                if self.isAuthSet(pamFiles[0]) and self.isAuthSet(pamFiles[1]):
                    self.pass_check(CONFIG[checkFile]["PASS_COMMENT_AUTH"])
                else:
                    self.fail_check(CONFIG[checkFile]["FAIL_COMMENT_AUTH"])
                if self.isAccountSet(pamFiles[0]) and self.isAccountSet(pamFiles[1]):
                    self.pass_check(CONFIG[checkFile]["PASS_COMMENT_ACCOUNT"])
                else:
                    self.fail_check(CONFIG[checkFile]["FAIL_COMMENT_ACCOUNT"])
            else:
                authFile, accountFile = *CONFIG[checkFile]["PAM_FILES_UBUNTU_DEBIAN_SUSE"]
                if self.isAuthSet(authFile):
                    self.pass_check(CONFIG[checkFile]["PASS_COMMENT_AUTH"])
                else:
                    self.fail_check(CONFIG[checkFile]["FAIL_COMMENT_AUTH"])
                if self.isAccountSet(authFile):
                    self.pass_check(CONFIG[checkFile]["PASS_COMMENT_ACCOUNT"])
                else:
                    self.fail_check(CONFIG[checkFile]["FAIL_COMMENT_ACCOUNT"])
        except:
            self.handle_error(checkFile, sys.exc_info())
