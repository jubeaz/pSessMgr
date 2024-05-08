# commands to test

## session
```bash
cp -r ~/documents/pentesting-games/prolabs/nrunner/evidence/logging/nxc ~/.nxc-psm ; cp ~/.arsenal.json ~/.arsenal.json-psm ; cp -r ~/documents/pentesting-games/prolabs/nrunner/evidence/logging/sqlmap/ ~/.local/share/sqlmap-psm



rm -rf ~/.psm ; rm -rf titi ; rm -rf /tmp/titi ; poetry run psm session build -p /tmp titi  ; poetry run psm session activate titi

rm -f ~/.



ls -al ~/ | grep .nxc-psm ; ls -al ~/.nxc-psm/; ls -al ~/.arsenal.json-psm*; ls -al ~/.local/share/ | grep sqlmap-psm ; ls -al ~/.local/share/sqlmap/; 


rm -rf ~/.psm ; rm -rf titi ; rm -rf /tmp/titi ; poetry run psm session build -p /tmp titi  ; poetry run psm session activate titi; poetry run psm session add titi sqlmap


poetry run psm session deactivate titi
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
poetry run psm computer list
poetry run psm computer add 10.10.1.1
poetry run psm computer add-fqdn 10.10.1.1 a.fr
poetry run psm computer add-fqdn 10.10.1.1 b.fr
poetry run psm computer add-fqdn 10.10.1.1 c.com

poetry run psm computer add-role 10.10.1.1 smb
poetry run psm computer update -s c 10.10.1.1 
```

# scope
```bash
poetry run psm scope list
poetry run psm scope add --excluded 172.16.0.2
poetry run psm scope add --excluded 172.16.0.2/24
```

# bd requests
```bash

sqlite3  -readonly ~/.psm/psm.db 'select * from sessions;'
sqlite3  -readonly /tmp/titi/.psm_session.db  'select * from domains;'

sqlite3  -readonly /tmp/titi/.psm_session.db  '.fullschema'
```

