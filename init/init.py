#!/usr/bin/env python3

import os
import yaml
import sys

def init(source: str) -> str:
    os.system("cp /opt/wd/t* /data/")    
    return "init"


if __name__ == "__main__":
    # Make sure that at least one argument is given, that is either 'write' or 'read'
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} write|read")
        exit(1)

    # If it checks out, call the appropriate function
    command = sys.argv[1]
    if command == "init":
        print(yaml.dump({ "contents": init(os.environ["SOURCE"]) }))
