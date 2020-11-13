from abc import ABC,abstractmethod
from texttable import Texttable


class AbstractCheck(ABC):

    CONST_TABLE_HEADERS=["RULE","STATUS","REMEDIATION","COMMENTS"]
    CONST_COLS_WIDTH=[40,10,40,40]
    CONST_COLS_ALIGN=["l","c","l","l"]
    CONST_PASS="PASS"
    CONST_FAIL="FAIL"
    CONST_ERROR="ERROR"
    nrSubChecks=0
    nrFailures=0

    def __init__(self,checkId,checkName,checkRules,checkRemediations):
        self.id=checkId
        self.name=checkName
        self.rules=checkRules
        self.remediations=checkRemediations
        self.statuses=[]
        self.comments=[]
        self.init_text_table()
        self.nrFailures=0
        self.nrSubChecks=0
        

    def init_text_table(self):
        self.textTable=Texttable()
        self.textTable.set_cols_width((AbstractCheck.CONST_COLS_WIDTH))
        self.textTable.set_cols_align((AbstractCheck.CONST_COLS_ALIGN))
        self.textTable.header(AbstractCheck.CONST_TABLE_HEADERS)

    def pass_check(self,passComment):
        self.statuses += CONST_PASS
        self.comments += passComment

    def fail_check(self,failComment):
        self.statuses += CONST_FAIL
        self.comments += failComment

    def handle_error(self,checkFile, exceptionType, exceptionObject, exceptionTb):
        self.rules=self.remediations=self.statuses=self.comments=["ERROR"]
        #log print(exceptionType, checkFile, exceptionTb.tb_lineno)
        print("Error %s" % checkFile)
    
    @abstractmethod
    def run_check(self,OSName, OSVersion):
        pass

    def print_check_output(self,fileName):
        self.nrFailures=len(list(filter(lambda x: x == 'FAIL', self.statuses))); 
        self.nrSubChecks=len(self.rules)
        AbstractCheck.nrSubChecks += self.nrSubChecks
        AbstractCheck.nrFailures += self.nrFailures
        with open(fileName,'a') as fileInput:
            fileInput.write('Section '+ self.id + ' - ' + self.name + '\n')
            for i in range(self.nrSubChecks):  
                self.textTable.add_row([self.rules[i],self.statuses[i],self.remediations[i],self.comments[i]])
            fileInput.write(self.textTable.draw()+"\n\n\n\n")
