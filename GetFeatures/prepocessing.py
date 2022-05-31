#!/usr/bin/env python3

import yaml
import sys
import os
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor

def processing(source: str) -> str:

    train = pd.read_csv(f"/data/train.csv")
    test = pd.read_csv(f"/data/test.csv")

    whole_data = pd.concat([train,test], ignore_index = True)

        # Name processing
        #Title Feature(New)
    whole_data['Title'] = whole_data['Name'].apply(lambda x:x.split(',')[1].split('.')[0].strip())
    whole_data['Title'].replace(['Mr'], 'Mr', inplace=True)
    whole_data['Title'].replace(['Mlle', 'Miss'], 'Miss', inplace=True)
    whole_data['Title'].replace(['Mme', 'Ms', 'Mrs'],'Mrs', inplace=True)
    whole_data['Title'].replace(['Capt', 'Col', 'Major', 'Dr', 'Rev'],'Officer', inplace=True)
    whole_data['Title'].replace(['Don', 'Sir', 'the Countess', 'Dona', 'Lady'], 'Royalty', inplace=True)
    whole_data['Title'].replace(['Master','Jonkheer'],'Master', inplace=True)

    #Treatment of family characteristics
    whole_data['Family'] = whole_data['SibSp'] + whole_data['Parch'] + 1

    #Classfication : Family label
    def Family_label(z):
        if (z > 7):
            return 0
        elif (z >= 2) & (z <=4):
            return 2
        elif ((z > 4) & (z <= 7)) | (z == 1):
            return 1
    whole_data['Family_label'] = whole_data['Family'].apply(Family_label)

    # 'Cabin' data processing
    whole_data['Cabin'] = whole_data['Cabin'].fillna("Unknown")
    whole_data['Deck'] = whole_data['Cabin'].str.get(0)

    # 'Ticket' processing
    whole_data['Ticket'].value_counts()

    Ticket_Count = dict(whole_data['Ticket'].value_counts())
    whole_data['Ticket_Class'] = whole_data['Ticket'].apply(lambda x:Ticket_Count[x])

    ##Todo: 存Ticket_Class ， Survived -> ticket.csv

    # The survival rate of 'tickets' from 2 to 4 is higher than all others
    def Ticket_Label(t):
        if (t > 8):
            return 0
        elif ((t > 4) & (t <= 8)) | (t == 1):
            return 1
        elif (t >= 2) & (t <= 4):
            return 2

    whole_data['Ticket_Class'] = whole_data['Ticket_Class'].apply(Ticket_Label)

    #Embarked number
    whole_data[whole_data['Embarked'].isnull()]
    whole_data.groupby(by=["Pclass",'Embarked']).Fare.median()
    whole_data['Embarked'] = whole_data['Embarked'].fillna('C')
    whole_data[whole_data['Fare'].isnull()]

    fare=whole_data[(whole_data['Embarked'] == "S") & (whole_data['Pclass'] == 3)].Fare.median()
    whole_data['Fare']=whole_data['Fare'].fillna(fare)

    agedf = whole_data[['Age', 'Pclass','Sex','Title']]
    agedf = pd.get_dummies(agedf)
    know_age = agedf[agedf.Age.notnull()].values
    unknow_age = agedf[agedf.Age.isnull()].values
    y = know_age[:, 0]
    x = know_age[:, 1:]
    random = RandomForestRegressor(random_state=0, n_estimators=100, n_jobs=-1)
    random.fit(x, y)
    predict_Ages = random.predict(unknow_age[:, 1::])
    whole_data.loc[ (whole_data.Age.isnull()), 'Age' ] = predict_Ages

    whole_data['Surname']=whole_data['Name'].apply(lambda x:x.split(',')[0].strip())
    Surname_Count = dict(whole_data['Surname'].value_counts())
    whole_data['FamilyGroup'] = whole_data['Surname'].apply(lambda x:Surname_Count[x])
    Female_Child_Group=whole_data.loc[(whole_data['FamilyGroup']>=2) & ((whole_data['Age']<=12) | (whole_data['Sex']=='female'))]
    Male_Adult_Group=whole_data.loc[(whole_data['FamilyGroup']>=2) & (whole_data['Age']>12) & (whole_data['Sex']=='male')]

    Female_Child=pd.DataFrame(Female_Child_Group.groupby('Surname')['Survived'].mean().value_counts())
    Female_Child.columns=['GroupCount']

    Male_Adult=pd.DataFrame(Male_Adult_Group.groupby('Surname')['Survived'].mean().value_counts())
    Male_Adult.columns=['GroupCount']

    Female_Child_Group=Female_Child_Group.groupby('Surname')['Survived'].mean()
    Dead_List=set(Female_Child_Group[Female_Child_Group.apply(lambda x:x==0)].index)

    Male_Adult_List=Male_Adult_Group.groupby('Surname')['Survived'].mean()
    Survived_List=set(Male_Adult_List[Male_Adult_List.apply(lambda x:x==1)].index)

    whole_data.to_csv(f"/data/data_for_visual.csv")

    if source == "train":

        train=whole_data.loc[whole_data['Survived'].notnull()]
        whole_data=whole_data[['Survived','Pclass','Sex','Age','Fare','Embarked','Title','Family_label','Deck','Ticket_Class']]
        whole_data=pd.get_dummies(whole_data)
        train=whole_data[whole_data['Survived'].notnull()]

        train.to_csv(f"/data/{source}_traindata.csv")

    if source == "test":

        test=whole_data.loc[whole_data['Survived'].isnull()]
        test.loc[(test['Surname'].apply(lambda x:x in Dead_List)),'Sex'] = 'male'
        test.loc[(test['Surname'].apply(lambda x:x in Dead_List)),'Age'] = 60
        test.loc[(test['Surname'].apply(lambda x:x in Dead_List)),'Title'] = 'Mr'
        test.loc[(test['Surname'].apply(lambda x:x in Survived_List)),'Sex'] = 'female'
        test.loc[(test['Surname'].apply(lambda x:x in Survived_List)),'Age'] = 5
        test.loc[(test['Surname'].apply(lambda x:x in Survived_List)),'Title'] = 'Miss'

        # Feature conversion
        whole_data=whole_data[['Survived','Pclass','Sex','Age','Fare','Embarked','Title','Family_label','Deck','Ticket_Class']]
        whole_data=pd.get_dummies(whole_data)
        test=whole_data[whole_data['Survived'].isnull()].drop('Survived',axis=1)

        test.to_csv(f"/data/{source}_testdata.csv")
#"Figure saved to \"/data/number_of_words_{source}.png\""
    return "features was saved at ./data"

    #except IOError as e:
    #    return f"ERROR: {e} ({e.errno})"

if __name__ == "__main__":
    # Make sure that at least one argument is given, that is either 'write' or 'read'
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} write|read")
        exit(1)

    # If it checks out, call the appropriate function
    command = sys.argv[1]
    if command == "processing":
        print(yaml.dump({ "contents": processing(os.environ["SOURCE"]) }))
