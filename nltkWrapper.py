## this is a wrapper class for package nltk
import nltk
import matplotlib
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class nltkWrapperClass:
    ##initiate class d(object):
    def __init__(self,out_dir):                     ## private method
        nltk.download('stopwords')
        nltk.download('vader_lexicon')
        self.__out_dir = out_dir                    ## private attribute
        self.sid = SentimentIntensityAnalyzer()     ## public attribute

    def __repr__(self):
        return repr(f'The output direcotry of this class is {self.__out_dir}')

    ## Public method to count word frequency
    def wordFreqCount(self,token_list):
        freq = nltk.FreqDist(token_list)
        return freq

    ## Public method to print out word frequency
    def wordFreqPrint(self,freq):
        for key,val in freq.items():
            print(f'key is: {key}, value is : {val}')

    ## Public method to plot out word frequency
    def wordFreqPlot(self,freq):
        freq.plot(20, cumulative=False)
        matplotlib.pyplot.show()

    ## Public method to clean up english stop words
    def stopwordClean(self,token_list):
        clean_token = []
        for token in token_list:
            if token not in stopwords.words('english'):
                clean_token.append(token)
        return clean_token

    ## Public method for giving sentiment score for tweet list and return dictionary
    ## that use tweet id as key and another dictionary that contains the text of tweet
    ## and it's sentiment score as value. Also there is a verbose flag
    def sentiScore(self,tweet_list,Verbose):
        sentiment_score_list = []
        Tweet_dict = {}
        for tweet in tweet_list:
            individual_tweet_dict = {}
            individual_tweet_dict['Text'] = tweet.text
            #Calculating sentiment scores
            individual_tweet_dict['Sentiment_score'] = self.sid.polarity_scores(tweet.text)
            Tweet_dict[tweet.id] = individual_tweet_dict
            if Verbose:
                print(f'Tweet is : {tweet.text}\nSentiment score is :{self.sid.polarity_scores(tweet.text)}\n\n')
        return Tweet_dict

    ## Public method to filter positive tweets
    def posTweets(self,Tweet_dict,Verbose):
        Pos_Tweet_dict = {}
        for tweet in Tweet_dict:
            if Tweet_dict[tweet]['Sentiment_score']['compound'] > 0.05:
                Pos_Tweet_dict[tweet] = Tweet_dict[tweet]
                if Verbose:
                    print(f"Positive tweet is : {Tweet_dict[tweet]['Text']}\nSentiment score is :{Tweet_dict[tweet]['Sentiment_score']}\n\n")
        return Pos_Tweet_dict

    ## Public method to filter negative tweets
    def negTweets(self,Tweet_dict,Verbose):
        Neg_Tweet_dict = {}
        for tweet in Tweet_dict:
            if Tweet_dict[tweet]['Sentiment_score']['compound'] < -0.05:
                Neg_Tweet_dict[tweet] = Tweet_dict[tweet]
                if Verbose:
                    print(f"Negative tweet is : {Tweet_dict[tweet]['Text']}\nSentiment score is :{Tweet_dict[tweet]['Sentiment_score']}\n\n")
        return Neg_Tweet_dict

    ## Public method to save pos and neg tweet results
    def CataResultSave(self,Pos_Tweet_dict,Neg_Tweet_dict):
        pos_result=open(self.__out_dir+"Positive_Tweets_Results.txt",'w')
        for tweet in Pos_Tweet_dict:
            pos_result.write(f"Positive tweet is : {Pos_Tweet_dict[tweet]['Text']}\nSentiment score is :{Pos_Tweet_dict[tweet]['Sentiment_score']}\n\n")
        pos_result.close()

        neg_result=open(self.__out_dir+"Negative_Tweets_Results.txt",'w')
        for tweet in Neg_Tweet_dict:
            neg_result.write(f"Negative tweet is : {Neg_Tweet_dict[tweet]['Text']}\nSentiment score is :{Neg_Tweet_dict[tweet]['Sentiment_score']}\n\n")
        neg_result.close()
