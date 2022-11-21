# Importing required modules
import tweepy
import os
import time
import urllib.request
import json
from dotenv import load_dotenv
load_dotenv()

# Setting environment variables
BEARER_TOKEN = os.environ['BEARERTOKEN']
API_KEY = os.environ['APIKEY']
API_KEY_SECRET = os.environ['APISECRETKEY']
ACCESS_TOKEN = os.environ['ACCESSTOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESSTOKENSECRET']

# Initiating the client
client = tweepy.Client(consumer_key=API_KEY,
                       consumer_secret=API_KEY_SECRET,
                       access_token=ACCESS_TOKEN,
                       access_token_secret=ACCESS_TOKEN_SECRET)


# procedure to post tweets for specific location
# Takes district and chettra number as input

def postTweetByLocation(district,chettra):
#for debug purposes
  print ("Inside the function")

# Opening the file
  data = urllib.request.urlopen('https://result.election.gov.np/JSONFiles/ElectionResultCentral2079.txt')

  Location = ""
  Candidates=[]

# Looping through the data 
  for line in data:
    singleCandidate = []
    actualData = json.loads(line.decode('utf-8'))

    # looping through actualData
    for i in range(len(actualData)):

        # Checking if the district name and chettra number matches
      if (actualData[i]['DistrictName'] == district and int(actualData[i]['SCConstID'])==chettra):
        Symbol = actualData[i]['SymbolName']
        CandidateName = actualData[i]['CandidateName']
        VoteReceived = actualData[i]['TotalVoteReceived']
        singleCandidate = [Symbol, CandidateName, VoteReceived]

        # adding to candidates list if the vote obtained is not zero
        if (singleCandidate[2]!=0):
          Candidates.append(singleCandidate)

  # Sorting the Candidates list based on votes received by candidate
  Candidates.sort(reverse = True, key = lambda i: i[2])

#   formatting the message to be posted
  Location = district +" - " + str(chettra)
  if (len(Candidates)!=0):
    message = "Live Election Update " + "\n" + "\n" + Location + "\n" + "\n"
    
  
    for j in range(4):
        message = message + str(
          j + 1) + ". " + Candidates[j][1] + "  (" +Candidates[j][0]+")  " + " - " + str(Candidates[j][2]) + "\n"
  
    message = message + "\n" + "Source: https://result.election.gov.np/" +"\n"+"\n"+"#NepalElection2022"

    # printing the message for debug purpose
    print(message)

    #posting a tweet and a use of exception handling
    try:
      response = client.create_tweet(text=message)
      time.sleep(120)
      print(response)
    except:
      print("Some Error encountered")
  else:
    print("Counting hasn't Started")



# List that contains list of locations whose data is being posted
Locations = [["झापा", 5], ["डडेलधुरा", 1], ["गोरखा", 2], ["सप्तरी", 2],["इलाम", 1], ["काठमाडौं", 5], ["काठमाडौं", 4],["ताप्लेजुंग", 1],["चितवन", 2], ["झापा", 3], ["झापा", 1],["भक्तपुर",2],["भक्तपुर",1],["कास्की",2],["काठमाडौं", 1],["काठमाडौं", 7],["काठमाडौं", 9],["काठमाडौं", 8],['ललितपुर',3]]


# procedure to post top 5 parties condition
def postTweetByParty():
#for debug purposes
  print ("Inside the function")

# Opening the file
  data = urllib.request.urlopen('https://result.election.gov.np/JSONFiles/Election2079/Common/HoRPartyTop5.txt')
  PoliticalParty=[]

# Looping through the data 
  for line in data:
    singleParty = []
    actualData = json.loads(line.decode('utf-8'))

    # looping through actualData
    for i in range(len(actualData)):
      PoliticalPartyName = actualData[i]['PoliticalPartyName']
      TotalWins = actualData[i]['TotWin']
      TotalLeads = actualData[i]['TotLead']
      TotalWinLead = actualData[i]['TotWinLead']
      singleParty = [PoliticalPartyName, TotalWins, TotalLeads, TotalWinLead]
      PoliticalParty.append(singleParty)

    #formatting the content of the tweet to be posted
  content = "Live update(Wins+Leads)" +"\n" +"\n"
  for j in range(len(PoliticalParty)):
    content = content + str(j+1) +". "+ PoliticalParty[j][0]+" - " + str(PoliticalParty[j][3]) +"\n"

  content = content + "\n" + "#NepalElections2022"

  # printing the content for debug purpose
  print(content)

  #posting a tweet and a use of exception handling
  try:
      response = client.create_tweet(text=content)
      time.sleep(120)
      print(response)
      
  except:
      print("Some Error encountered")



# Procedures call 
while (True):
  postTweetByParty()
  for k in range(len(Locations)):
    postTweetByLocation(Locations[k][0], Locations[k][1])
  time.sleep(600)
