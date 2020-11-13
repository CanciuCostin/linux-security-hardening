#!/usr/bin/python
import sys
import os
import time
#import Checks.Common.systemUsers as SystemUsers
#import Checks.Common.middlewareCheck as middlewareCheck
from shutil import copyfile
from shutil import rmtree
#import Checks.Common.configuration as configuration
#import Checks.Common.readConfigurationFile as readConfigurationFile
import modules.checks
#import Remediations
import logging
import logging.config
import copy
from PyInquirer import style_from_dict, Token, prompt, Separator
from modules.utils.SystemInfoHelper import *
from modules.utils.ArgumentsHelper import *
from modules.utils.AbstractCheck import *
from config.ChecksConfig import *





class ScanningWorker():

    def __init__(self):
        self.checks=[]
        self.systemInfoHelper = SystemInfoHelper()
        self.argumentsHelper = ArgumentsHelper(self.systemInfoHelper.hostname, self.systemInfoHelper.scanDate)
                  
    def run_checks(self):
        nrFileChecks=len(modules.checks.__all__)
        percentage=0
        for i in range(nrFileChecks):
            self.update_progress(i/nrFileChecks,'Running Check '+modules.checks.__all__[i]+'...')
            __import__('modules.checks.'+modules.checks.__all__[i])
            check=sys.modules['modules.checks.'+modules.checks.__all__[i]].Check(*(CONFIG[modules.checks.__all__[i]]["INPUT"]))
            check.run_check(self.systemInfoHelper.OSName, self.systemInfoHelper.OSVersion)
            self.checks.append(check)
        self.checks.sort(key=lambda x:x.id,reverse=False)
        for check in self.checks:
            check.print_check_output(self.argumentsHelper.outputFile)
        self.update_progress(100,'Complete!')

    def printCounts(self,elapsedSeconds):
        CONST_RED = '\033[91m'
        CONST_END = '\033[0m'
        CONST_GREEN= '\033[32m'
        with open(self.argumentsHelper.outputFile,'a') as fileInput:
            print('\nTotal number of checks: %s' % AbstractCheck.nrSubChecks);
            fileInput.write('\n\n\nTotal number of checks: %s' % AbstractCheck.nrSubChecks)
            print('- Total number of Failures: %s' % AbstractCheck.nrFailures);
            fileInput.write('\n- Total number of Failures:                  %s' % AbstractCheck.nrFailures)
            print('Overall Status: %s' % CONST_RED+'FAIL'+CONST_END if AbstractCheck.nrFailures > 0 else 'Overall Status: %s' % CONST_GREEN+'PASS'+CONST_END);
            fileInput.write('\nOverall Status: %s' % 'FAIL' if AbstractCheck.nrFailures > 0 else '\nOverall Status: %s' % 'PASS')
            fileInput.write('\nDuration: {:02d}:{:02d}'.format(int(elapsedSeconds/60), (elapsedSeconds % 60)) )


    def load_imports(self, path):
        checkFiles = os.listdir(path)
        imports = []
        for i in range(len(checkFiles)):
            name = checkFiles[i].split('.')
            if len(name) > 1:
                if name[1] == 'py' and name[0] != '__init__':
                    name = name[0]
                    imports.append(name)
        toWrite = '__all__ = '+str(imports)
        with open(path+'__init__.py','w') as fileOutput:
            fileOutput.write(toWrite)
        return imports

    def update_progress(self,progress,statuss):
        points=''
        barLength = 56
        status = ""
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
            status = "error: progress var must be float\r\n"
        if progress < 0:
            progress = 0
            status = "Halt...\r\n"
        if progress >= 1:
            progress = 1
            status = "Done...\r\n"
        block = int(round(barLength*progress))
        text = "\rProgress: [{0}] {1}%".format( "#"*block + "-"*(barLength-block), int(progress*100))    
        points+='.'
        sys.stdout.write(text)
        sys.stdout.flush()


# style = style_from_dict({
#     Token.Separator: '#cc5454',
#     Token.QuestionMark: '#673ab7 bold',
#     Token.Selected: '#cc5454',  # default
#     Token.Pointer: '#673ab7 bold',
#     Token.Instruction: '',  # default
#     Token.Answer: '#f44336 bold',
#     Token.Question: '',
# })

# def getChecksToRemediate(checkList):
#     global style
#     choices=[
#                 Separator('= Check Titles =')
#             ]
#     choices.extend(checkList)
#     questions = [
#         {
#             'type': 'checkbox',
#             'message': 'Select Checks To Remediate',
#             'name': 'checks',
#             'choices': choices,
#             'validate': lambda answer: 'You must choose at least one check.' \
#                 if len(answer['checks']) == 0 else True
#         }
#     ]
#     answers = prompt(questions, style=style)
#     return answers

# def getBlueCloudType():
#     global style
#     questions = [
#         {
#             'type': 'list',
#             'message': 'Select Server Type',
#             'name': 'BlueCloudServerType',
#             'choices': [
#                 Separator('= Type ='),
#                 {
#                     "name":"Bluecloud"
#                 },
#                 {
#                     "name":"non-Bluecloud"
#                 }
#             ],
#             'validate': lambda answer: 'You must choose at least one check.' \
#                 if len(answer['checks']) == 0 else True
#         }
#     ]
#     answers = prompt(questions, style=style)
#     return answers



    def start_scan(self,start):
        #logging.basicConfig(filename=ScanningWorker.scansLogFile,format='%(asctime)s --- %(levelname)s --- %(message)s',level=logging.DEBUG)
        #logging.info(ScanningWorker.fileName)
        #middlewareCheck.checkMiddleware(ScanningWorker.fileName)
        self.run_checks()
        end = time.time(); elapsedSeconds=int(end - start)
        self.printCounts(elapsedSeconds)
        #os.symlink(ScanningWorker.fileName,lastScanFileName)
        print('\n----------------Health Check Done! Please check the file:----------------\n{0}\n'.format(self.argumentsHelper.outputFile))

if __name__== '__main__':
    scanningWorker=ScanningWorker()

    start = time.time()
    #ScanningWorker.dirName,ScanningWorker.scriptVersion=loadArguments()
    #ScanningWorker.remediationsLogFile=ScanningWorker.dirName+'/Remediations.log'
    #ScanningWorker.scansLogFile=ScanningWorker.dirName+'/Scans.log'
    checksImports=scanningWorker.load_imports('modules/checks/')
    #ScanningWorker.fileName,ScanningWorker.userId,ScanningWorker.scanDate,ScanningWorker.UTCscanDate,ScanningWorker.hostName,ScanningWorker.FQDN,ScanningWorker.osName,ScanningWorker.osVersion,ScanningWorker.osBuildDate,ScanningWorker.lastReboot,ScanningWorker.ipAddresses,ScanningWorker.MACAddresses=check_realease.getServerUniqueInformation(ScanningWorker.dirName,ScanningWorker.scriptVersion)
    #if ScanningWorker.osName == 'Not Supported':
    #    print('Sorry, this operating system is not supported. Supported Operating Systems: RedHat, CentOS, Ubuntu, Debian, SuSE')
    #    sys.exit(101)
    
    #if '--R' in list(map(lambda x:x.upper(),sys.argv)):
    #    remediateScript()
    #else:
    scanningWorker.start_scan(start)
    #else:
    #    sys.exit(-2)