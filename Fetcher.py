#!/usr/bin/env python
# coding: utf-8

# Import libraries

import os
import json
import math
import numpy as np
import pandas as pd
import requests as r



class Dataset:
    def __init__(self):
        self.description = "This is a class which download dataset"
        self.town = None
        self.dataset = None

    def download(self, town, dataset_code):
        self.town = town
        self.dataset = dataset_code
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
            if dataset_code != "temp":
                response['data'] = {k[:-6]:v for k,v in response['data'].items()}
            else:
                response['data'] = {k:v for k,v in response['data'].items()}
            return response

    def save(self, content):
        _path = f"dataset/{self.dataset}/{self.town}.json"

        if not os.path.exists("dataset/"):
            os.mkdir("dataset")
            if not os.path.exists(f"dataset/{self.dataset}"):
                os.mkdir(f"dataset/{self.dataset}")
                if os.path.exists(_path):
                    os.remove(_path)
        else:
            if not os.path.exists(f"dataset/{self.dataset}"):
                os.mkdir(f"dataset/{self.dataset}")
                if os.path.exists(_path):
                    os.remove(_path)

        if self.dataset in ["temp", "wind"]:
            daily = self.get_daily_values(content["data"], metric="avg")
        elif self.dataset in ["rainfall", "snowfall", "solar"]:
            daily = self.get_daily_values(content["data"], metric="sum")

        print(_path)
        with open(_path, 'w') as json_file:
            json.dump(daily, json_file)
        print(f"{_path} Saved.")

    def get_lat_lon(self, name):
        # this json data could be replaced later by a jsonf file data
        town = {
            "Miami": [25.762329613614614, -80.19114735100034],
            "New York": [40.64136425563865, -73.78201731266307],
            "Las Vegas": [36.169819817986365, -115.14034125787191],
            "Chicago": [41.86510407471184, -87.69969903002156],
            "Seattle": [47.60461047246771, -122.33245824227117],
            "San Francisco": [37.77740029947461, -122.40115963920373],
            "Washington": [38.90682577195005, -77.04238707504109],
            "New Orleans": [30.01005090305327, -90.06336574477528],
            "Palm Springs": [33.826330865812224, -116.54404246241852],
            "San Diego": [32.723783379579274, -117.16668979753065],
            "Charleston": [32.7725713187095, -79.91668374248282]
        }
        return town[name] if town[name]!= None else None

    def get_dataset_name(self, name):
        
        dataset = {
            "wind": ["era5_land_wind_u-hourly", "era5_land_wind_v-hourly"],
            "temp": "prismc-tmax-daily",                                     #"rtma_temp-hourly",
            "rainfall": "era5_land_precip-hourly",
            "snowfall": "era5_land_snowfall-hourly",
            "solar": "era5_land_surface_solar_radiation_downwards-hourly"
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

    def get_daily_values(self, timeseries, metric="avg"):
        values = {}

        if metric == "sum":
            for k, v in timeseries.items():
                if v is not None:
                    if k[:10] in values:
                        values[k[:10]] += [float(v.split()[0])]
                    else:
                        values[k[:10]] = [float(v.split()[0])]
            return {"data": {k:sum(v) for k,v in values.items()} }

        # in case, metric = avg
        if metric == "avg":
            for k, v in timeseries.items():
                if v is not None:
                    if k[:10] in values:
                        values[k[:10]] += [float(v.split()[0])]
                    else:
                        values[k[:10]] = [float(v.split()[0])]
            return {"data": {k:sum(v)/len(v) for k,v in values.items()} }

        return {"data": values}




#dataset = Dataset()

#d = dataset.download("Miami", "wind")
