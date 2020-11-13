#!/usr/bin/python
from modules.utils.AbstractCheck import *
from config.ChecksConfig import *
import sys
import os
sys.path.append("../..")


class Check(AbstractCheck):

    def isConfigurationSet(self, OSName, OSVersion, pamFiles):
        for pamFile in pamFiles:
            isConfigSet = False
            with open(pamFile, 'r') as fileInput:
                for line in fileInput:
                    if len(line) > 0 and line[0] != '#':
                        fields = line.split()
                        if len(fields) >= 7 and all((
                            fields[0] == 'password',
                            fields[1] in CONFIG[checkFile]["PAM_CONTROLS"],
                            fields[2] in CONFIG[checkFile]["PAM_MODULES"],
                            'remember=' in line,
                            'use_authtok' in fields,
                            any(x in fields for x in CONFIG[checkFile]["HASH_ALGORITHM"]), 'shadow' in fields))
                        rememberValue = re.search(
                            'remember=(\d+)', line).group(1)
                        if rememberValue.isdigit() and int(rememberValue) >= CONFIG[checkFile]["MIN_REMEMBER"]:
                            isConfigSet = True
            if not isConfigSet:
                return False
        return True

    def run_check(self, OSName, OSVersion):
        try:
            checkFile = os.path.basename(__file__[:-3])
            if 'Red Hat' in osName or 'CentOS' in osName:
                pamFiles = CONFIG[checkFile]["PAM_FILES_RH_CENTOS"]
            else:
                pamFiles = CONFIG[checkFile]["PAM_FILES_UBUNTU_DEBIAN_SUSE"]
            if self.isConfigurationSet(OSName, OSVersion, pamFiles):
                self.pass_check(CONFIG[checkFile]["PASS_COMMENT"])
            else:
                self.fail_check(CONFIG[checkFile]["FAIL_COMMENT"])
        except:
            self.handle_error(checkFile, sys.exc_info())
