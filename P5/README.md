# Project 5 - Linux-based Server Configuration
## About
The goal is to take a baseline Ubuntu virtual machine and prepare it to host a
web application provided. The VM must be configured to protect against a
variety of common attacks and host the web application so that it functions
appropriately.

## SSH access
To gain access to the VM using ssh, issue the command:

`ssh -i <KEY_FILE> grader@52.37.83.120 -p 2200`


## HTTP access
To access the hosted web application, visit:
`http://ec2-52-37-83-120.us-west-2.compute.amazonaws.com/`


## Installed software

### Server packages
1. ntp
2. apache2
3. libapache2-mod-wsgi
4. postgresql
5. git
6. python-pip
7. python-dev
8. postgresql-server-dev-all
9. fail2ban
10. sendmail
11. iptables-persistent
12. apticron

### Python packages (pip installations)
1. Flask
2. SQLAlchemy
3. bleach
4. GitHub-Flask
5. psycopg2
6. virtualenv


## Additional functionality
1. The firewall has been configured to monitor for repeat unsuccessful login
attempts and appropriately ban attackers through `fail2ban` .

2. A cron script is included to automatically manage package updates using
`aptitude`. See `/etc/cron.weekly/apt-security-updates`  for configuration
details and the corresponding logrotate  entry at
`/etc/logrotate.d/apt-security-updates`.

3. The VM includes monitoring for OS security patches by using `apticron`. The
cron file is located at `/etc/cron.d/apticron` and the corresponding
configuration file at `/etc/apticron/apticron.conf`.
