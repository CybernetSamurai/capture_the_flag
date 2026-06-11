# CTF: File Transfer Protocol Basics

__MASTER HANDBOOK 2026.02__

DESCRIPTION: Enumerate an FTP server, retrieve files, and identify common security mistakes
associated with legacy protocols.

DIFFICULTY: Novice

ESTIMATED TIME: 10 minutes

TARGET: ftp.corp.net (172.31.27.121)

OBJECTIVES:
+ Connect to an FTP service using anonymous authentication
+ Download files of interest
+ Navigate directories and identify hidden files

## PART 0x00 -- Initial Access

Connect to the FTP server and attempt to authenticate. Determine whether
Anonymous login is permitted.

_Command_

```
$ tnftp ftp://anonymous:@ftp.corp.net
```

_Expected Output_

```
Connected to ftp.corp.net.
220- ________________________________
220-/ Welcome to the Very Secure FTP \
220-\ Server                         /
220- --------------------------------
220-        \   ^__^
220-         \  (oo)\_______
220-            (__)\       )\/\
220-                ||----w |
220-                ||     ||
220-
220-This server was used for internal backups.
220-Some files may no longer be relevant.
220-
220-Nothing important to find here...
220
331 Please specify the password.
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
200 Switching to Binary mode.
ftp>
```

## PART 0x01 -- File Enumeration

Once authenticated, perform a directory listing and look for files that may
contain sensitive information or flags.

_Command(s)_

```
ftp> ls
150 Here comes the directory listing.
-rw-r--r--    1 0        0             378 Jan 16 01:36 README.txt
drwxr-xr-x    3 0        0              62 Jan 16 01:45 backups
-rw-r--r--    1 0        0              31 Jan 16 01:43 flag_01.txt
drwxr-xr-x    3 0        0              40 Jan 16 01:50 public
drwxr-xr-x    2 0        0              43 Jan 16 01:42 staff
226 Directory send OK.
ftp> get /flag_01.txt
```

_Flag\_01_

```
FLAG{d1sabl3_anonym0us_l0g1n5}
```

## PART 0x02 -- Hidden Files

Explore the filesystem further and look for additional interesting files and
hidden artifacts.

_Command(s)_

```
ftp> cd /backups
ftp> ls -a
150 Here comes the directory listing.
drwxr-xr-x    3 0        0              62 Jan 16 01:45 .
drwxr-xr-x    5 0        0              85 Jan 16 01:43 ..
-rw-r--r--    1 0        0              31 Jan 16 01:45 .flag_02.txt
-rw-r--r--    1 0        0             150 Jan 16 01:45 notes.txt
drwxr-xr-x    2 0        0              25 Jan 16 02:18 old_configs
226 Directory send OK.
ftp> get /backups/.flag_02.txt
```

_Flag\_02:_

```
FLAG{h1dd3n_fi1es_arn7_5ecur3}
```

----

EOF
