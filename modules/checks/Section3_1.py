#!/usr/bin/python
from modules.utils.PasswordExemptionsHelper import *
from modules.utils.AbstractCheck import *
from config.ChecksConfig import *
import sys
import os
sys.path.append("../..")


class Check(AbstractCheck):

    def getLogModuleParams(self, OSName, OSVersion, checkFile):
        if 'Red Hat' in OSName or 'CentOS' in OSName:
            syslogRequirements=CONFIG[checkFile]["REQUIREMENTS_REDHAT_SYSLOG"]
            rsyslogRequirements=CONFIG[checkFile]["REQUIREMENTS_REDHAT_RSYSLOG"]
            syslogngRequirements=CONFIG[checkFile]["REQUIREMENTS_REDHAT_SYSLOGNG"]
        elif 'Ubuntu' in OSName or 'Debian' in OSName:
            syslogRequirements=CONFIG[checkFile]["REQUIREMENTS_UBUNTU_DEBIAN_SYSLOG"]
            rsyslogRequirements=CONFIG[checkFile]["REQUIREMENTS_UBUNTU_DEBIAN_RSYSLOG"]
            syslogngRequirements=CONFIG[checkFile]["REQUIREMENTS_UBUNTU_DEBIAN_SYSLOGNG"]
        else:
            syslogRequirements=CONFIG[checkFile]["REQUIREMENTS_SUSE_SYSLOG"]
            rsyslogRequirements=CONFIG[checkFile]["REQUIREMENTS_SUSE_RSYSLOG"]
            syslogngRequirements=CONFIG[checkFile]["REQUIREMENTS_SUSE_SYSLOGNG"]

        if os.path.isfile(CONFIG[checkFile]["SYSLOG-NG_FILE"]):
            requirements = syslogngRequirements
            logFiles=[CONFIG[checkFile]["SYSLOG-NG_FILE"]]
        elif os.path.isfile(CONFIG[checkFile]["RSYSLOG_FILE"]):
            requirements = rsyslogRequirements
            logFiles=[CONFIG[checkFile]["RSYSLOG_FILE"] + glob.glob(CONFIG[checkFile]["RSYSLOG_DIR"])
        elif os.path.isfile(CONFIG[checkFile]["SYSLOG_FILE"]):
            requirements = syslogRequirements
            logFiles=[CONFIG[checkFile]["SYSLOG_FILE"])
        return logFiles, requirements

    def run_check(self, OSName, OSVersion):
        try:
            checkFile = os.path.basename(__file__[:-3])
            logFiles,requirements=self.getLogModuleParams(OSName,OSVersion,checkFile)
            lines=list()
            for logFile in logFiles:
                with open(logFile, 'r') as fileInput:
                    for line in fileInput:
                        if len(line) > 0 and line != '#':
                            lines.append(line)
            linesParams=list(map(lambda x: x.split(),lines))
            if all(x in linesParams for x in requirements):
                self.pass_check(CONFIG[checkFile]["PASS_COMMENT"])
            else:
                self.fail_check(CONFIG[checkFile]["FAIL_COMMENT"])
        except:
            self.handle_error(checkFile, sys.exc_info())
