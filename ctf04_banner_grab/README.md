# CTF: Banner Grabbing Basics

__MASTER HANDBOOK 2026.02__

DESCRIPTION: Banner grabbing is a reconnaissance technique used to identify services, applications, or custom listeners running on open ports. Many services reveal identifying information immediately upon connection, which can assist attackers in service enumeration and vulnerability research.

In this challenge, you will perform increasingly thorough port scans and manually connect to discovered services to retrieve exposed banners. Keep in mind that there are many ways to complete this challenge.

DIFFICULTY: Novice

ESTIMATED TIME: 5 minutes

TARGET: banner.corp.net (172.31.27.124)

OBJECTIVES:
+ Perform fast, standard, and full TCP port scans
+ Observe how scan depth impacts discovery
+ Manually connect to open ports to retrieve banners

## PART 0x00 -- Fast Scan

Using Nmap, perform a fast scan with the `-F` switch to quickly identify the top 100 commonly used ports.

For sections 0x00 - 0x02, answer the following questions...

_Questions:_
+ What listing port was discovered?
+ Is port considered well-known, registered, or ephemeral?
+ What service (if any) is typically found on this port?

_Command:_

```
$ nmap -F banner.corp.net
```

_Expected Output:_

```
PORT    STATE SERVICE
110/tcp open  pop3
```

_Answers:_

```
Port 110, well-known, pop3
```

## PART 0x01 -- Normal Scan

Using Nmap, perform a standard TCP scan (no switches) against the target. This covers the top 1,000 most commonly used ports.

_Command(s):_

```
$ nmap banner.corp.net
```

_Expected Output:_

```
PORT     STATE SERVICE
110/tcp  open  pop3
9001/tcp open  tor-orport
```

_Answers:_

```
Port 9001, registered, tor-orport
```

## PART 0x02 -- Full Port Scan

Perform a complete TCP scan against all 65,535 ports.

_Command(s):_

```
$ nmap --open -p- banner.corp.net
```

_Expected Output:_

```
PORT      STATE SERVICE
110/tcp   open  pop3
9001/tcp  open  tor-orport
55389/tcp open  unknown
```

_Answers:_

```
Port 55389, ephemeral, N/A
```

## PART 0x03 -- Banner Grabbing

Use `netcat` (`nc`) to manually connect to each discovered port and observe the service banner.

_Commands:_

```
$ nc banner.corp.net 110
$ nc banner.corp.net 9001
$ nc banner.corp.net 55389
```

_Flags:_

```
FLAG{id1YnQWd}
FLAG{FkdENVQm}
FLAG{TvKxYN9Q}
```

----

EOF
