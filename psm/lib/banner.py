# https://patorjk.com/software/taag/#p=display&f=Bloody&t=PSM
__version__ = "0.1.0"
__author__ = "jubeaz"


def show_banner():
    banner = f"""
 ██▓███    ██████  ███▄ ▄███▓
▓██░  ██▒▒██    ▒ ▓██▒▀█▀ ██▒
▓██░ ██▓▒░ ▓██▄   ▓██    ▓██░
▒██▄█▓▒ ▒  ▒   ██▒▒██    ▒██ 
▒██▒ ░  ░▒██████▒▒▒██▒   ░██▒
▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░░ ▒░   ░  ░
░▒ ░     ░ ░▒  ░ ░░  ░      ░
░░       ░  ░  ░  ░      ░   
               ░         ░   

                        v{__version__}                   
                        @{__author__}                    
    
    
    """
    print(banner)


def small_banner():
    banner = f"""psm v{__version__} by @{__author__}"""

    print(banner)
