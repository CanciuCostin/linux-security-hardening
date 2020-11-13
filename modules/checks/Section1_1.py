#!/usr/bin/python
from modules.utils.AbstractCheck import *
from config.ChecksConfig import *
import sys
sys.path.append("../..")


class Check(AbstractCheck):
    def parseDate(self):
        supportDate = config.SUPPORT_DATES[osItem]
        year = int(supportDate[0:4])
        month = supportDate[5:7]
        month = int(month.strip(
            '0')) if not month == '10' else int(month)
        day = supportDate[8:10]
        day = int(day.strip('0')) if not any(
            x == day for x in ['10', '20', '30']) else int(day)
        return year, month, day

    def run_check(self, OSName, OSVersion):
        try:
            checkFile=os.path.basename(__file__[:-3])
            for osItem in config.SUPPORT_DATES.keys():
                if osItem in osName:
                    year, month, day = self.parseDate()
                    if datetime.datetime(year, month, day) > dt.today():
                        self.pass_check(CONFIG[checkFile]["PASS_COMMENT"])
                    else:
                        self.fail_check(CONFIG[checkFile]["FAIL_COMMENT"])
                    return
            self.fail_check(CONFIG[checkFile]["FAIL_COMMENT_UNKNOWN"])
        except:
            self.handle_error(checkFile, sys.exc_info())
