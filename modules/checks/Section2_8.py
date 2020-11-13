#!/usr/bin/python
from modules.utils.PasswordExemptionsHelper import *
from modules.utils.AbstractCheck import *
from config.ChecksConfig import *
import sys
import os
sys.path.append("../..")


class Check(AbstractCheck):

    def areIdsUnique(self, idsDict):
        reverseDict = dict()
        for key, value in idsDict.items():
            if not value in reverseDict:
                reverseDict[value] = list()
            reverseDict[value].append(key)
        for idKey in reverseDict.keys():
            if len(reverseDict[idKey]) > 1:
                duplicateUserIds[idKey] = reverseDict[idKey]
        return True if len(duplicateUserIds) == 0 else False
        

    def areUserIdsUnique(self):
        with open(CONFIG[checkFile]["PASSWD_FILE"], 'r') as fileInput:
            for line in fileInput:
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    fields = line.split(":")
                    if len(fields) >= 5:
                        users[fields[0]] = fields[2]
        return True if self.areIdsUnique(users)

    def areGroupIdsUnique(self):
        with open(CONFIG[checkFile]["GROUP_FILE"], 'r') as fileInput:
            for line in fileInput:
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    fields = line.split(":")
                    if len(fields) >= 4:
                        groups[fields[0]] = fields[2]
        return True if self.areIdsUnique(groups) else False

    def run_check(self, OSName, OSVersion):
        try:
            checkFile = os.path.basename(__file__[:-3])
            if self.areUserIdsUnique():
                self.pass_check(CONFIG[checkFile]["PASS_COMMENT_USERS"])
            else:
                self.fail_check(CONFIG[checkFile]["FAIL_COMMENT_USERS"])
            if self.areGroupIdsUnique():
                self.pass_check(CONFIG[checkFile]["PASS_COMMENT_GROUPS"])
            else:
                self.fail_check(CONFIG[checkFile]["FAIL_COMMENT_GROUPS"])
        except:
            self.handle_error(checkFile, sys.exc_info())
