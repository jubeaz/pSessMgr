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

poetry run psm domain add -n NRUN -s S-1-5-21-2291914956-3290296217-2402366952 corp.local
```

# bd requests
```bash

sqlite3  -readonly ~/.psm/psm.db 'select * from sessions;'
sqlite3  -readonly /tmp/titi/.psm_session.db  'select * from domains;'

sqlite3  -readonly /tmp/titi/.psm_session.db  '.fullschema'


```

to do:
* dans la db il faut enregistrer pour chaque outil l'emplacement du fichier de config sur le fs pour s'assurer que si le template bouge.
* c'est cette valeur enregistrée qui sera utilisée pour l'activation

au process de creat

# to do
* A la creation d'une session creer la bd qui va avec.

* A l'activation d'une session s'assurer que la bd est la

* a l'ajout d'un o

