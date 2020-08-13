#!/usr/bin/python
from texttable import Texttable
import sys
import os
import time
import Checks.Common.systemUsers as SystemUsers
import Checks.Common.middlewareCheck as middlewareCheck
import Checks.Common.check_realease as check_realease
from shutil import copyfile
from shutil import rmtree
import Checks.Common.configuration as configuration
import Checks.Common.readConfigurationFile as readConfigurationFile
import Checks
#import Remediations
import logging
import logging.config
import copy
from PyInquirer import style_from_dict, Token, prompt, Separator

def loadImports(path):
    files = os.listdir(path)
    imports = []
    for i in range(len(files)):
        name = files[i].split('.')
        if len(name) > 1:
            if name[1] == 'py' and name[0] != '__init__':
               name = name[0]
               imports.append(name)
    toWrite = '__all__ = '+str(imports)
    with open(path+'__init__.py','w') as fileOutput:
        fileOutput.write(toWrite)
    return imports

def update_progress(progress,statuss):
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

class Remediation:
    remediations=[]

    def __init__(self,checkId,checkName,remediationMethod):
        self.checkId=checkId
        self.checkName=checkName
        self.remediateCheck=remediationMethod

    @staticmethod
    def loadRemediations():
        nrRemediations=len(Remediations.__all__)
        for i in range(nrRemediations):
            __import__('Remediations.'+Remediations.__all__[i])
            remediation=Remediation(sys.modules['Remediations.'+Remediations.__all__[i]].CONST_ID,sys.modules['Remediations.'+Remediations.__all__[i]].CONST_NAME,sys.modules['Remediations.'+Remediations.__all__[i]].remediate)
            Remediation.remediations.append(remediation)

class Test:
    AllChecks=list()
    userId=''
    fileName=''
    scanDate=''
    UTCscanDate=''
    hostName=''
    osName=''
    osVersion=''
    osBuildDate=''
    lastReboot=''
    ipAddresses=''
    MACAddresses=''
    dirName=''
    tableHeaders=list()
    tableHeaders.extend(["RULE","Status","REMEDIATION","COMMENTS"])
    noChecks=0
    noFailures=0
    noWarnings=0
    def __init__(self,testMethod):
        self.testId=None
        self.testName=None
        self.testRule=None
        self.Passes=None
        self.Messages=None
        self.remediations=None
        self.flags=None        
        self.testMethod=testMethod
        self.testId,self.testName,self.testRule,self.Passes,self.Messages,self.remediations,self.flags=self.testMethod(Test.osName,Test.osVersion,sys.argv)
    def printTestTable(self,*args):
        if self.Passes != None:
            onlyFails=True if '-FAIL' in list(map(lambda x:x.upper() ,sys.argv)) else False
            onlyPasses=True if '-PASS' in list(map(lambda x:x.upper() ,sys.argv)) else False
            nrChecks=len(self.Messages); Test.noChecks+=nrChecks
            nrFailures=len(list(filter(lambda x: x == 'FAIL',self.Passes))); Test.noFailures+=nrFailures
            nrWarnings=len(list(filter(lambda x: x == 'WARNING',self.Passes)));
            nrPasses=len(list(filter(lambda x: x in ['PASS','INFO'],self.Passes)));
            nrNA=len(list(filter(lambda x: x == 'N/A',self.Passes)));
            Statuses=copy.deepcopy(self.Passes)
            Comments=copy.deepcopy(self.Messages)
            if onlyFails or onlyPasses:
                nrRows=len(self.Messages)
                i=0
                while i<nrRows and nrRows > 0:
                    if ( (onlyFails and (self.Passes[i] not in ['FAIL','INFO','WARNING'])) or ( onlyPasses and (self.Passes[i] not in ['PASS']))):
                        del self.Passes[i]
                        del self.Messages[i]
                        del self.remediations[i]
                        nrRows-=1
                        i-=1
                    i+=1
            nrRows=len(self.Messages)
            if nrRows > 0:
                self.textTable=Texttable()
                self.textTable.set_cols_width(([40,10,40,40]))
                self.textTable.set_cols_align((["l","c","l","l"]))
                TableHeaders=[Test.tableHeaders[0],Test.tableHeaders[1],Test.tableHeaders[2],Test.tableHeaders[3]]
                self.textTable.header(TableHeaders)
                Result='PASS'
                if nrFailures > 0:
                    Result='FAIL'
                elif nrWarnings > 0:
                    Result='WARNING'
                elif nrPasses > 0:
                    Result='PASS'
                elif nrNA > 0:
                    Result='N/A'
                for i in range(len(Comments)):
                    elem=dict()
                    elem["RULE"]=self.testRule[i]
                    elem["STATUS"]=Statuses[i]
                    elem["COMMENT"]=Comments[i]
                f= open(Test.fileName,"a")        
                f.write('Section '+self.testId+' - '+self.testName+'\n')
                for i in range(nrRows):  
                    self.textTable.add_row([self.testRule[i],self.Passes[i],self.remediations[i],self.Messages[i] ])
                f.write(self.textTable.draw()+"\n\n\n\n")
                f.close()
            else:
                for i in range(len(Comments)):
                    elem=dict()
                    elem["RULE"]=self.testRule[i]
                    elem["STATUS"]=Statuses[i]
                    elem["COMMENT"]=Comments[i]
                  
    @staticmethod
    def DisplayChecks():
        noFileChecks=len(Checks.__all__)
        percentage=0
        for i in range(noFileChecks):
            update_progress(i/noFileChecks,'Running Check '+Checks.__all__[i]+'...')
            __import__('Checks.'+Checks.__all__[i])
            test=Test(sys.modules['Checks.'+Checks.__all__[i]].ExecuteTest)
            Test.AllChecks.append(test)
        AllChecks=list(filter(lambda x:x.testId != None,Test.AllChecks))
        AllChecks.sort(key=lambda x:x.testId,reverse=False)
        selectedTest=list(filter(lambda x: '-Section' in x,sys.argv))
        if len(selectedTest) > 0:
            for check in AllChecks:
                if check.testId.replace(' ','') == selectedTest[0][8:]:
                    check.printTestTable()
        else:
            for check in AllChecks:
                check.printTestTable()
        update_progress(100,'Complete!')

    @staticmethod
    def printCounts(elapsedSeconds):
        CONST_RED = '\033[91m'
        CONST_END = '\033[0m'
        CONST_GREEN= '\033[32m'
        fileObject=open(Test.fileName,'a') 
        print('\nTotal number of checks: %s' % Test.noChecks); fileObject.write('\n\n\nTotal number of checks: %s' % Test.noChecks)
        print('- Total number of Failures: %s' % Test.noFailures);               fileObject.write('\n- Total number of Failures:                  %s' % Test.noFailures)
        print('- Total number of Warnings: %s' % Test.noWarnings); fileObject.write('\n- Total number of Warnings:                %s' % Test.noWarnings)
        print('Overall Status: %s' % CONST_RED+'FAIL'+CONST_END if Test.noFailures > 0 else 'Overall Status: %s' % CONST_GREEN+'PASS'+CONST_END); fileObject.write('\nOverall Status: %s' % 'FAIL' if Test.noFailures > 0 else '\nOverall Status: %s' % 'PASS')
        fileObject.write('\nDuration: {:02d}:{:02d}'.format(int(elapsedSeconds/60), (elapsedSeconds % 60)) )
        fileObject.close()

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

def getChecksToRemediate(checkList):
    global style
    choices=[
                Separator('= Check Titles =')
            ]
    choices.extend(checkList)
    questions = [
        {
            'type': 'checkbox',
            'message': 'Select Checks To Remediate',
            'name': 'checks',
            'choices': choices,
            'validate': lambda answer: 'You must choose at least one check.' \
                if len(answer['checks']) == 0 else True
        }
    ]
    answers = prompt(questions, style=style)
    return answers

def getBlueCloudType():
    global style
    questions = [
        {
            'type': 'list',
            'message': 'Select Server Type',
            'name': 'BlueCloudServerType',
            'choices': [
                Separator('= Type ='),
                {
                    "name":"Bluecloud"
                },
                {
                    "name":"non-Bluecloud"
                }
            ],
            'validate': lambda answer: 'You must choose at least one check.' \
                if len(answer['checks']) == 0 else True
        }
    ]
    answers = prompt(questions, style=style)
    return answers

def loadArguments():
    print('\n-------------------------------------------------------------------------')
    print('\n--------------------------Running Health Check---------------------------\n')
    print('-------------------------------------------------------------------------\n')
    if len(sys.argv) > 1 and 'dirName=' in sys.argv[1]:
        dirName=sys.argv[1][8:]
    else:
        dirName=os.getcwd()
    if not os.path.isdir(dirName):
        os.mkdir(dirName)
    scriptVersion=configuration.SCRIPT_VERSION
    return dirName,scriptVersion

def remediateScript():
    Remediation.loadRemediations()
    logging.basicConfig(filename=Test.remediationsLogFile,format='%(asctime)s --- %(levelname)s --- %(message)s',level=logging.DEBUG)
    remediationCheckTitles=list(filter(lambda arg:arg.startswith('Section'),sys.argv))
    if len(remediationCheckTitles) == 0:
        allRemediationCheckTitles=list(map(lambda check:{'name': "Section " + check.checkId + " - " + check.checkName},Remediation.remediations))
        remediationCheckTitles=getChecksToRemediate(allRemediationCheckTitles)['checks']
    exitCode=0
    for remediationCheckTitle in remediationCheckTitles:
        checkToRemediate=list(filter(lambda r: r.checkId + ' - ' + r.checkName == remediationCheckTitle[8:],Remediation.remediations))
        if len(checkToRemediate) != 0:
            logging.info('___"Section '+checkToRemediate[0].checkId+' - '+checkToRemediate[0].checkName+'"')
            exitCode=checkToRemediate[0].remediateCheck(Test.osName,Test.osVersion,sys.argv)
        else:
            continue
    logging.debug('exit___'+str(exitCode))
    if not exitCode == 0:
        sys.exit(exitCode)

def saveFilesToBeUploaded(dirName,*args):
    uploadManualDirectory=dirName+'/FilesToUploadManually'
    if os.path.isdir(uploadManualDirectory):
        rmtree(uploadManualDirectory)
    os.mkdir(uploadManualDirectory)
    for fileName in args:
        copyfile(fileName,uploadManualDirectory+'/'+fileName.split('/')[-1])

def scanScript(start):
    logging.basicConfig(filename=Test.scansLogFile,format='%(asctime)s --- %(levelname)s --- %(message)s',level=logging.DEBUG)
    logging.info(Test.fileName)
    middlewareCheck.checkMiddleware(Test.fileName)
    Test.DisplayChecks()
    end = time.time(); elapsedSeconds=int(end - start)
    Test.printCounts(elapsedSeconds)
    #os.symlink(Test.fileName,lastScanFileName)
    print('\n----------------Health Check Done! Please check the file:----------------\n{0}\n'.format(Test.fileName))

if __name__=='__main__':
    start = time.time()
    Test.dirName,Test.scriptVersion=loadArguments()
    Test.remediationsLogFile=Test.dirName+'/Remediations.log'
    Test.scansLogFile=Test.dirName+'/Scans.log'
    #if checkScripVersion.isLatestScriptVersion(Test.scriptVersion) or '-justTesting' in sys.argv:
    checksImports=loadImports('Checks/')
    #remediationsImports=loadImports('Remediations/')
    Test.fileName,Test.userId,Test.scanDate,Test.UTCscanDate,Test.hostName,Test.FQDN,Test.osName,Test.osVersion,Test.osBuildDate,Test.lastReboot,Test.ipAddresses,Test.MACAddresses=check_realease.getServerUniqueInformation(Test.dirName,Test.scriptVersion)
    if Test.osName == 'Not Supported':
        print('Sorry, this operating system is not supported. Supported Operating Systems: RedHat, CentOS, Ubuntu, Debian, SuSE')
        sys.exit(101)
    #if '--R' in list(map(lambda x:x.upper(),sys.argv)):
    #    remediateScript()
    #else:
    scanScript(start)
    #else:
    #    sys.exit(-2)