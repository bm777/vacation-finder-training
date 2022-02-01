#!/usr/bin/env python
# coding: utf-8

# Import libraries



import requests as r
import pandas as pd
import numpy as np
import math
from sklearn.linear_model import LinearRegression
from joblib import dump, load


# Dataset class

class Dataset:
    def __init__(self):
        self.description = "This is a class which download dataset"
        
    def download(self, town, dataset_code):
        HEADER = {
            "Authorization" : self.get_token()
        }
        lat, lon = self.get_lat_lon("Miami")
        if isinstance(self.get_dataset_name(dataset_code), list):
            dataset_name0 = self.get_dataset_name(dataset_code)[0]
            dataset_name1 = self.get_dataset_name(dataset_code)[1]
            
            response0 = r.get(f'https://api.dclimate.net/apiv3/grid-history/{dataset_name0}/{lat}_{lon}', headers=HEADER)
            response1 = r.get(f'https://api.dclimate.net/apiv3/grid-history/{dataset_name1}/{lat}_{lon}', headers=HEADER)
            response = self.get_norme(response0.json(), response1.json())
            response['data'] = {k[:-6]:v for k,v in response['data'].items()}
            return response
        else:
            dataset_name = self.get_dataset_name(dataset_code)
            response = r.get(f'https://api.dclimate.net/apiv3/grid-history/{dataset_name}/{lat}_{lon}', headers=HEADER)
            response = response.json()
            response['data'] = {k[:-6]:v for k,v in response['data'].items()}
            return response
        
    def get_lat_lon(self, name):
        town = {
            "Miami": [25.762329613614614, -80.19114735100034],
            "New York": [40.64136425563865, -73.78201731266307],
            "Las Vegas": [36.169819817986365, -115.14034125787191]
        }
        return town[name] if town[name]!= None else None
    
    def get_dataset_name(self, name):
        dataset = {
            "wind": ["era5_land_wind_u-hourly", "era5_land_wind_v-hourly"],
            "temp": "rtma_temp-hourly"
        }
        return dataset[name] if dataset[name]!= None else None
    
    def get_norme(self, r0, r1): 
        ret = {'data': {}}
        for k,v in r0['data'].items():
            ret['data'][k] = f'{math.sqrt(float(v.split()[0])**2 + float(r1["data"][k].split()[0])**2)} {v.split()[1]}'
        return ret
        
    def get_token(self):
        """
        Get a THE TOKEN FROM local storage
        Args:
            None
        """
        with open(".token") as t:
            tok = t.readline()
        return tok.strip()



#dataset = Dataset()


#d = dataset.download("Miami", "wind")




# # Vacation class

class Vacation:
    
    def __init__(self, town="Miami", dataset_name="wind"):
        self.description = "vacation class for training"
        self.town = town
        self.dataset_name = ""
        
    def train(self, X, y):
        regressor = LinearRegression().fit(X, y)
        return regressor
    
    def save_model(self, model):
        dump(model, f'{self.town}-{self.dataset_name}.joblib')
        
    def load_model(self, filename):
        load(filename)
        
    def calculate_yearly_value(self, timeseries, metric="avg"):
        values = {}
        
        if metric == "min": 
            for k, v in timeseries.items():
                if int(k.split("-")[0]) in values:
                    if v is not None:
                        if values[int(k.split("-")[0])][0] > float(v.split()[0]):
                            values[int(k.split("-")[0])] = [float(v.split()[0])]
                else:
                    if v is not None:
                        values[int(k.split("-")[0])] = [float(v.split()[0])]
            return values
        
        if metric == "max": 
            for k, v in timeseries.items():
                if int(k.split("-")[0]) in values:
                    if v is not None:
                        if values[int(k.split("-")[0])][0] < float(v.split()[0]):
                            values[int(k.split("-")[0])] = [float(v.split()[0])]
                else:
                    if v is not None:
                        values[int(k.split("-")[0])] = [float(v.split()[0])]
            return values
        
        if metric == "max": 
            for k, v in timeseries.items():
                if int(k.split("-")[0]) in values:
                    if v is not None:
                        if values[int(k.split("-")[0])][0] < float(v.split()[0]):
                            values[int(k.split("-")[0])] = [float(v.split()[0])]
                else:
                    if v is not None:
                        values[int(k.split("-")[0])] = [float(v.split()[0])]
            return values
        
        # in case, metric = avg
        for k, v in timeseries.items():
            if v is not None:
                if int(k.split("-")[0]) in values:
                    values[int(k.split("-")[0])] += [float(v.split()[0])]
                else:
                    values[int(k.split("-")[0])] = [float(v.split()[0])]
        return {k:sum(v)/len(v) for k,v in values.items()}
        

    def dt_range(self, start, end):
        date_range = pd.date_range(start=start, end=end, freq="1H").to_pydatetime().tolist()
        return [f'{str(d).split()[0]}T{str(d).split()[1]}.000Z' for d in date_range][:-1]

    def dt_range_to_keys(self, datetime_range):
        keys = [d.split("T")[0] +' '+ d.split("T")[1].split(".")[0] for d in datetime_range]
        return keys

    def select_hours(self, datetime_range, start, end):
        return [d for d in datetime_range if start <= int(d.split('T')[1].split(":")[0]) < end]

    def get_timeseries(self, resp, year_start, year_end, day_start, day_end, hour_start, hour_end):
        data = resp['data']
        #generate timeseries
        ts = []
        for yr in range(year_start, year_end):
            start = f'{yr}-{day_start}'
            end = f'{yr}-{day_end}'
            ts += self.dt_range_to_keys(self.select_hours(self.dt_range(start, end), hour_start, hour_end))
        return {k:v for k,v in data.items() if k.split()[0]+" "+k.split()[1].split("-")[0] in ts}
        
        

"""
vacation = Vacation()

ts = vacation.get_timeseries(d, 2001, 2022, "09-01", "09-14", 0, 24)

years = vacation.calculate_yearly_value(ts,  metric="avg")

y = np.array(list(years.values()))
X = np.array(list(years.keys())).reshape(-1, 1)

model = vacation.train(X, y)

model.coef_, model.intercept_

input_date = [[2022]]

result = model.predict(input_date)
print(result)
vacation.save_model(model)
"""