#!/usr/bin/env python3

import os
import sys
import yaml
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# The function

def gender(source: str) -> str:
    try:
        if source == "train":
            data = pd.read_csv(f"/data/train.csv")
        elif source == "test":
            data = pd.read_csv(f"/data/test.csv")
        else:
            return f"Source Error"

        sns.barplot(x="Sex", y="Survived", data=data)
        plt.savefig(f"/data/gender_{source}.png")
        plt.close("all")
        return "Figure saved to \"/data/gender{source}.png\""
    except IOError as e:
        return f"ERROR: {e} ({e.errno})"

def pclass(source: str) -> str:
    try:
        data = pd.read_csv(f"/data/{source}.csv")

        sns.barplot(x="Pclass", y="Survived", data=data)
        plt.savefig(f"/data/pclass_{source}.png")
        plt.close()
        return "Figure saved to \"/data/pclass{source}.png\""
    except:
        return f"Error: {e} ({e.errno})"



# The entrypoint of the script
if __name__ == "__main__":
    # Make sure that at least one argument is given, that is either 'write' or 'read'
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} write|read")
        exit(1)

    # If it checks out, call the appropriate function
    command = sys.argv[1]
    if command == "gender":
        print(yaml.dump({ "contents": gender(os.environ["SOURCE"]) }))
    elif command == "pclass":
        print(yaml.dump({ "contents": pclass(os.environ["SOURCE"]) }))
    # Done!
