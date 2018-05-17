import pandas as pd
import random
import numpy as np
import smtplib
import pandas as pd

def runMatch(NamesDB):
    NamesPID = list(NamesDB.PID.values)
    pairs = []
    # If there are more than two people left
    while len(NamesPID) > 2:
        CurrentMatch = NamesDB.PID[0]
        previousMatches = [NamesDB.matches[0]]
        # Add yourself to the previous matches to stop you being matched with yourself
        previousMatches.append(CurrentMatch)
        AllParticipants = list(NamesDB.PID)
        # Possible matches are elements NOT in BOTH lists
        possibleMatches = set(AllParticipants) ^ set(previousMatches)
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
    
    return NamesDB, pairsLong

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