
import json
import pandas as pd
from datetime import date

def get_prediction(df_open, date_in_future, town):
    future = date_in_future                             # date for future prediction
    last = get_last_day_from_dataset(town)              # last day from temperature dataset
    print(last, future)

    f = int(future[:4]), int(future[5:7]), int(future[8:])
    l = int(last[:4]), int(last[5:7]), int(last[8:])

    days_in_future = date(f[0], f[1], f[2]) - date(l[0], l[1], l[2])
    days_in_future = days_in_future.days
    assert days_in_future >= 1 and days_in_future <= 30, "Date value should be within 1 and 30"

    df = df_open[df_open["town"] == town] # get only DataFrame for Miami
    df.reset_index(inplace=True)             # separate index merget with usable value
    df.drop(columns="index")                 # get drop index column which is containing unusable values
    days_in_future -= 1                      # because index in DataFrame starts from 0 instead of 1 (regular starting index of days)
    return df.get_value(days_in_future, 1, takeable=True)


def get_last_day_from_dataset(town):
    df = json.load(open(f"dataset/temp/{town}.json"))
    df = df["data"]
    return list(df.keys())[-1]
