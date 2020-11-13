# Linux Secure HealthCheck
 Command line application to validate secure configuration on Linux servers
 
 
<!-- TABLE OF CONTENTS -->
## Check Baseline

* [1.1 - OS Support](#1.1)



## 1. General Rules
### 1.1 - OS Support
* The operating system must be under support.
   * Red Hat Enterprise Linux release 8.1 -> 2021-11-30
   * Red Hat Enterprise Linux release 8.2 -> 2022-04-30
   * CentOS Linux release 7               -> 2024-06-30
   * CentOS Linux release 8.0             -> 2029-06-30
   * SUSE Linux Enterprise Server 12      -> 2024-10-31
   * SUSE Linux Enterprise Server 15      -> 2028-07-31
   * Ubuntu 16                            -> 2021-04-01
   * Ubuntu 18                            -> 2023-04-01
            
### 1.2 - Business Use Notice
* The file /etc/motd or /etc/issue must contain the MOTD.
   * Default MOTD: The system must only be used for conducting business or for purposes authorized by management

## 2. Password Controls
### 2.1 - Default maximum password age
* File /etc/login.defs must contain the line:
```
PASS_MAX_DAYS       90
```
### 2.2 - Maximum password age per user
* Maximum password age must be set to 90 days for each user in /etc/shadow (5th field).
### 2.3 - Password length and complexity
* One of these two options must be implemented:     
   * Parameters of "retry=3 minlen=14 dcredit=-1 ucredit=0 lcredit=-1 ocredit=0" in /etc/pam.d/$PAMFILE    
   * Parameters of "min=disabled,14,14,14,14 passphrase=0 random=0 enforce=everyone" in /etc/pam.d/$PAMFILE   
  
   Note: $PAMFILE will be 'common-password' for SUSE and Debian, for all other distributions will be:'system-auth'

   Note: For Red Hat Enterprise Linux V6 and later:  The same entry chosen for system-auth file must ADDITIONALLY be included in the /etc/pam.d/password-auth file.

   Note: any two credits of -1 are required and they can be replaced by the minclass=2 parameter.
### 2.4 - Default minimum password age
* File /etc/login.defs must contain the line:
```
PASS_MIN_DAYS       1
```
### 2.5 - Minimum password age per user
* Minimum password age must be set to 1 day for each user in /etc/shadow (4th field).

### 2.6 - Password history
* The files /etc/pam.d/system-auth and /etc/pam.d/password-auth (RHEL/CENTOS) or /etc/pam.d/common-password (Ubuntu/Debian/SuSE) must include:
```
password $CONTROL $PAM_MODULE remember=7 use_authtok sha512 shadow
```

 Where $CONTROL is required or sufficient, and $PAM_MODULE is pam_unix.so  or pam_pwhistory.so

### 2.7 - Maximum login retries
* File /etc/pam.d/system-auth and /etc/pam.d/password-auth (RHEL/CENTOS) or /etc/pam.d/common-auth (UBUNTU/DEBIAN/SUSE) must contain:
auth required $PAM_MODULE deny=5

### 2.8 - Prevent UID and GID reuse
* All user ids must be unique in /etc/passwd

* All group ids must be unique in /etc/group

### 2.9 - Enforce a default no access policy
* The file /etc/pam.d/other should contain:\n"auth required pam_deny.so"\n"account required pam_deny.so"

## 3. Logging Controls
### 3.1 - Login success or failure
* For RHEL,CENTOS, SUSE:
   * Requirements for systems that use syslog:
```
File:/etc/syslog.conf
*.info;mail.none;authpriv.none;cron.none /var/log/messages
authpriv.* /var/log/secure
```
   * Requirements for systems that use syslog-ng:
```
File:/etc/syslog-ng/syslog-ng.conf
    filter f_authpriv { facility(auth,authpriv); };
    destination authpriv { file("/var/log/secure"); };
    source src { internal(); };
    log { source(src); filter(f_authpriv); destination(authpriv); };
```
   * Requirements for systems that use rsyslog:
```
File:/etc/rsyslog.conf
$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat
*.info;mail.none;authpriv.none;cron.none /var/log/messages
authpriv.* /var/log/secure
For UBUNTU/DEBIAN
```
   * Requirements for systems that use syslog:
```
File:/etc/syslog.conf
auth,authpriv.* /var/log/auth.log
*.*;auth,authpriv.none -/var/log/syslog
```
   * Requirements for systems that use syslog-ng:
```
File:/etc/syslog-ng/syslog-ng.conf
    filter f_authpriv { facility(auth,authpriv); };
    destination authpriv { file("/var/log/secure"); };
    source src { internal(); };
    log { source(src); filter(f_authpriv); destination(authpriv); };
```
   * Requirements for systems that use rsyslog:
```
File:/etc/rsyslog.conf
$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat
auth,authpriv.* /var/log/auth.log
*.*;auth,authpriv.none -/var/log/syslog
```

### 3.2 - /var/log/wtmp
* File /var/log/wtmp must exist.

### 3.3 - /var/log/syslog and /var/log/messages
* File /var/log/syslog (Ubuntu/Debian) or /var/log/messages (RHEL/CENTOS/SUSE) must exist.

### 3.4 - /var/log/faillog
* File /var/log/faillog must exist if pam_tally2 is not used.

### 3.5 - /var/log/tallylog
* File /var/log/tallylog must exist if pam_tally2 is used.

### 3.6 - /var/log/auth.log and /var/log/secure
* File /var/log/auth.log (Ubuntu/Debian) or /var/log/secure (RHEL/CENTOS/SUSE) must exist.

### 3.7 - Log retention
* Logs must be retained for at least 90 days for /var/log/secure.
* Logs must be retained for at least 90 days for /var/log/auth.log.
* Logs must be retained for at least 90 days for /var/log/messages.
* Logs must be retained for at least 90 days for /var/log/syslog.
* Logs must be retained for at least 90 days for /var/log/kern.log.


## 4. Authorization Controls
### 4.1 - Ftp account home directory.
* If it exists and anonymous ftp is enabled, it must be owned by root and grant write access only to the owner
