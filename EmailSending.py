import smtplib
import pandas as pd

def buildEmail(fname, other_person_fname , other_person_lname, other_person_email):
    message = ('Hi ' + fname + ',\n' + 'For this week\'s StochastiCoffee catchup, you\'ve drawn ' +
               other_person_fname + ' ' + other_person_lname + '.\nContact ' + other_person_fname +
               ' at ' + other_person_email)
    return message

matches = pd.DataFrame({'personA':[0,1,2,3], 'personB':[2,3,0,1]})
names = pd.read_csv('TestNames.csv')

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