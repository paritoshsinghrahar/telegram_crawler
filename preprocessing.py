"""
Pre-Processing
1. The JSON file is processed to extract raw data and store it.
2. Raw data is converted to a data frame and processed to filter non-English characters.
3. Messages containing SHIB and DODGE are kept.
"""

# Libraries
from tqdm import tqdm
import json
import argparse
import pandas as pd

# Creates and returns data frame with attributes: text, date, time
def create_dataframe(text, date, time):
    df = pd.DataFrame(list(zip(text, date, time)), columns =['Text', 'Date','Time'])
    return df

# Saves data frame to CSV
def save_dataframe(df):
    df.to_csv('data/telegram_processed_data.csv',index=False)

# Pandas Functionality Extender: Filters English Character
def english_char_filter(x):
    return x.encode('ascii',errors='ignore').decode()

# Pandas Functionality Extender: Lowercase String
def lowercase_string(x):
    return x.lower()

# Filters English characters and keeps messages with substrings dodge or shib
# Returns filtered dataframe
def process_dataframe(df):
    df['Text'] = df['Text'].apply(english_char_filter)
    df['Text'] = df['Text'].apply(lowercase_string)
    df = df[df['Text'].str.contains("doge|shib")==True]
    df = df.reset_index(drop=True)
    return df
    
# Extract raw data from JSON file and returns list of attributes: text, date, time
def processing_main(data):
    string_list, date_list, time_list  = [],[],[]
    
    # Pre-processing text data
    for i in tqdm(data['messages']):
        if isinstance(i['text'], list):
            temp_str=''
            for j in i['text']:
                if not isinstance(j,str):
                    temp_str+=j['text']
                else:
                    temp_str+=j
            string_list.append(temp_str)

        else:
            string_list.append(i['text'])

    # Pre-processing Date data
    for i in tqdm(data['messages']):
        date,time = i['date'].split('T')
        date_list.append(date)
        time_list.append(time)

    return string_list, date_list, time_list

# Main Driver 
def main():
    
    # Input Filename: 'data/result.json'
    
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()
    
    file_data = open(args.input)
    json_data = json.load(file_data)
    text, date, time = processing_main(json_data)
    df = create_dataframe(text, date, time)
    df = process_dataframe(df)
    save_dataframe(df)
    

if __name__ == "__main__":
    main()