#!/usr/bin/python
from modules.utils.AbstractCheck import *
from config.ChecksConfig import *
import sys
import os
sys.path.append("../..")


class Check(AbstractCheck):
    def isLengthCompliant(self, minlen, lcredit, ucredit, dcredit, ocredit, minLength):
        for credit in [lcredit, ucredit, dcredit, ocredit]:
            if credit > 0:
                minlen -= credit
        if minlen >= minLength:
            return True
        return False

    def getPwQualityConfigValues(self):
        minLen, dcredit, ucredit, lcredit, ocredit, minclass = 9, 0, 0, 0, 0, 0
        try:
            with open('/etc/security/pwquality.conf', 'r') as fileInput:
                for line in fileInput:
                    if len(line) > 0 and line[0] != '#':
                        fields = line.strip().split('=')
                        if len(fields) == 2:
                            if fields[0].strip() == 'minlen':
                                minLen = int(fields[1])
                            elif fields[0].strip() == 'dcredit':
                                dcredit = int(fields[1])
                            elif fields[0].strip() == 'ucredit':
                                ucredit = int(fields[1])
                            elif fields[0].strip() == 'lcredit':
                                lcredit = int(fields[1])
                            elif fields[0].strip() == 'ocredit':
                                ocredit = int(fields[1])
                            elif fields[0].strip() == 'minclass':
                                minclass = int(fields[1])
            return minLen, dcredit, ucredit, lcredit, ocredit, minclass
        except:
            return None, None, None, None, None, None


def checkCracklib(self, lines, minLength, minComplexity):
    try:
        for line in lines:
            if len(line) > 0 and line[0] != '#':
                fields = line.split()
                if len(fields) >= 3:
                    if all((fields[0] == 'password',
                            fields[1] in ['required', 'requisite'],
                            fields[2] == 'pam_cracklib.so')):
                        minLen, dcredit, ucredit, lcredit, ocredit, minclass = 9, 0, 0, 0, 0, 0
                        if 'minlen=' in line:
                            minLen = int(
                                re.search('minlen=(\d+)', line).group(1))
                        if 'dcredit=' in line:
                            dcredit = int(
                                re.search('dcredit=(.\d+|\d+)', line).group(1))
                        if 'ucredit=' in line:
                            ucredit = int(
                                re.search('ucredit=(.\d+|\d+)', line).group(1))
                        if 'ocredit=' in line:
                            ocredit = int(
                                re.search('ocredit=(.\d+|\d+)', line).group(1))
                        if 'lcredit=' in line:
                            lcredit = int(
                                re.search('lcredit=(.\d+|\d+)', line).group(1))
                        if 'minclass=' in line:
                            minclass = int(
                                re.search('minclass=(.\d+|\d+)', line).group(1))
                        if isLengthCompliant(minLen, lcredit, ucredit, dcredit, ocredit, minLength)
                        and (len(list(filter(lambda x: x == -1, [dcredit, ucredit, ocredit, lcredit]))) >= minComplexity or minclass >= minComplexity):
                            return True
        return False
    except:
        return False


def checkPwQuality(self, lines, minLength, minComplexity):
    try:
        for line in lines:
            if len(line) > 0 and line[0] != '#':
                fields = line.split()
                if len(fields) >= 3:
                    if all((fields[0] == 'password',
                            fields[1] in ['required', 'requisite'],
                            fields[2] == 'pam_pwquality.so')):
                        minLen = 0
                        minLen, dcredit, ucredit, lcredit, ocredit, minclass = self.getPwQualityConfigValues()
                        if 'minlen=' in line:
                            minLen = int(
                                re.search('minlen=(\d+)', line).group(1))
                        if 'dcredit=' in line:
                            dcredit = int(
                                re.search('dcredit=(.\d+|\d+)', line).group(1))
                        if 'ucredit=' in line:
                            ucredit = int(
                                re.search('ucredit=(.\d+|\d+)', line).group(1))
                        if 'ocredit=' in line:
                            ocredit = int(
                                re.search('ocredit=(.\d+|\d+)', line).group(1))
                        if 'lcredit=' in line:
                            lcredit = int(
                                re.search('lcredit=(.\d+|\d+)', line).group(1))
                        if 'minclass=' in line:
                            minclass = int(
                                re.search('minclass=(.\d+|\d+)', line).group(1))
                        if isLengthCompliant(minLen, lcredit, ucredit, dcredit, ocredit, minLength)
                        and (len(list(filter(lambda x: x == -1, [dcredit, ucredit, ocredit, lcredit]))) >= minComplexity or minclass >= minComplexity):
                            return True
        return False
    except:
        return False


def checkPasswdq(self, lines, minLength, minComplexity):
    try:
        for line in lines:
            if len(line) > 0 and line[0] != '#':
                fields = line.split()
                if len(fields) >= 3:
                    if all((fields[0] == 'password',
                            fields[1] in ['required', 'requisite'],
                            fields[2] == 'pam_passwdq.so')):
                        if all(x in line for x in ['min=disabled,{0},{0},{0},{0}'.format(str(minLength)), 'passphrase=0', 'random=0', 'enforce=everyone']):
                            return True
        return False
    except:
        return False

    def run_check(self, OSName, OSVersion):
        try:
            checkFile = os.path.basename(__file__[:-3])
            if 'Red Hat' in osName or 'CentOS' in osName:
                pamFile = CONFIG[checkFile][FILE_REDHAT]
            else:
                pamfile = CONFIG[checkFile][FILE_UBUNTU_DEBIAN_SUSE]
            with open(pamFile, 'r') as fileInput:
                pamLines = fileInput.readlines()
            if any((self.checkPasswdq(
                        pamLines, CONFIG[checkFile]["MIN_LENGTH"], CONFIG[checkFile]["MIN_COMPLEXITY"]),
                    self.checkCracklib(
                        pamLines, CONFIG[checkFile]["MIN_LENGTH"], CONFIG[checkFile]["MIN_COMPLEXITY"]),
                    self.checkPwQuality(
                        pamLines, CONFIG[checkFile]["MIN_LENGTH"], CONFIG[checkFile]["MIN_COMPLEXITY"]))):
                self.pass_check(CONFIG[checkFile]["PASS_COMMENT"])
            else:
                self.fail_check(CONFIG[checkFile]["FAIL_COMMENT"])
        except:
            self.handle_error(checkFile, sys.exc_info())
