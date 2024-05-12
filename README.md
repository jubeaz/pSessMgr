
# install

# define session template 
Session template is configured in the section `[session_template]` of the file `~/.psm/psm.conf`

Options to config:
* `folders`: a list of relative paths that will be created inside the session
* `symlinks`: a list of symbolic links to create inside the session. Each symbolic link is made of :
    * (first) an absolute (`~/` allowed) represnting the destination of the link
    * (second) a relative path represnting link
* `copies`: a list of files to be copied inside the session. each copie is made of:
    * (first) an absolute (`~/` allowed), source of the copie
    * (second) a relative path, destination of the copie inside the section 
* `tools`: a subset of the tools managed by psm (see `psm/tools`)

example:
```ini
folders = [
    "admin", 
    "deliverables", 
    "evidence/findings", 
    "evidence/scans", 
    "evidence/scans/vuln", 
    "evidence/scans/service", 
    "evidence/scans/web", 
    "evidence/scans/ad", 
    "evidence/osint", 
    "evidence/wireless", 
    "evidence/logging", 
    "evidence/misc", 
    "notes", 
    "notes/_template", 
    "retest", 
    "utils/windows", 
    "utils/linux"
    ]

symlinks = [
    ["/opt/windows/windows_weaponize", "utils/windows/windows_weaponize"], 
    ["/opt/windows/SharpCollection/NetFramework_4.7_x64", "utils/windows/NetFramework_4.7_x64"]
    ]

copies = [
    ["~/.config/tmuxinator/tmux-pentest.yml", "tmux-pentest.yml"], 
    ]

tools = [
    "arsenal",
    "hashcat",
    "john",
    "jwt_tool",
    "nxc",
    "sqlmap",
    "tplmap",
    ]
```


# Todo

## session 
* `build`: add controle if there is an active session since
* add a `remove tool` 


## generator
* export_etc_krb5_conf filter scope ?????????

## computer
* bloodyad dnsDump: process alias 
```
recordName: sccm.haas.local
CNAME: bran.haas.local
```
## scope
* manage scope inclusion / mixxing action type (hard problem)
## database
* upgrade computer and domain models to add foreign key constraints

# Scopes
## facts 
* must be disjoints 
* no mixed types
* default type Allow
* no scope means all IP included

## to do
* 