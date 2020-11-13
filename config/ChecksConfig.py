CONFIG = {
    "Section1_1": {
        "INPUT": ["1.1",
                  "OS Support",
                  ["Operating system must be under support."],
                  ["Migrate your operating system towards a supported version."]],
        "PASS_COMMENT": "Operating system is under support. End date: {0}",
        "FAIL_COMMENT": "Operating system is not under support anymore. End date: {0}",
        "FAIL_COMMENT_UNKNOWN": "Could not determine end of support date for this OS.",
        "SUPPORT_DATES": {
            'RedHat Enterprise Linux Server release 2': '2009-05-31',
            'RedHat Enterprise Linux Server release 3': '2010-10-31',
            'RedHat Enterprise Linux Server release 4': '2012-02-29',
            'RedHat Enterprise Linux Server release 5': '2017-03-31',
            'Red Hat Enterprise Linux Server release 6.0': '2012-11-30',
            'Red Hat Enterprise Linux Server release 6.1 ': '2013-05-31',
            'Red Hat Enterprise Linux Server release 6.2': '2014-01-07',
            'Red Hat Enterprise Linux Server release 6.3': '2014-06-30',
            'Red Hat Enterprise Linux Server release 6.4': '2015-03-03',
            'Red Hat Enterprise Linux Server release 6.5': '2015-11-30',
            'Red Hat Enterprise Linux Server release 6.6': '2016-10-31',
            'Red Hat Enterprise Linux Server release 6.7': '2017-12-31',
            'Red Hat Enterprise Linux Server release 6.8': '2018-03-03',
            'Red Hat Enterprise Linux Server release 6.9': '2018-11-30',
            'Red Hat Enterprise Linux Server release 6.10': '2020-11-30',
            'Red Hat Enterprise Linux Server release 8.0': '2029-05-01',
            'Red Hat Enterprise Linux Server release 8.0': '2021-11-30',
            'Red Hat Enterprise Linux release 8.0': '2021-11-30',
            'Red Hat Enterprise Linux Server release 8.1': '2021-11-30',
            'Red Hat Enterprise Linux release 8.1': '2021-11-30',
            'Red Hat Enterprise Linux Server release 8.2': '2022-04-30',
            'Red Hat Enterprise Linux release 8.2': '2022-04-30',
            'Red Hat Enterprise Linux Server release 8.3': '2022-04-30',
            'Red Hat Enterprise Linux release 8.3': '2022-04-30',
            'Red Hat Enterprise Linux Server release 8.4': '2022-04-30',
            'Red Hat Enterprise Linux release 8.4': '2022-04-30',
            'Red Hat Enterprise Linux Server release 8.6': '2022-04-30',
            'Red Hat Enterprise Linux release 8.6': '2022-04-30',
            'Red Hat Enterprise Linux Server release 8.8': '2022-04-30',
            'Red Hat Enterprise Linux release 8.8': '2022-04-30',
            'Red Hat Enterprise Linux Server release 7.0': '2017-03-03',
            'Red Hat Enterprise Linux Server release 7.1 ': '2017-03-03',
            'Red Hat Enterprise Linux Server release 7.2': '2017-11-30',
            'Red Hat Enterprise Linux Server release 7.3': '2017-11-30',
            'Red Hat Enterprise Linux Server release 7.4': '2019-08-31',
            'Red Hat Enterprise Linux Server release 7.5': '2020-04-30',
            'Red Hat Enterprise Linux Server release 7.6': '2020-10-31',
            'Red Hat Enterprise Linux Server release 7.7': '2024-06-01',
            'Red Hat Enterprise Linux Server release 7.8': '2024-06-01',
            'CentOS Linux release 2': '2009-05-31',
            'CentOS Linux release 3': '2010-10-31',
            'CentOS Linux release 4': '2012-02-29',
            'CentOS Linux release 5': '2017-03-31',
            'CentOS Linux release 6': '2020-11-30',
            'CentOS Linux release 7': '2024-06-30',
            'CentOS Linux release 8.0': '2029-06-30',
            'CentOS Linux release 8.1': '2029-06-30',
            'CentOS Linux release 8.2': '2029-06-30',
            'CentOS Linux release 8.3': '2029-06-30',
            'CentOS release 2': '2009-05-31',
            'CentOS release 3': '2010-10-31',
            'CentOS release 4': '2012-02-29',
            'CentOS release 5': '2017-03-31',
            'CentOS release 6': '2020-11-30',
            'CentOS release 7': '2024-06-30',
            'CentOS release 8.0': '2029-06-30',
            'CentOS release 8.1': '2029-06-30',
            'CentOS release 8.2': '2029-06-30',
            'CentOS release 8.3': '2029-06-30',
            'Ubuntu 12': '2017-04-01',
            'Ubuntu 14': '2019-04-01',
            'Ubuntu 16': '2021-04-01',
            'Ubuntu 18': '2023-04-01',
            'Debian 6': '2014-05-31',
            'Debian 7': '2016-04-26',
            'Debian 8': '2018-06-06',
            'SUSE Linux Enterprise Server 10': '2013-07-31',
            'SUSE Linux Enterprise Server 11': '2019-03-31',
            'SUSE Linux Enterprise Server 12': '2024-10-31',
            'SUSE Linux Enterprise Server 15': '2028-07-31'
        }
    },
    "Section1_2": {
        "INPUT": ["1.1",
                  "Business Use Notice",
                  ["The file /etc/motd or /etc/issue must contain the MOTD:"],
                  ["Add the MOTD text into /etc/motd"]],
        "PASS_COMMENT": "The MOTD is set.",
        "FAIL_COMMENT": "The MOTD is not set.",
        "MOTD": "The system must only be used for conducting business or for purposes authorized by management",
        "MOTD_FILES": ['/etc/motd', '/etc/issue', '/etc/issue.net']
    },
    "Section2_1": {
        "INPUT": ["2.1",
                  "Default maximum password age",
                  ["File /etc/login.defs must contain the line: \nPASS_MAX_DAYS       90"],
                  ["Add the required line in /etc/login.defs."]],
        "PASS_COMMENT": "The required line was found in /etc/login.defs.",
        "FAIL_COMMENT": "The required line was not found in /etc/login.defs",
        "LOGIN_DEFS": "/etc/login.defs",
        "PASS_MAX_AGE": 90
    },
    "Section2_2": {
        "INPUT": ["2.2",
                  "Maximum password age per user",
                  ["Maximum password age must be set to 90 days for each user in /etc/shadow (5th field)."],
                  ["Run the command: chage -M 90 <user>"]],
        "PASS_COMMENT": "All users have maximum password age set to 90 days.\n\n",
        "FAIL_COMMENT": "There are users having maximum password age < 90 days.\n\n",
        "SHADOW_FILE": "/etc/shadow",
        "PASS_MAX_AGE": 90
    },
    "Section2_3": {
        "INPUT": ["2.3",
                  "Password length and complexity",
                  ['''
One of these two options must be implemented:     
* Parameters of "retry=3 minlen=14 dcredit=-1 ucredit=0 lcredit=-1 ocredit=0" in /etc/pam.d/$PAMFILE    
* parameters of "min=disabled,14,14,14,14 passphrase=0 random=0 enforce=everyone" in /etc/pam.d/$PAMFILE   
  
Note: $PAMFILE will be 'common-password' for SUSE and Debian, for all other distributions will be:'system-auth'
Note: For Red Hat Enterprise Linux V6 and later:  The same entry chosen for system-auth file must ADDITIONALLY be included in the /etc/pam.d/password-auth file.
Note: any two credits of -1 are required and they can be replaced by the minclass=2 parameter.
'''],
                  ["Update pamfile."]],
        "PASS_COMMENT": "Password length and complexity rules are set.",
        "FAIL_COMMENT": "Password length and complexity rules are not set.",
        "FILE_REDHAT": "/etc/pam.d/system-auth",
        "FILE_UBUNTU_DEBIAN_SUSE": "/etc/pam.d/common-password",
        "MIN_LENGTH": 15,
        "MIN_COMPLEXITY": 2
    },
    "Section2_4": {
        "INPUT": ["2.4",
                  "Default minimum password age",
                  ["File /etc/login.defs must contain the line: \nPASS_MIN_DAYS       1"],
                  ["Add the required line in /etc/login.defs."]],
        "PASS_COMMENT": "The required line was found in /etc/login.defs.",
        "FAIL_COMMENT": "The required line was not found in /etc/login.defs",
        "LOGIN_DEFS": "/etc/login.defs",
        "PASS_MIN_AGE": 1
    },
    "Section2_5": {
        "INPUT": ["2.5",
                  "Minimum password age per user",
                  ["Minimum password age must be set to 1 day for each user in /etc/shadow (5th field)."],
                  ["Run the command: chage -m 1 <user>"]],
        "PASS_COMMENT": "All users have minimum password age set to 1 day.\n\n",
        "FAIL_COMMENT": "There are users having minimum password age < 1 days.\n\n",
        "SHADOW_FILE": "/etc/shadow",
        "PASS_MIN_AGE": 1
    },
    "Section2_6": {
        "INPUT": ["2.6",
                  "Password history",
                  ['''The files /etc/pam.d/system-auth and /etc/pam.d/password-auth (RHEL/CENTOS) or /etc/pam.d/common-password (Ubuntu/Debian/SuSE) must include:
password $CONTROL $PAM_MODULE remember=7 use_authtok sha512 shadow

Where $CONTROL is required or sufficient, and $PAM_MODULE is pam_unix.so  or pam_pwhistory.so'''],
                  ["Update the pam files according to the operating system requirements."]],
        "PASS_COMMENT": "The configuration in the pam files is compliant.",
        "FAIL_COMMENT": "The configuration in the pam files is not compliant.",
        "PAM_FILES_RH_CENTOS": ["/etc/pam.d/system-auth", "/etc/pam.d/password-auth"],
        "PAM_FILES_UBUNTU_DEBIAN_SUSE": ["/etc/pam.d/common-password"],
        "PAM_CONTROLS": ["required", "sufficient"],
        "PAM_MODULES": ["pam_unix.so", "pam_pwhistory.so"],
        "HASH_ALGORITHM": "sha512",
        "MIN_REMEMBER": 7
    },
    "Section2_7": {
        "INPUT": ["2.7",
                  "Maximum login retries",
                  [
                      '''File /etc/pam.d/system-auth and /etc/pam.d/password-auth (RHEL/CENTOS) or /etc/pam.d/common-auth (UBUNTU/DEBIAN/SUSE) must contain:

auth required $PAM_MODULE deny=5''',
                      '''File /etc/pam.d/system-auth and /etc/pam.d/password-auth (RHEL/CENTOS) or /etc/pam.d/common-account (UBUNTU/DEBIAN/SUSE) must contain:

account required $PAM_MODULE

Where $PAM_MODULE is one of: pam_tally.so, pam_tally2.so, pam_faillock.so
'''],
                  ["Add the auth line into the required pam files.",
                   "Add the account line into the required pam files."]],
        "PASS_COMMENT_AUTH": "The auth line is set in the pam files.",
        "FAIL_COMMENT_AUTH": "The auth line is not set in the pam files",
        "PASS_COMMENT_ACCOUNT": "The account line is set in the pam files.",
        "FAIL_COMMENT_ACCOUNT": "The account line is not set in the pam files",
        "PAM_FILES_RH_CENTOS": ["/etc/pam.d/system-auth", "/etc/pam.d/password-auth"],
        "PAM_FILES_UBUNTU_DEBIAN_SUSE": ["/etc/pam.d/common-auth", "/etc/pam.d/common-account"],
        "PAM_MODULES": ["pam_tally.so", "pam_tally2.so", "pam_faillock.so"],
        "MAX_RETRIES": 5
    },
    "Section2_8": {
        "INPUT": ["2.8",
                  "Prevent UID and GID reuse",
                  ["All user ids must be unique in /etc/passwd",
                      "All group ids must be unique in /etc/group"],
                  ["Run the command: chage -m 1 <user>"]],
        "PASS_COMMENT_USERS": "All UIDs are unique.",
        "FAIL_COMMENT_USERS": "UIDs are not unique.",
        "PASS_COMMENT_GROUPS": "All GIDs are unique.",
        "FAIL_COMMENT_GROUPS": "GIDs are not unique.",
        "PASSWD_FILE": "/etc/passwd",
        "GROUP_FILE": "/etc/group"
    },
    "Section2_9": {
        "INPUT": ["2.9",
                  "Enforce a default no access policy",
                  ['The file /etc/pam.d/other should contain:\n"auth required pam_deny.so"\n"account required pam_deny.so"'],
                  ["Update /etc/pam.d/other"]],
        "PASS_COMMENT": "The configuration is set in /etc/pam.d/other.",
        "FAIL_COMMENT": "The configuration is not set in /etc/pam.d/other.",
        "PAM_OTHER": "/etc/pam.d/other"
    },
    "Section3_1": {
        "INPUT": ["3.1",
                  "Login success or failure",
                  [
                      '''
For RHEL,CENTOS, SUSE:

Requirements for systems that use syslog:

File:/etc/syslog.conf
*.info;mail.none;authpriv.none;cron.none /var/log/messages
authpriv.* /var/log/secure

Requirements for systems that use syslog-ng:

File:/etc/syslog-ng/syslog-ng.conf

    filter f_authpriv { facility(auth,authpriv); };
    destination authpriv { file("/var/log/secure"); };
    source src { internal(); };
    log { source(src); filter(f_authpriv); destination(authpriv); };

Requirements for systems that use rsyslog:

File:/etc/rsyslog.conf

$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat
*.info;mail.none;authpriv.none;cron.none /var/log/messages
authpriv.* /var/log/secure


For UBUNTU/DEBIAN

Requirements for systems that use syslog:

File:/etc/syslog.conf
auth,authpriv.* /var/log/auth.log
*.*;auth,authpriv.none -/var/log/syslog

Requirements for systems that use syslog-ng:

File:/etc/syslog-ng/syslog-ng.conf

    filter f_authpriv { facility(auth,authpriv); };
    destination authpriv { file("/var/log/secure"); };
    source src { internal(); };
    log { source(src); filter(f_authpriv); destination(authpriv); };


Requirements for systems that use rsyslog:

File:/etc/rsyslog.conf

$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat
auth,authpriv.* /var/log/auth.log
*.*;auth,authpriv.none -/var/log/syslog'
'''
                  ],
                  ["Run the command: chage -m 1 <user>"]],
        "PASS_COMMENT": "All UIDs are unique.",
        "FAIL_COMMENT": "UIDs are not unique.",
        "REQUIREMENTS_REDHAT_SYSLOG": [['*.info;mail.none;authpriv.none;cron.none', '/var/log/messages'], ['authpriv.*', '/var/log/secure']],
        "REQUIREMENTS_REDHAT_SYSLOGNG": [['filter f_authpriv', '{ facility(auth,authpriv); };'], ['destination authpriv', '{ file("/var/log/secure"); };'], ['source src', '{ internal(); };'], ['log', '{ source(src); filter(f_authpriv); destination(authpriv); };']],
        "REQUIREMENTS_REDHAT_RSYSLOG": [['$ActionFileDefaultTemplate', 'RSYSLOG_TraditionalFileFormat'], ['*.info;mail.none;authpriv.none;cron.none', '/var/log/messages']],
        "REQUIREMENTS_UBUNTU_DEBIAN_SYSLOG": [['auth,authpriv.*', '/var/log/auth.log'], ['*.*;auth,authpriv.none', '-/var/log/syslog']],
        "REQUIREMENTS_UBUNTU_DEBIAN_SYSLOGNG": [['filter', 'f_authpriv', '{', 'facility(auth,authpriv);', '};'], ['destination', 'authpriv', '{', 'file("/var/log/secure");', '};'], ['source', 'src', '{', 'internal();', '};'], ['log', '{', 'source(src);', 'filter(f_authpriv);', 'destination(authpriv);', '};']],
        "REQUIREMENTS_UBUNTU_DEBIAN_RSYSLOG": [['$ActionFileDefaultTemplate', 'RSYSLOG_TraditionalFileFormat'], ['auth,authpriv.*', '/var/log/auth.log'], ['*.*;auth,authpriv.none', '-/var/log/syslog']],
        "REQUIREMENTS_SUSE_SYSLOG": [['*.info;mail.none;authpriv.none;cron.none', '/var/log/messages'], ['authpriv.*', '/var/log/secure']],
        "REQUIREMENTS_SUSE_SYSLOGNG": [['filter', 'f_authpriv', '{', 'facility(auth,authpriv);', '};'], ['destination', 'authpriv', '{', 'file("/var/log/secure");', '};'], ['source', 'src', '{', 'internal();', '};'], ['log', '{', 'source(src);', 'filter(f_authpriv);', 'destination(authpriv);', '};']],
        "REQUIREMENTS_SUSE_RSYSLOG": [['$ActionFileDefaultTemplate', 'RSYSLOG_TraditionalFileFormat'], ['*.info;mail.none;authpriv.none;cron.none', '/var/log/messages'], ['authpriv.*', '/var/log/secure']],
        "SYSLOG_FILE": '/etc/syslog.conf',
        "SYSLOG-NG_FILE": '/etc/syslog-ng/syslog-ng.conf',
        "RSYSLOG_FILE": '/etc/rsyslog.conf',
        "RSYSLOG_DIR": '/etc/rsyslog.d/*'
    },
    "Section3_2": {
        "INPUT": ["3.2",
                  "/var/log/wtmp",
                  ["File /var/log/wtmp must exist."],
                  ["Enable /var/log/wtmp logging."]],
        "PASS_COMMENT": "The file /var/log/wtmp exists.",
        "FAIL_COMMENT": "The file /var/log/wtmp does not exists.",
        "WTMP_FILE": "/var/log/wtmp"
    },
    "Section3_3": {
        "INPUT": ["3.3",
                  "/var/log/syslog and /var/log/messages",
                  ["File /var/log/syslog (Ubuntu/Debian) or /var/log/messages (RHEL/CENTOS/SUSE) must exist."],
                  ["Enable /var/log/syslog or /var/log/messages logging."]],
        "PASS_COMMENT": "The log file exists.",
        "FAIL_COMMENT": "The log file does not exist.",
        "SYSLOG_FILE": "/var/log/syslog",
        "MESSAGES_FILE": "/var/log/messages"
    },
    "Section3_4": {
        "INPUT": ["3.4",
                  "/var/log/faillog",
                  ["File /var/log/faillog must exist if pam_tally2 is not used."],
                  ["Enable /var/log/faillog logging."]],
        "PASS_COMMENT": "The file /var/log/faillog exists.",
        "PASS_COMMENT_TALLY2": "The system is using pam_tally2.",
        "FAIL_COMMENT": "The file /var/log/faillog does not exist.",
        "FAILLOG_FILE": "/var/log/faillog",
        "LIBS_PATHS": ['/lib/security', '/lib64/security', '/lib32/security', '/lib/x86_64-linux-gnu/security', '/usr/lib/x86_64-linux-gnu/security', '/usr/lib/security', '/usr/lib64/security', '/usr/lib/security']
    },
    "Section3_5": {
        "INPUT": ["3.5",
                  "/var/log/tallylog",
                  ["File /var/log/tallylog must exist if pam_tally2 is used."],
                  ["Enable /var/log/tallylog logging."]],
        "PASS_COMMENT": "The file /var/log/tallylog exists.",
        "PASS_COMMENT_TALLY2": "The system is not using pam_tally2.",
        "FAIL_COMMENT": "The file /var/log/tallylog does not exist.",
        "TALLYLOG_FILE": "/var/log/tallylog",
        "LIBS_PATHS": ['/lib/security', '/lib64/security', '/lib32/security', '/lib/x86_64-linux-gnu/security', '/usr/lib/x86_64-linux-gnu/security', '/usr/lib/security', '/usr/lib64/security', '/usr/lib/security']
    },
    "Section3_6": {
        "INPUT": ["3.6",
                  "/var/log/auth.log and /var/log/secure",
                  ["File /var/log/auth.log (Ubuntu/Debian) or /var/log/secure (RHEL/CENTOS/SUSE) must exist."],
                  ["Enable /var/log/auth.log or /var/log/secure logging."]],
        "PASS_COMMENT": "The log file exists.",
        "FAIL_COMMENT": "The log file does not exist.",
        "AUTH_FILE": "/var/log/auth.log",
        "SECURE_FILE": "/var/log/secure"
    },
    "Section3_7": {
        "INPUT": ["3.7",
                  "Log retention"
                  ["Logs must be retained for at least 90 days for /var/log/secure.",
                   "Logs must be retained for at least 90 days for /var/log/auth.log",
                   "Logs must be retained for at least 90 days for /var/log/messages",
                   "Logs must be retained for at least 90 days for /var/log/syslog",
                   "Logs must be retained for at least 90 days for /var/log/kern.log"],
                  ["Configure log rotation in /etc/logrotate.conf",
                   "Configure log rotation in /etc/logrotate.conf",
                   "Configure log rotation in /etc/logrotate.conf",
                   "Configure log rotation in /etc/logrotate.conf",
                   "Configure log rotation in /etc/logrotate.conf"]],
        "COMMENT": "Log retention is set to {0} for {1}",
        "PASS_COMMENT_NOT_PRESENT": "Log file does not exist: ",
        "LOG_FILES": ['/var/log/secure', '/var/log/auth.log', '/var/log/messages', '/var/log/syslog', '/var/log/kern.log']
    },
    "Section4_1": {
        "INPUT": ["4.1",
                  "Ftp account home directory.",
                  ["If it exists and anonymous ftp is enabled, it must be owned by root and grant write access only to the owner"],
                  ["Update permissions on ~ftp"]],
        "PASS_COMMENT": "The ftp home directory has correct permissions.",
        "FAIL_COMMENT": "The ftp home directory has not correct permissions.",
        "PASS_COMMENT_FTP_NOT_FOUND": "FTP was not found on the server.",
        "FTP_HOME": "/home/ftp",
        "FTP_FILES": ['/etc/ftpd/ftpaccess', '/etc/vsftpd.conf', '/etc/ftpaccess', '/etc/vsftpd/vsftpd.conf']
    },


}
