
class ArgumentsHelper:
    def __init__(self,hostname,scanDate):
        self.getOutputFile(hostname,scanDate)

    def getOutputFile(self,hostname,scanDate):
        self.outputFile = hostname + '__' + scanDate[:10].replace("-","") + '_' + scanDate[-8:-3] + '.txt'
        