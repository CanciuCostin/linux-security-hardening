#!/usr/bin/python
from modules.utils.PasswordExemptionsHelper import *
from modules.utils.AbstractCheck import *
from config.ChecksConfig import *
import sys
import os
sys.path.append("../..")


class Check(AbstractCheck):

    def is_anonymous_ftp_enabled(self):
        for FTPFile in CONFIG[checkFile]["FTP_FILES"]:
            try:
                with open(FTPFile,'r') as fileInput:
                    for line in fileInput:
                        if len(line) > 0 and line[0] != '#':
                            if 'anonymous_enable=NO'.upper() in line.upper() or 'guestserver' in line:
                                return False
                    return True
            except OSError:
                continue
        return True

    def run_check(self, OSName, OSVersion):
        try:
            checkFile = os.path.basename(__file__[:-3])
            if os.path.exists("/home/ftp") and any(os.path.exist(FTPFile) for FTPFile in CONFIG[checkFile]["FTP_FILES"]):
                if self.is_anonymous_ftp_enabled():
                    self.fail_check(CONFIG[checkFile]["FAIL_COMMENT"])
                else:
                    self.pass_check(CONFIG[checkFile]["PASS_COMMENT"])
            else:
                self.pass_check(CONFIG[checkFile]["PASS_COMMENT_FTP_NOT_FOUND"])
        except:
            self.handle_error(checkFile, sys.exc_info())
