```bash
rm -rf ~/.psm ; rm -rf titi ; rm -rf /tmp/titi ; poetry run psm session build titi  ; poetry run psm session build -p /tmp titi

rm -rf ~/.psm ; rm -rf titi ; rm -rf /tmp/titi ; poetry run psm session build titi  ;  poetry run psm session destroy titi


rm -rf ~/.psm ; rm -rf titi ; rm -rf /tmp/titi ; poetry run psm session build titi  ; poetry run psm session activate titi


poetry run psm session build -p /tmp titi


sqlite3  -readonly ~/.psm/psm.db 'select * from sessions;'

rm -f ~/.

cp -r ~/documents/pentesting-games/prolabs/nrunner/evidence/logging/nxc ~/.nxc-psm ; cp ~/.arsenal.json ~/.arsenal.json-psm ; cp -r ~/documents/pentesting-games/prolabs/nrunner/evidence/logging/sqlmap/ ~/.local/share/sqlmap-psm


ls -al ~/ | grep .nxc-psm ; ls -al ~/.nxc-psm/; ls -al ~/.arsenal.json-psm*; ls -al ~/.local/share/ | grep sqlmap-psm ; ls -al ~/.local/share/sqlmap/; 

poetry run psm session activate titi

poetry run psm session deactivate titi

rm -rf ~/.psm ; rm -rf titi ; rm -rf /tmp/titi ; poetry run psm session build -p /tmp titi  ; poetry run psm session activate titi; poetry run psm session add titi sqlmap
```


to do:
* dans la db il faut enregistrer pour chaque outil l'emplacement du fichier de config sur le fs pour s'assurer que si le template bouge.
* c'est cette valeur enregistrée qui sera utilisée pour l'activation

au process de creat