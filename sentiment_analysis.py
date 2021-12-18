from nltk.sentiment import SentimentIntensityAnalyzer
import operator
import argparse
import pandas as pd

## Safeguard against Fail
import nltk
nltk.download('vader_lexicon')
##

def save_dataframe(df):
    df.to_csv('data/telegram_visualization_data.csv',index=False)

def sentiment_analysis_func(df):
    sia = SentimentIntensityAnalyzer()
    df['sentiment'] = df["Text"].apply(lambda x: sia.polarity_scores(x)["compound"])
    return df

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