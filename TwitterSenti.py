#API key: ****
#API secret key: ****
#Bearer token: ****
#Access token:****
#Access token secret:****





######PART1#########
##Connect twitter API and collect Text Data###
#Apply file operations

#help("modules")
import tweepy

from tweepy import OAuthHandler
from tweepy import API


from tweepy.streaming import StreamListener
import time

class SListener(StreamListener): 
    def __init__(self, api = None):        
        self.output  = open('tweets_%s.json' % 
                            time.strftime('%Y%m%d-%H%M%S'), 'w')        
        self.api = api or API()



# Setting up tweepy API authentication credentials
auth = tweepy.OAuthHandler("****", 
    "****") #"CONSUMER_KEY", "CONSUMER_SECRET"
auth.set_access_token("****", 
    "****") #"ACCESS_TOKEN", "ACCESS_TOKEN_SECRET"

api = tweepy.API(auth)

#Testing the credentials
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
    

    

#######PART2########
####Processing Twitter Text#####

##Tokenization
##Apply list mutability, iterations and dictionaries
## Search keyword
token_list = []
tweet_list = []
keyword='vaccine covid'
for tweet in api.search(q=keyword,
                                    lang="en",
                                    count=100,
                                    result_type="top",
                                    include_entities=True
                                    ):
    # print(f'Searched result is : {tweet}')
    ## append tweet to tweet_list 
    tweet_list.append(tweet)
    for each_token in tweet.text.split():
        token_list.append(each_token.lower())
    
print(f'tweet_list is: {tweet_list}')
print(f'tweet list length is: {len(tweet_list)}\n\n')



   

########PART3########
#####Analysis########

from nltkWrapper import nltkWrapperClass
## set up output directory
out_dir = "./"
nltkWrapper = nltkWrapperClass(out_dir)

## class repr method 
print(repr(nltkWrapper))

##Clean up English stop words first 
clean_token = nltkWrapper.stopwordClean(token_list)

##Count word frequency using NLTK
freq = nltkWrapper.wordFreqCount(clean_token)

##Print out word frequency 
nltkWrapper.wordFreqPrint(freq)

##Plot out word frequency 
nltkWrapper.wordFreqPlot(freq)

##Sentiment Analysis
Verbose = True
Tweet_dict = nltkWrapper.sentiScore(tweet_list,Verbose)


#Tweet catagorize 
#Filter out positive tweet, if compoint score > 0.05 consider positive 
Pos_Tweet_dict = nltkWrapper.posTweets(Tweet_dict,Verbose)
#Filter out negative tweet, if compoint score < -0.05 consider positive 
Neg_Tweet_dict = nltkWrapper.negTweets(Tweet_dict,Verbose)

## Save categorized tweet results 
nltkWrapper.CataResultSave(Pos_Tweet_dict,Neg_Tweet_dict)

















