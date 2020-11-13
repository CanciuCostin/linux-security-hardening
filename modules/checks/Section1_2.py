#!/usr/bin/python
from modules.utils.AbstractCheck import *
from config.ChecksConfig import *
import sys
sys.path.append("../..")


class Check(AbstractCheck):

    def run_check(self, OSName, OSVersion):
        try:
            checkFile = os.path.basename(__file__[:-3])
            motdFiles = CONFIG[checkFile]["MOTD_FILES"]
            if os.path.islink('/etc/motd'):
                linkPath = os.path.realpath('/etc/motd')
            if linkPath == '/var/run/motd':
                motdFiles[0] = '/etc/motd.tail'
            for fileName in motdFiles:
                try:
                    with open(fileName, 'r') as fileInput:
                        for line in fileInput:
                            if not line.startswith('#') and CONFIG[checkFile]["MOTD"] in line:
                                self.pass_check(
                                    CONFIG[checkFile]["PASS_COMMENT"])
                                return
                except OSError:
                    continue
            self.fail_check(CONFIG[checkFile]["FAIL_COMMENT_UNKNOWN"])
        except:
            self.handle_error(checkFile, sys.exc_info())
