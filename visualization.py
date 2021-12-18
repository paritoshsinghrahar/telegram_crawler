'''
1. A simple script to generate visualizations from processed code.
2. Visualizations are generated in plotly.
3. For better visualizations sentiment range from -1 to +1 is extended to -1000 to +1000.'''

#Libraries
import argparse
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Secondary Plots Visualizations (Saves Histogram on Sentiment Value)
def plot_visu_sec(df):
    fig = px.histogram(df, x = "sentiment",color_discrete_sequence=['#ffff00'])
    fig.update_layout(
        title="Sentiment Histogram",
        xaxis_title="Sentiment",
        yaxis_title="Count",
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color='white'
        )
    )
    fig.write_image("images/plot_hist.png")
    
    df2 = df[df.sentiment != 0]
    fig = px.histogram(df2, x = "sentiment",color_discrete_sequence=['#ffff00'])
    fig.update_layout(
        title="Sentiment Histogram (- Neutal Values)",
        xaxis_title="Sentiment",
        yaxis_title="Count",
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color='white'
        )
    )
    fig.write_image("images/plot_hist_without_zero.png")

# Plots Visualizations (Saves number of messages per day and the average sentiment per day)
def plot_visu(df):
    fig = go.Figure(data=[
        go.Bar(x=df["Date"], y=df["Count"], marker_color = 'mediumspringgreen', name='No_of_Messages'),
        go.Scatter(x=df["Date"], y=df["Mean_Sentiment"]*1000,marker_color = 'yellow',name='Avg_Sentiment')
    ])

    fig.update_layout(
        title="Sentiment Analysis",
        xaxis_title="Day",
        xaxis=dict(
        title='Day',
        tickmode='linear'),
        yaxis_title="Value",
        legend_title="Legend",
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color='white'
        )
    )
    fig.write_image("images/plot.png")

# Data Processing for plots visualizations
def plot_data_process(df):
    
    sent_mean_df = df.groupby(df.Date).sentiment.mean().to_frame()
    sent_mean_df.reset_index(level=0, inplace=True)
    sent_mean_df.columns = ['Date', 'Mean_Sentiment']
    
    mess_count_df = df.groupby(df.Date).size().to_frame()
    mess_count_df.reset_index(level=0, inplace=True)
    mess_count_df.columns = ['Date', 'Count']
    
    df = pd.merge(sent_mean_df,mess_count_df,on='Date')
    return df

# Main Driver 
def main():
    
    # Input Filename: 'data/telegram_processed_data.csv'
    
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()
    
    df_org = pd.read_csv(args.input)
    df = plot_data_process(df_org)
    plot_visu(df)
    plot_visu_sec(df_org)
    
if __name__ == "__main__":
    main()
    
    