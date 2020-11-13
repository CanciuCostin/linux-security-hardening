# Linux Secure HealthCheck
 Command line application to validate secure configuration on Linux servers
 
 
<!-- TABLE OF CONTENTS -->
## Check Baseline

* [1.1 - OS Support](#1.1)



## 1. General Checks
### 1.1 - OS Support
The operating system must be under support.
Main operating systems:
* Red Hat Enterprise Linux release 8.1 -> 2021-11-30
* Red Hat Enterprise Linux release 8.2 -> 2022-04-30
* CentOS Linux release 7               -> 2024-06-30
* CentOS Linux release 8.0             -> 2029-06-30
* SUSE Linux Enterprise Server 12      -> 2024-10-31
* SUSE Linux Enterprise Server 15      -> 2028-07-31
* Ubuntu 16                            -> 2021-04-01
* Ubuntu 18                            -> 2023-04-01
            
### 1.2 - Business Use Notice
The file /etc/motd or /etc/issue must contain the MOTD.
Default MOTD: The system must only be used for conducting business or for purposes authorized by management

## 2. Password Checks
### 2.1 - Default maximum password age
File /etc/login.defs must contain the line:
```
PASS_MAX_DAYS       90
```
### 2.2 - Maximum password age per user
Maximum password age must be set to 90 days for each user in /etc/shadow (5th field).
### 2.3 - Password length and complexity
One of these two options must be implemented:     
* Parameters of "retry=3 minlen=14 dcredit=-1 ucredit=0 lcredit=-1 ocredit=0" in /etc/pam.d/$PAMFILE    
* parameters of "min=disabled,14,14,14,14 passphrase=0 random=0 enforce=everyone" in /etc/pam.d/$PAMFILE   
  
Note: $PAMFILE will be 'common-password' for SUSE and Debian, for all other distributions will be:'system-auth'
Note: For Red Hat Enterprise Linux V6 and later:  The same entry chosen for system-auth file must ADDITIONALLY be included in the /etc/pam.d/password-auth file.
Note: any two credits of -1 are required and they can be replaced by the minclass=2 parameter.
### 2.4 - Default minimum password age
File /etc/login.defs must contain the line:
```
PASS_MIN_DAYS       1
```
### 2.5 - Minimum password age per user
Minimum password age must be set to 1 day for each user in /etc/shadow (4th field).
