import re
import pandas as pd
import json


def preprocess(data):
    # pattern = '\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}'  #for 24 Hours
    df = json.loads(data)
    df_messages = pd.json_normalize(df['messages'])
    df = df_messages[['date', 'from', 'text']]
    df['date'] = df["date"].str.replace("T", " ")
    df["date"] = pd.to_datetime(df["date"])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df.rename(columns={'from': 'user'}, inplace=True)
    df.rename(columns={'text': 'message'}, inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df['date_column'] = df['date'].dt.date
    df['time_column'] = df['date'].dt.time
    df['day_name'] = df['date'].dt.day_name()
    df = df.drop(columns=['date'])
    df.rename(columns={'date_column': 'date'}, inplace=True)
    df.rename(columns={'time_column': 'time'}, inplace=True)

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df