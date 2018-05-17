import pandas as pd
import random
import numpy as np
import smtplib
import pandas as pd

def filterFrequency(names):
    week_no = int(names.columns[-1].split('week')[1])
    thisweek = []
    for index, row in names.iterrows():
        if week_no % int(row['frequency']) == 0:
            thisweek.append(True)
        else:
            thisweek.append(False)
    names['this_week'] = thisweek

    names = names[names['this_week']].drop(labels = 'this_week', axis = 1)

    return names

def runMatch(NamesDB):
    NamesPID = list(NamesDB.PID.values)
    pairs = []
    # If there are more than two people left
    while len(NamesPID) > 2:
        CurrentMatch = NamesPID[0]
        #previousMatches = [NamesDB.week1[0]]
        previousMatches = [col for col in NamesDB.columns if col[0:4] == 'week']
        previousMatchesL = list(NamesDB[previousMatches].iloc[0].values.astype(int))
        # Add yourself to the previous matches to stop you being matched with yourself
        previousMatchesL.append(CurrentMatch)
        AllParticipants = list(NamesPID)
        # Possible matches are elements NOT in BOTH lists
        possibleMatches = set(AllParticipants) ^ set(previousMatchesL)
        Name1 = NamesPID[0]
        rand2 = random.choice(list(possibleMatches))
        NamesPID.remove(Name1)
        NamesPID.remove(rand2)
        pair = Name1, rand2
        pairs.append(pair)
    else:
        pair = NamesPID[0], NamesPID[1]
        pairs.append(pair)

    # Convert to pandas DataFrame
    pairsnp = np.array(pairs)
    pairsDF = pd.DataFrame(pairsnp, columns = ('personA', 'personB'))
    
    # Make sure the matches are listed against both people, so copy and invert the columns
    pairsDoubled = pairsDF.copy()
    pairsDoubled = pairsDoubled.rename({'personA': 'personB', 'personB': 'personA'}, axis = 1)
    pairsLong = pd.concat([pairsDF, pairsDoubled]).reset_index(drop = True)
    AppendedDB = appendMatches(NamesDB, pairsLong)
    writeToCSV(NamesDB, AppendedDB)
    
    return pairsLong, AppendedDB

def appendMatches(NamesDB, pairsLong):
    AppendedDB = pd.merge(NamesDB, pairsLong, left_on='PID', right_on = 'personA')
    AppendedDB = AppendedDB.drop(['personA'], axis = 1)
    ColumnName = 'week' + str(StartWeek)
    AppendedDB = AppendedDB.rename({'personB': ColumnName}, axis = 1)
    
    return AppendedDB

def writeToCSV(NamesDB, AppendedDB):
    #ToWrite = pd.merge(NamesDB, AppendedDB, left_on='PID')
    with open('TestNames.csv', 'w') as f:
        AppendedDB.to_csv(f, index=False)
    
def buildEmail(fname, other_person_fname , other_person_lname, other_person_email):
    message = ('Hi ' + fname + ',\n' + 'For this week\'s StochastiCoffee catchup, you\'ve drawn ' +
               other_person_fname + ' ' + other_person_lname + '.\nContact ' + other_person_fname +
               ' at ' + other_person_email)
    return message

def sendEmail(names, matches): 
    gmail_user = 'kingofspam@gmail.com'  
    gmail_password = 'spamking'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_user, gmail_password)
    for _, row in matches.iterrows():
        email = names.loc[row['personA']]['email']
        fname = names.loc[row['personA'],'First Name']
        other_person_fname = names.loc[row['personB'],'First Name']
        other_person_lname = names.loc[row['personB'],'Last Name']
        other_person_email = names.loc[row['personB'],'email']
        message = buildEmail(fname, other_person_fname , other_person_lname, other_person_email)
        server.sendmail(gmail_user, email, message)

    server.quit()
    
StartWeek = 2
NamesDB = pd.read_csv('TestNames.csv')
#Namestomatch = filterFrequency(NamesDB)
matches, AppendedNamesDB = runMatch(NamesDB)