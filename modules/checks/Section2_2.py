#!/usr/bin/python
from modules.utils.PasswordExemptionsHelper import *
from modules.utils.AbstractCheck import *
from config.ChecksConfig import *
import sys
import os
sys.path.append("../..")


class Check(AbstractCheck):
    def usersToString(self, usersDict):
        return '\n'.join([x[0]
                    + ":"
                    + str(x[1]['maxAge'])
                    + ' Is Exempted: '
                    + x[1]['isUserExempted'] for x in usersDict.items()])

    def get_users_info(self, checkFile, passwordExemptionsHelper):
        users = dict()
         with open(CONFIG[checkFile]["SHADOW_FILE"], 'r') as fileInput:
              for line in fileInput:
                   try:
                        line = line.strip()
                        if len(line) > 0 and not line.startswith('#'):
                            fields = line.split(":")
                            if len(fields) >= 5:
                                user = dict()
                                user["maxAge"] = int(
                                    fields[4]) if fields[4].isdigit() else -1
                                user["isUserExempted"] = 'Yes' if passwordExemptionsHelper.isUserExempted(
                                    fields[0]) else 'No'
                    except:
                        print("Error reading pass max age info for line: " + line)
                        continue
        return users

    def run_check(self, OSName, OSVersion):
        try:
            checkFile = os.path.basename(__file__[:-3])
            passwordExemptionsHelper = PasswordExemptionsHelper()
            users = self.get_users_info(checkFile, passwordExemptionsHelper)
            failedUsers = dict(filter(lambda x:
                                        x[1]["isUserExempted"] == 'No'
                                        and not x[1]["maxAge"] in range (1, CONFIG[checkFile]["PASS_MAX_AGE"] + 1), users.items()))
            if len(failedUsers) == 0:
                self.pass_check(CONFIG[checkFile]["PASS_COMMENT"] + self.usersToString(users)
            else:
                self.fail_check(CONFIG[checkFile]["FAIL_COMMENT"] + self.usersToString(failedUsers))
        except:
            self.handle_error(checkFile, sys.exc_info())
