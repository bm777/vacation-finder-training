import os
import json
import tzlocal
import numpy as np
import pandas as pd
from Fetcher import Dataset
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing

# global variable
list_town = ["Miami", "New York", "Las Vega", "Chicago", "Seattle", "San Francisco", "Washington","New Orleans", "Palm Springs", "San Diego", "Charleston"]
list_dataset = ["temp", "rainfall", "snowfall", "wind", "solar"]

def process_download():
    d = Dataset()
    print("---------------------------------------------------------------------")
    for town in list_town:
        for dataset in list_dataset[:1]:
            print(f"-dataset: {dataset} -town: {town}")
            res = d.download(town, dataset)     # At each download, it will overwrite value of the constructor with  new value of town and dataset_code
            d.save(res)


def training(days=30):
    d = Dataset()
    final_df = []
    for dataset in list_dataset[:1]:
        for town in list_town:
            print(f"dataset/{dataset}/{town}.json")
            if os.path.exists(f"dataset/{dataset}/{town}.json"):
                print(f"{dataset} - {town}")
                res = json.load(open(f"dataset/{dataset}/{town}.json"))
                data = res["data"]

                index = pd.to_datetime(list(data.keys()))
                values = [float(s) if s else None for s in data.values()]

                series = pd.Series(values, index=index)
                df = series.to_frame(name='Value')

                df = df[~df.index.astype(str).str.contains('02-29')]

                #algorithm
                print("Training...")
                hw_model = ExponentialSmoothing(df["Value"],
                          trend    ="add",
                          seasonal = "add",
                          seasonal_periods=365,
                          damped=False
                          ).fit(use_boxcox="log") # damped=False


                hw_fitted = hw_model.fittedvalues
                hw_resid = hw_model.resid
                days_in_future = 30
                # Adding the mean of the residuals to correct the bias.
                py_hw = hw_model.forecast(days_in_future) + np.mean(hw_resid)
                print(py_hw)

                # to frame
                df = py_hw.to_frame()

                # get lat and long
                lat, long = d.get_lat_lon(town)

                df["lat"] = str(lat)
                df["long"] = str(long)
                df["town"] = str(town)

                final_df.append(df)
                df = None

    to_save = pd.concat(final_df)
    to_save.to_pickle("temp_model.pkl")






"""
def listener():
    if event.exception:
        print("The job crashed :(")
    else:
        print("The job worked :)")
        print("The Training can start")
"""


process_download()

scheduler = BlockingScheduler(timezone=str(tzlocal.get_localzone()))
scheduler.add_job(process_download, "interval", hours=2)      # minutes=2, hours=2, seconds=5
#scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
scheduler.start()
