import pandas as pd
import random
import numpy as np
import smtplib
import pandas as pd

def pop_random(lst):
    idx = random.randrange(0, len(lst))
    return lst.pop(idx)

def runMatch(csvfile):
    NamesDB = pd.read_csv(csvfile)
    NamesPID = list(NamesDB.PID.values)
    pairs = []
    while len(NamesPID) > 0:
        rand1 = pop_random(NamesPID)
        rand2 = pop_random(NamesPID)
        pair = rand1, rand2
        pairs.append(pair)

    pairsnp = np.array(pairs)
    pairsDF = pd.DataFrame(pairsnp, columns = ('personA', 'personB'))
    
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

names, matches = runMatch('TestNames.csv')
sendEmail(names, matches)