'''
1. Sentiment Analysis is done using the nltk library.
2. The built-in, pretrained sentiment analyzer called VADER (Valence Aware Dictionary and sEntiment Reasoner) was utilized for sentiment analysis. VADER is tuned for social media linguistics.
3. Since the goal of the project is to perform first analysis on the dataset, nltk(VADER) is chosen for quick and preliminary exploratory analysis.
'''

#Libraries
from nltk.sentiment import SentimentIntensityAnalyzer
import operator
import argparse
import pandas as pd

## Safeguard against Fail
import nltk
nltk.download('vader_lexicon')
##

# Saves data frame to CSV
def save_dataframe(df):
    df.to_csv('data/telegram_visualization_data.csv',index=False)

# Sentiment Analysis Driiver; returns dataframe with sentiment values
def sentiment_analysis_func(df):
    sia = SentimentIntensityAnalyzer()
    df['sentiment'] = df["Text"].apply(lambda x: sia.polarity_scores(x)["compound"])
    return df

# Main Driver 
def main():
    
    # Input Filename: 'data/telegram_processed_data.csv'
    
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()
    
    df = pd.read_csv(args.input)
    df = sentiment_analysis_func(df)
    save_dataframe(df)
    
if __name__ == "__main__":
    main()