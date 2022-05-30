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

def Ticket(source: str) -> str:
    try:
        data = pd.read_csv(f"/data/{source}.csv")

        data['Ticket'].value_counts()

        Ticket_Count = dict(data['Ticket'].value_counts())
        data['Ticket_Class'] = data['Ticket'].apply(lambda x: Ticket_Count[x])
        sns.barplot(x='Ticket_Class', y='Survived', data=data)
        plt.savefig(f"/data/Ticket_{source}.png")
        plt.close()
        return "Figure saved to \"/data/Ticket{source}.png\""
    except:
        return f"Error: {e} ({e.errno})"

def Title(source: str) -> str:
    try:
        data = pd.read_csv(f"/data/{source}.csv")

        # Name processing
        # Title Feature(New)
        data['Title'] = data['Name'].apply(lambda x: x.split(',')[1].split('.')[0].strip())
        data['Title'].replace(['Mr'], 'Mr', inplace=True)
        data['Title'].replace(['Mlle', 'Miss'], 'Miss', inplace=True)
        data['Title'].replace(['Mme', 'Ms', 'Mrs'], 'Mrs', inplace=True)
        data['Title'].replace(['Capt', 'Col', 'Major', 'Dr', 'Rev'], 'Officer', inplace=True)
        data['Title'].replace(['Don', 'Sir', 'the Countess', 'Dona', 'Lady'], 'Royalty', inplace=True)
        data['Title'].replace(['Master', 'Jonkheer'], 'Master', inplace=True)

        sns.barplot(x="Title", y="Survived", data=data)

        plt.savefig(f"/data/Title_{source}.png")
        plt.close()
        return "Figure saved to \"/data/Title{source}.png\""
    except:
        return f"Error: {e} ({e.errno})"

def Correlation(source: str) -> str:
    try:
        data = pd.read_csv(f"/data/{source}.csv")

        data['Sex'] = data['Sex'].map({'male': 0, 'female': 1})
        data['Embarked'] = data['Embarked'].fillna('S')
        data['Embarked'] = data['Embarked'].map({'S': 0, 'C': 1, 'Q': 2})
        data['Family'] = data['SibSp'] + data['Parch']
        data = data[[col for col in data.columns if col != 'Survived'] + ['Survived']]
        corr = data.corr()

        sns.color_palette(sns.diverging_palette(230, 20))

        fig, ax = plt.subplots(1, 1, figsize=(7, 7))

        mask = np.zeros_like(corr, dtype=np.bool)
        mask[np.triu_indices_from(mask)] = True

        cmap = sns.diverging_palette(230, 20, as_cmap=True)

        sns.heatmap(corr,
                    square=True,
                    mask=mask,
                    linewidth=2.5,
                    vmax=0.4, vmin=-0.4,
                    cmap=cmap,
                    cbar=False,
                    ax=ax)

        ax.set_yticklabels(ax.get_xticklabels(), fontfamily='serif', rotation=0, fontsize=11)
        ax.set_xticklabels(ax.get_xticklabels(), fontfamily='serif', rotation=90, fontsize=11)

        ax.spines['top'].set_visible(True)

        plt.tight_layout()
        plt.show()

        plt.savefig(f"/data/Correlation_{source}.png")
        plt.close()

        return "Figure saved to \"/data/Correlation{source}.png\""
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
    elif command == "Ticket":
        print(yaml.dump({ "contents": Ticket(os.environ["SOURCE"]) }))
    elif command == "Title":
        print(yaml.dump({ "contents": Title(os.environ["SOURCE"]) }))
    elif command == "Correlation":
        print(yaml.dump({ "contents": Correlation(os.environ["SOURCE"]) }))
    # Done!
