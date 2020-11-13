
#!/usr/bin/python
import subprocess
import os
import re


class SystemInfoHelper:
    def __init__(self):
        self.getOSDistribution()
        self.getScanDate()
        self.getUTCScanDate()
        self.getHostname()
        self.getFQDN()
        self.getIPAddresses()
        self.getMACAddresses()
        self.getOperatingSystem()
        self.getLastRebootDate()
        self.getOSBuildDate()
        self.getUserId()
        self.getCPUArchitecture()
        self.getSystemUUID()

    def getOSDistribution(self):
        try:
            CONST_PATH_RH = '/etc/redhat-release'
            CONST_PATH_SUSE = '/etc/SuSE-release'
            CONST_PATH_DEBIAN = '/etc/debian_version'
            if os.path.isfile(CONST_PATH_RH):
                self.OSDistribution = 'RedHat'
            elif os.path.isfile(CONST_PATH_SUSE):
                self.OSDistribution = 'SuSE'
            elif os.path.isfile(CONST_PATH_DEBIAN):
                self.OSDistribution = 'Debian'
            else:
                raise Exception
        except:
            self.OSDistribution = "Unknown"

    def getScanDate(self):
        try:
            CONST_DATE_COMMAND = ['date', '+%Y-%m-%d %H:%M:%S']
            self.scanDate = subprocess.check_output(
                CONST_DATE_COMMAND,
                stderr=subprocess.PIPE,
                universal_newlines=True).strip()
        except:
            self.scanDate = "Unknown"

    def getUTCScanDate(self):
        try:
            CONST_UTC_DATE_COMMAND = ['date', '-u', '+%Y-%m-%d %H:%M:%S']
            self.UTCScanDate = subprocess.check_output(
                CONST_UTC_DATE_COMMAND,
                stderr=subprocess.PIPE,
                universal_newlines=True).strip()
        except:
            self.UTCScanDate = "Unknown"

    def getHostname(self):
        try:
            CONST_HOSTNAME_COMMAND = ['hostname']
            self.hostname = subprocess.check_output(
                CONST_HOSTNAME_COMMAND,
                stderr=open('/dev/null', 'w'),
                shell=True,
                universal_newlines=True).strip()
        except:
            self.hostname = "Unknown"

    def getFQDN(self):
        try:
            CONST_FQDN_COMMAND = ['hostname --fqdn']
            self.FQDN = subprocess.check_output(
                CONST_FQDN_COMMAND,
                stderr=open('/dev/null', 'w'),
                shell=True,
                universal_newlines=True).strip()
        except:
            self.FQDN = "Unknown"

    def getIPAddresses(self):
        try:
            CONST_IP_COMMAND_RH = (
                "ip addr show | grep -w -v lo | grep -w -v docker | grep -oP '(?<=inet\s)\d+(\.\d+){3}'")
            CONST_IP_COMMAND_SUSE = (
                "ip addr show | grep -w -v lo | grep -w -v docker | grep -oP '(?<=inet\s)\d+(\.\d+){3}'")
            CONST_IP_COMMAND_DEBIAN = (
                "ip addr show | grep -w -v lo | grep -w -v docker | grep -oP '(?<=inet\s)\d+(\.\d+){3}'")
            if self.OSDistribution == 'RedHat':
                self.IPAddresses = str(subprocess.Popen(
                    CONST_IP_COMMAND_RH,
                    stdout=subprocess.PIPE,
                    shell=True,
                    universal_newlines=True).communicate()[0].strip().split())
            elif self.OSDistribution == 'SuSE':
                IpAddresses = str(subprocess.Popen(
                    CONST_IP_COMMAND_SUSE,
                    stdout=subprocess.PIPE,
                    shell=True,
                    universal_newlines=True).communicate()[0].strip().split())
            elif self.OSDistribution == 'Debian':
                IpAddresses = str(subprocess.Popen(
                    CONST_IP_COMMAND_DEBIAN,
                    stdout=subprocess.PIPE,
                    shell=True,
                    universal_newlines=True).communicate()[0].strip().split())
            else:
                raise Exception
        except:
            self.IPAddresses = "Unknown"

    def getMACAddresses(self):
        try:
            CONST_MAC_COMMAND = (
                "ip link show | grep -v lo | grep -v docker | awk '/link/ { print $2 }'")
            self.MACAddresses = str(subprocess.Popen(
                                    CONST_MAC_COMMAND,
                                    stdout=subprocess.PIPE,
                                    shell=True,
                                    universal_newlines=True).communicate()[0].strip().split('\n'))
        except:
            self.MACAddresses = "Unknown"

    def getOperatingSystem(self):
        try:
            if self.OSDistribution == 'RedHat':
                with open('/etc/redhat-release', 'r') as fileInput:
                    self.OSName = fileObject.read().strip()
                self.OSVersion = re.findall("\d+\.\d+", self.OSName)[0]
            elif self.OSDistribution == 'SuSE':
                self.OSName = subprocess.Popen(
                    ("cat /etc/SuSE-release | head -1"),
                    stdout=subprocess.PIPE,
                    shell=True,
                    universal_newlines=True).communicate()[0].strip()
                self.OSVersion = subprocess.Popen(
                    ("awk -F= '/VERSION/ {print $2}' /etc/SuSE-release"),
                    stdout=subprocess.PIPE,
                    shell=True,
                    universal_newlines=True).communicate()[0].strip()
            elif self.OSDistribution == 'Debian':
                distrib = str(subprocess.Popen(
                    ("awk -F= '/DISTRIB_ID/ {print $2}' /etc/lsb-release"),
                    stdout=subprocess.PIPE,
                    shell=True,
                    universal_newlines=True).communicate()[0]).strip()
                if distrib == 'Ubuntu':
                    self.OSName = "Ubuntu "
                    self.OSVersion = subprocess.Popen(
                        ("awk -F= '/DISTRIB_RELEASE/ {print $2}' /etc/lsb-release"),
                        stdout=subprocess.PIPE,
                        shell=True,
                        universal_newlines=True).communicate()[0].strip()
                    self.OSName += OsVersion
                else:
                    self.OSName = "Debian"
                    self.OSVersion = subprocess.Popen(
                        ("cat /etc/debian_version"),
                        stdout=subprocess.PIPE,
                        shell=True,
                        universal_newlines=True).communicate()[0].strip()
            else:
                raise Exception
        except:
            self.OSName = "Uknown"
            self.OSVersion = "Uknown"

    def getLastRebootDate(self):
        try:
            if self.OSDistribution == 'RedHat':
                CONST_LAST_REBOOT_COMMAND_RH = ("who -b | awk '{print $3,$4}'")
                self.lastReboot = subprocess.Popen(
                    CONST_LAST_REBOOT_COMMAND_RH,
                    stdout=subprocess.PIPE,
                    shell=True,
                    universal_newlines=True).communicate()[0].strip()
            elif self.OSDistribution == 'SuSE':
                CONST_LAST_REBOOT_COMMAND_SUSE = (
                    "who -b | awk '{print $3,$4,$5}'")
                self.lastReboot = subprocess.Popen(
                    CONST_LAST_REBOOT_COMMAND_SUSE,
                    stdout=subprocess.PIPE,
                    shell=True,
                    universal_newlines=True).communicate()[0].strip()
            elif self.OSDistribution == 'Debian':
                CONST_LAST_REBOOT_COMMAND_DEBIAN = (
                    "who -b | awk '{print $3,$4}'")
                self.lastReboot = subprocess.Popen(
                    CONST_LAST_REBOOT_COMMAND_DEBIAN,
                    stdout=subprocess.PIPE,
                    shell=True,
                    universal_newlines=True).communicate()[0].strip()
            else:
                raise Exception
        except:
            self.lastReboot = "Unknown"

    def getOSBuildDate(self):
        try:
            CONST_BUILD_DATE_COMMAND = (
                "ls -lact --full-time /etc |awk 'END {print $6}'")
            self.OSBuildDate = subprocess.Popen(
                CONST_BUILD_DATE_COMMAND,
                stdout=subprocess.PIPE,
                shell=True,
                universal_newlines=True).communicate()[0].strip()
        except:
            self.OSBuildDate = "Unknown"

    def getUserId(self):
        try:
            self.userId = os.getlogin().strip()
        except:
            self.userId = "Unknown"

    def getCPUArchitecture(self):
        try:
            CONST_ARCHITECTURE_COMMAND = ['uname', '-m']
            self.CPUArchitecture = subprocess.check_output(
                CONST_ARCHITECTURE_COMMAND,
                stderr=open('/dev/null', 'w')).strip()
        except:
            self.CPUArchitecture = "Unknown"

    def getSystemUUID(self):
        try:
            CONST_UUID_COMMAND = ("dmidecode -s system-uuid")
            self.systemUUID = subprocess.Popen(
                CONST_UUID_COMMAND,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                universal_newlines=True).communicate()[0].strip()
        except:
            self.systemUUID = "Unknown"
