#!/usr/bin/python
from modules.utils.PasswordExemptionsHelper import *
from modules.utils.AbstractCheck import *
from config.ChecksConfig import *
import sys
import os
sys.path.append("../..")


class Check(AbstractCheck):

    def getDefaultLogRotation(self):
        try:
            logPeriod='daily'
            logRetention=1
            with open('/etc/logrotate.conf','r') as fileInput:
                lines=fileInput.readlines()
            i=0
            while i < len(lines):
                if '{' in lines[i]:
                    while '}' not in lines[i]:
                        i+=1
                if any(x in lines[i] for x in ['hourly','daily','monthly','yearly','weekly']) and not lines[i].startswith('#'):
                    logPeriod = lines[i].strip()
                if 'rotate ' in lines[i] and not lines[i].startswith('#'):
                    logRetention = int(lines[i].strip().split()[1])
                i+=1
            return logRetention,logPeriod
        except:
            return None

    def getLogRotation(self,defaultPeriod,defaultRotate,rotationFileName):
        try:
            logRetention=defaultRotate
            logPeriod=defaultPeriod
            for file in ['/etc/logrotate.conf'] + list(map(lambda x : '/etc/logrotate.d/' + x, os.listdir('/etc/logrotate.d'))):
                lines=[]
                with open(file,'r') as fileInput:
                    lines=fileInput.readlines()
                i=0
                while i < len(lines):
                    if rotationFileName in lines[i] and '{' in lines[i]:
                        for j in range(i,len(lines)):
                            if 'rotate ' in lines[j] and not lines[j].startswith('#'):
                                logRetention = int(lines[j].strip().split()[1])
                            if any(x in lines[j] for x in ['hourly','daily','monthly','yearly','weekly']) and not lines[j].startswith('#'):
                                logPeriod = lines[j].strip()
                            if '}' in lines[j]:
                                break
                    i+=1
            if 'hourly' in logPeriod:
                logRetention/=24
            elif 'weekly' in logPeriod:
                logRetention*=7
            elif 'monthly' in logPeriod:
                logRetention*=31
            elif 'yearly' in logPeriod:
                logRetention*=365
            return logRetention  
        except:
            return -1


    def run_check(self, OSName, OSVersion):
        try:
            checkFile = os.path.basename(__file__[:-3])
            for logFile in CONFIG[checkFile]["LOG_FILES"]:
                defaultRotate,defaultLogPeriod=self.getDefaultLogRotation()
                logRotate = self.getLogRotation(defaultLogPeriod,defaultRotate,logFile)
                if os.path.isfile(logFile):
                    if logRotate < 90:
                        self.fail_check(CONFIG[checkFile]["COMMENT"].format(logRotate,logFile))
                    else:
                        self.pass_check(CONFIG[checkFile]["COMMENT"].format(logRotate, logFile))
                else:
                    self.pass_check(CONFIG[checkFile]["PASS_COMMENT_NOT_PRESENT"] + logFile)
        except:
            self.handle_error(checkFile, sys.exc_info())
