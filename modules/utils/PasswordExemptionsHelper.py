
#!/usr/bin/python

class PasswordExemptionsHelper:
    def __init__(self):
        self.exemptedUsers=[]

                                if fields[1] not in ['','*','!!'] and not passwordExemptions.isUserExemptedFromPasswordRules(pwd.getpwnam(fields[0]).pw_uid,fields[0]) and not passwordExemptions.isSystemUser(fields[0],osName):
        
    def isSystemUser(userName,osName):
        try:
            CONST_REDHAT_5_RANGES={0:99,101:499}
            CONST_REDHAT_6_RANGES={0:99,101:499}
            CONST_REDHAT_7_RANGES={0:99,101:999}
            CONST_UBUNTU_RANGES={0:99,101:999}
            CONST_DEBIAN_RANGES={0:99,101:999}
            CONST_SUSE_RANGES={0:99,101:499}
            idRanges=None
            if ('Red Hat' in osName and '5' in osName) or 'CentOS' in osName :
                idRanges=CONST_REDHAT_5_RANGES
            elif 'Red Hat' in osName and '6' in osName:
                idRanges=CONST_REDHAT_6_RANGES
            elif 'Red Hat' in osName and '7' in osName:
                idRanges=CONST_REDHAT_7_RANGES
            elif 'Ubuntu' in osName:
                idRanges=CONST_UBUNTU_RANGES
            elif 'Debian' in osName:
                idRanges=CONST_DEBIAN_RANGES
            elif 'SUSE' in osName:
                idRanges=CONST_SUSE_RANGES

            groupId=getpwnam(userName).pw_gid
            for minRange in idRanges.keys():
                maxRange=idRanges[minRange]
                if int(groupId) >= minRange and int(groupId) <= maxRange:
                    return True
            return False
        except Exception as ex:
            return False

    def isUserExemptedFromPasswordRules(userId,userName):
        CONST_OPTION_A_FILES=['/etc/passwd','/etc/ftpusers','/etc/vsftpd.ftpusers','/etc/vsftpd/ftpusers']
        CONST_OPTION_B_AND_C_FILES=['/etc/shadow']
        CONST_OPTION_D_FILES=['/etc/pam.d/system-auth','/etc/pam.d/password-auth']
        CONST_OPTION_D_REQUIREMENT=['auth','required','/lib/security/$ISA/pam_listfile.so','item=user','sense=deny','file=/etc/security/','onerr=succeed']
        try:
            #OPTION A
            for ftpFile in CONST_OPTION_A_FILES[1:]:
                if os.path.isfile(ftpFile):
                    file_object=open(ftpFile,'r')
                    for line in file_object:
                        line=line.strip()
                        if len(line) > 0 and line[0] != '#':
                            if line == userName:
                                return True
                    file_object.close()
            if os.path.isfile(CONST_OPTION_A_FILES[0]):
                file_object = open(CONST_OPTION_A_FILES[0], 'r')
                for line in file_object:
                    line = line.strip()
                    if len(line) > 0 and line[0] != '#':
                        fields = line.split(":")
                        if len(fields) >= 7 and fields[2] == str(userId) and any( x in fields[6] for x in ['/bin/false','/sbin/false','/bin/nologin','/sbin/nologin','/nologin']):
                            return True
                file_object.close()
            #OPTION B and OPTION C
            if os.path.isfile(CONST_OPTION_B_AND_C_FILES[0]):
                file_object = open(CONST_OPTION_B_AND_C_FILES[0], 'r')
                for line in file_object:
                    line = line.strip()
                    if len(line) > 0 and line[0] != '#':
                        fields = line.split(":")
                        if len(fields) >= 5 and fields[0] == userName:
                            #CHECKING OPTION B - locked account
                            if any(x in fields[1] for x in ['!','!!']) and '$' in fields[1]:
                                return True
                        #CHECKING OPTION C
                            if fields[1] in ['!','!!','x']:
                                return True
                file_object.close()
            return False
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return False
