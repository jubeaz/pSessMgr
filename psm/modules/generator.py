from psm.modules.domain import PSMDomain
from psm.modules.computer import PSMComputer
from psm.modules.scope import PSMScope
from psm.logger import psm_logger



class PSMGenerator:
    psm_computer = None
    psm_domain = None
    psm_scope = None

    def __init__(self):
        self.psm_computer = PSMComputer()
        self.psm_domain = PSMDomain()
        self.psm_scope = PSMScope()


    def export_etc_hosts(self):
        computers = self.psm_computer.get_ip_fqdns()
        # filter by scopes
        r = self.psm_scope.filter_computer_dict(computers)
        for ip, v in r.items():
            print(f"{ip} {", ".join(v)}")


    def export_ip_list(self):
        # get hosts
        computers = self.psm_computer.get_dict()
        # filter by scopes
        r = self.psm_scope.filter_computer_dict(computers)
        for ip in r:
            print(f"{ip}")


    def export_fqdn_list(self):
        # get hosts
        computers = self.psm_computer.get_dict()
        # filter by scopes
        r = self.psm_scope.filter_computer_dict(computers)
        for ip, v in r.items():
            if v["fqdns"]:
                print(f"{'\n'.join(v["fqdns"])}")
            else:
                print(ip)     

    def export_etc_krb5_conf(self):
        # get hosts
        domains = self.psm_domain.get_dict()
        for fqdn, v in domains.items():
            if v["dc_ip"]:
                try: 
                    c = self.psm_computer.get(v["dc_ip"])
                    if c.fqdns:
                        print(f"{fqdn.upper()} = {{ kdc = {c.fqdns[0]} }}")
                except Exception: 
                    psm_logger.info(f"Referenced DC for {fqdn} with ip {v["dc_ip"]} not found")
