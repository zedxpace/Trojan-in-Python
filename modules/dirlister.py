#This little snippet code simply exposes a run function that allows that lists all of the filesin current directory and returns that lists as a string. 
import os
def run(**args):
    print("[*] In dirlister module")
    files = os.listdir(".")
    return str(files)
    
        


