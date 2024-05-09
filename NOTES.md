# commands to test

## session

### regular (without system files)
```bash
cp -r ~/documents/pentesting-games/prolabs/nrunner/evidence/logging/nxc ~/.nxc-psm ; cp ~/.arsenal.json ~/.arsenal.json-psm ; cp -r ~/documents/pentesting-games/prolabs/nrunner/evidence/logging/sqlmap/ ~/.local/share/sqlmap-psm



rm -rf ~/.psm ; rm -rf titi ; rm -rf /tmp/titi ; poetry run psm session build -p /tmp titi  ; poetry run psm session activate titi

rm -f ~/.



ls -al ~/ | grep .nxc-psm ; ls -al ~/.nxc-psm/; ls -al ~/.arsenal.json-psm*; ls -al ~/.local/share/ | grep sqlmap-psm ; ls -al ~/.local/share/sqlmap/; 


rm -rf ~/.psm ; rm -rf titi ; rm -rf /tmp/titi ; poetry run psm session build -p /tmp titi  ; poetry run psm session activate titi; poetry run psm session add titi sqlmap


poetry run psm session deactivate titi
```

### with system file
```bash
sudo -E rm  -rf ~/.psm ; sudo -E  rm -rf titi ; sudo  -E rm -rf  /tmp/titi ; poetry run sudo -E psm session build -p /tmp titi  ; poetry run sudo -E  psm session activate titi
```

## domain
```bash
poetry run psm domain list

poetry run psm domain add nrunner.local
poetry run psm domain add research.nrunner.local

poetry run psm domain update -n NRUN -s S-1-5-21-2291914956-3290296217-2402366952 nrunner.local
poetry run psm domain target nrunner.local
poetry run psm domain target research.nrunner.local
poetry run psm domain activate research.nrunner.local
poetry run psm domain activate nrunner.local
poetry run psm domain update -n RESEARCH -s S-1-5-21-2291914956-3290296217-2402366952 research.nrunner.local
poetry run psm domain update -n RESEARCH -s S-1-5-21-0-0-0 research.nrunner.local
```

## computer
```bash
poetry run psm computer purge
poetry run psm computer list
poetry run psm computer add 10.10.0.2

poetry run psm computer add 10.10.1.1 
poetry run psm computer add-fqdn 10.10.1.1 a.fr 
poetry run psm computer add-fqdn 10.10.1.1 c.com
poetry run psm computer remove-fqdn 10.10.1.1 c.com
poetry run psm computer add 10.10.1.2
poetry run psm computer add-fqdn 10.10.1.2 b.fr
poetry run psm computer add 10.10.1.3
poetry run psm computer add-fqdn 10.10.1.3 c.fr


poetry run psm computer add 10.10.2.1 
poetry run psm computer add-fqdn 10.10.2.1 a.x.fr 
poetry run psm computer add 10.10.2.2
poetry run psm computer add-fqdn 10.10.2.2 b.x.fr
poetry run psm computer add 10.10.2.3
poetry run psm computer add-fqdn 10.10.2.3 c.x.fr


poetry run psm computer add-role 10.10.1.1 smb
poetry run psm computer add-role 10.10.1.1 dc
poetry run psm computer add-role 10.10.1.1 mssql
poetry run psm computer remove-role 10.10.1.1 mssql
poetry run psm computer update -s dc01 10.10.1.1 
```

# scope

```bash
# test overlapping
poetry run psm scope add 172.16.1.0/24
poetry run psm scope add 172.16.2.0/24
poetry run psm scope add 172.16.3.0/24
poetry run psm scope add 172.16.4.0/24
poetry run psm scope add 172.16.0.0/16
poetry run psm scope add 10.0.8.0/24
poetry run psm scope add 10.0.0.0/8
poetry run psm scope add 10.1.0.0/16
poetry run psm scope add 10.1.8.0/24



# real
poetry run psm scope purge
poetry run psm scope list
poetry run psm scope add --action block 10.10.2.0/24
poetry run psm scope add --action block 10.10.0.0/16
poetry run psm scope add --action block 10.10.1.1


poetry run psm scope add  10.10.2.0/24
```

# exporter
```bash
poetry run psm generator export-etc-hosts
```

# bd requests
```bash

sqlite3  -readonly ~/.psm/psm.db 'select * from sessions;'
sqlite3  -readonly /tmp/titi/.psm_session.db  'select * from domains;'

sqlite3  -readonly /tmp/titi/.psm_session.db  '.fullschema'
```

