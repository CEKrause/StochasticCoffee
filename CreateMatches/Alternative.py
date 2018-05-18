import pandas as pd
import random
import numpy as np
import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def filterFrequency(names):
    week_no = int(names.columns[-1].split('week')[1])
    thisweek = []
    for _, row in names.iterrows():
        if week_no % int(row['frequency']) == 0:
            thisweek.append(True)
        else:
            thisweek.append(False)
    names['this_week'] = thisweek

    return names[names['this_week']].drop(labels = 'this_week', axis = 1)

def runMatch(NamesDB):
### CLAIRE'S MATCHMAKING ALGORITHM ###
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
### END CLAIRE ###

### MIKE'S MATCHMAKING ALGORITHM ###
    # same as Claire's previousMatches variable - ie column names of all the previous weeks matches
    history = [col for col in NamesDB.columns if col[0:4] == 'week']
    # empty lists
    pairs = []
    matched_pids = []

    for index, row in NamesDB.iterrows():
        # if the PID has already been matched this week, don't do anything
        if row['PID'] in matched_pids:
            continue
        # ss means subset, need to copy because we are changing it and would otherwise generate warnings
        ss = NamesDB.copy()
        # cut ss down to the PIDs who don't have a match made yet
        ss = ss[~ss.isin({'PID':matched_pids})['PID']]
        # drop the PID in question from the ss also
        ss = ss.copy().drop(index, axis = 0)

        # create a column for the sum of the number of previous matches
        ss['past_freq'] = ((ss[history].values) == row['PID']).sum(axis=1)
        # drop all rows that don't have the new column == 0
        ss = ss.drop(ss[ss['past_freq'] != 0].index, axis = 0)

        # randomly chose one of the other remaining PIDs
        rand_no = random.choice(ss['PID'].values)
        # add the newly matched PIDs to the list, so they are ignored for the rest of this weeks matchmaking
        matched_pids.append(row['PID'])
        matched_pids.append(rand_no)
        # save the pairs for future use
        pairs.append((row['PID'],rand_no))
### END MIKE ###

### MIKE'S MATCHMAKING ALGORITHM - 3RD WHEEL VERSION###
    # same as Claire's previousMatches variable - ie column names of all the previous weeks matches
    history = [col for col in NamesDB.columns if col[0:4] == 'week']
    # empty lists
    pairs = []
    matched_pids = []
    met_everyone = []

    # randomly chose someone to be the third wheel if needed (ie odd number of participants)
    third_wheel = None
    if len(NamesDB) % 2 != 0:
        third_wheel = random.choice(NamesDB.index.values)
        NamesDB = NamesDB.drop(labels = third_wheel, axis = 0)
    for index, row in NamesDB.iterrows():
        # if the PID has already been matched this week, don't do anything
        if row['PID'] in matched_pids:
            continue
        # ss means subset, need to copy because we are changing it and would otherwise generate warnings
        ss = NamesDB.copy()
        # cut ss down to the PIDs who don't have a match made yet
        ss = ss[~ss.isin({'PID':matched_pids})['PID']]
        # drop the PID in question from the ss also
        ss = ss.copy().drop(index, axis = 0)

        # create a column for the sum of the number of previous matches
        ss['past_freq'] = ((ss[history].values) == row['PID']).sum(axis=1)
        # drop all rows that don't have the new column == 0
        ss = ss.drop(ss[ss['past_freq'] != 0].index, axis = 0)
        
        # to add bias towards people in different branches
        # find the subset of the subset that share the same branch as the person in question
        same_branch = ss[ss['branch'] == row['branch']]
        # if the ss branch is longer (ie all the people the person hasn't met are NOT in their branch), cull the list
        # otherwise don't, which is implict (sorry Zen of Python)
        if len(ss) > len(same_branch):
            ss = ss[ss['branch'] != row['branch']]

        if len(ss) == 0:
            matched_pids.append(row['PID'])
            met_everyone.append(row['PID'])
            continue
        # randomly chose one of the other remaining PIDs
        rand_no = random.choice(ss['PID'].values)
        # add the newly matched PIDs to the list, so they are ignored for the rest of this weeks matchmaking
        matched_pids.append(row['PID'])
        matched_pids.append(rand_no)
        # save the pairs for future use
        pairs.append((row['PID'],rand_no, np.nan))
    
    if len(met_everyone) != 0:
        while len(met_everyone) > 0:
            if len(met_everyone) == 1:
                # randomly chose one of the existing pairs
                rand_pair = random.choice(range(len(pairs)))
                # add the person to the random pair
                pairs[rand_pair][2] == met_everyone[0]
                # remove the (only) entry from the list
                met_everyone.pop()
            if len(met_everyone) > 1:
                # randomly assign the person someone they've already met
                match = random.choice(1, range(len(met_everyone)))
                # add the new match to the table
                pairs.append(met_everyone[0], met_everyone[match], np.nan)
                # remove the newly matched people from the met_everyone list
                met_everyone.remove(met_everyone[0])
                met_everyone.remove(met_everyone[match])
                
    # assign the third_wheel a pair
    # randomly chose a pair, if the pair is acutally a 3 due to met_everyone people
    # then choose a different pair, else, use that pair.
    if third_wheel != None:
        while True:
            pair = random.choice(pairs)
            if np.isnan(pair[2]):
                pair[2] = third_wheel
                break
        
### END MIKE 3RD WHEEL VERSION ###


### The code below is common to both match making methods ###
    # Convert to pandas DataFrame
    pairsnp = np.array(pairs)
    pairsDF = pd.DataFrame(pairsnp, columns = ('personA', 'personB'))
    
    # Make sure the matches are listed against both people, so copy and invert the columns
    pairsDoubled = pairsDF.copy()
    pairsDoubled = pairsDoubled.rename(index = str, columns = {'personA': 'personB', 'personB': 'personA'}) #{'personA': 'personB', 'personB': 'personA'}, axis = 1)
    pairsLong = pd.concat([pairsDF, pairsDoubled]).reset_index(drop = True)
    AppendedDB = appendMatches(NamesDB, pairsLong)
    writeToCSV(NamesDB, AppendedDB)
    
    return pairsLong, AppendedDB

def appendMatches(NamesDB, pairsLong):
    AppendedDB = pd.merge(NamesDB, pairsLong, left_on='PID', right_on = 'personA')
    AppendedDB = AppendedDB.drop(['personA'], axis = 1)
    LastWeek = int(NamesDB.columns[-1].split('week')[1])
    ColumnName = 'week' + str(LastWeek + 1)
    AppendedDB = AppendedDB.rename(index = str, columns ={'personB': ColumnName}) #{'personB': ColumnName}, axis = 1)
    
    return AppendedDB

def writeToCSV(NamesDB, AppendedDB):
    #ToWrite = pd.merge(NamesDB, AppendedDB, left_on='PID')
    with open('TestNames.csv', 'w') as f:
        AppendedDB.to_csv(f, index=False)
    
def buildEmail(fname, email, other_person_fname , other_person_lname, other_person_email, gmail_user):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Your StochastiCoffee match for next week is...'
    msg['From'] = gmail_user
    msg['To'] = email
    plain_text = """Hi %s,
For this week's StochastiCoffee catchup, you've drawn %s %s.
Contact %s at %s

Have a great catchup!
Cheers,
- The StochastiCoffee Crew
    """ %(fname, other_person_fname, other_person_lname, other_person_fname, other_person_email)
    html = """\
<html>
  <head></head>
  <body>
    <p>Hi %s,<br>
       For this week's StochastiCoffee catchup, you've drawn %s %s.<br>
       Contact %s at <a href="mailto:%s">%s</a>
    <p>
       Have a great catchup!<br>
       Cheers,<br>
       - The StochastiCoffee Crew
    </p>
  </body>
</html>
""" %(fname, other_person_fname, other_person_lname, other_person_fname, other_person_email, other_person_email)
    
    part1 = MIMEText(plain_text, 'text')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    return msg.as_string()

def sendEmail(names, matches): 
    gmail_user = 'kingofspam@gmail.com'  
    gmail_password = 'spamking'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_user, gmail_password)
    for _, row in matches.iterrows():
        email = names.loc[names[names['PID'] == row['personA']].index, 'email']
        fname = names.loc[names[names['PID'] == row['personA']].index, 'First Name']
        other_person_fname = names.loc[names[names['PID'] == row['personB']].index, 'First Name']
        other_person_lname = names.loc[names[names['PID'] == row['personB']].index, 'Last Name']
        other_person_email = names.loc[names[names['PID'] == row['personB']].index, 'email']
        message = buildEmail(fname, email, other_person_fname , other_person_lname, other_person_email, gmail_user)
#         server.sendmail(gmail_user, email, message)
        print(fname, email, other_person_fname , other_person_lname, other_person_email, message)

    server.quit()
    
    
NamesDB = pd.read_csv('TestNames.csv')
NamesToMatch = filterFrequency(NamesDB)
matches, names = runMatch(NamesToMatch)
# note, for testing purposes, the send email function currently just prints everything to the screen
# also, I'm getting some weird error from deep inside the python email libraries, so needs some more debugging
sendEmail(names, matches)
