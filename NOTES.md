# commands to test

# commands to test

## session

### regular (without system files)
```bash
rm -rf ~/.psm ; rm -rf /tmp/psm_test 
poetry run psm session build -p /tmp psm_test  
poetry run psm session activate psm_test
poetry run psm session add psm_test xxxxxxx
poetry run psm session deactivate psm_test
```

### with system file
```bash
sudo -E rm  -rf ~/.psm ; sudo -E  rm -rf titi ; sudo  -E rm -rf  /tmp/titi ; poetry run sudo -E psm session build -p /tmp titi  ; poetry run sudo -E  psm session activate titi
```

## domain
```bash
poetry run psm domain list

poetry run psm domain add haas.local
poetry run psm domain add weyland.local
poetry run psm domain add research.weyland.local

poetry run psm domain update -n HAAS --dc 172.16.0.1 haas.local
poetry run psm domain update -n WEYLAND --dc 172.16.1.1 weyland.local
poetry run psm domain update -n RESEARCH --dc 172.16.2.1 research.weyland.local

poetry run psm domain target weyland.local
poetry run psm domain target haas.local
poetry run psm domain activate research.weyland.local
poetry run psm domain activate weyland.local
```

## computer
https://libnmap.readthedocs.io/en/latest/index.html#

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

poetry run psm computer import-nmap  ./tests/files/nmap_ping.xml
poetry run psm computer import-nmap --store-details ./tests/files/nmap_fullscan.xml

poetry run psm computer import-bloodyad ./tests/files/boodyad_dnsdump.txt
poetry run psm computer import-adidnsdump ./tests/files/adidnsdump.csv


poetry run psm computer set-fact defender '{"satus":"Running", "extension_exception": ["ps1", ".exe'], "path_exception": []}'
poetry run psm computer purge
poetry run psm computer list
```

### export nxc check_conf

```bash
sqlite3  -readonly /tmp/psm_test/.nxc/workspaces/default/smb.db '.mode json'  'select h.ip, c.name, r.secure, r.reasons from conf_checks_results as r left join hosts as h on r.host_id == h.id left join conf_checks as c on r.check_id == c.id'

```


## scope

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

## exporter
```bash
poetry run psm generator export-etc-hosts
poetry run psm generator export-ip
poetry run psm generator export-fqdn
poetry run psm generator export-etc-krb5-conf
poetry run psm generator arsenal.conf
```

## bd requests
```bash

sqlite3  -readonly ~/.psm/psm.db 'select * from sessions;'
sqlite3  -readonly /tmp/titi/.psm_session.db  'select * from domains;'

sqlite3  -readonly /tmp/titi/.psm_session.db  '.fullschema'
```

