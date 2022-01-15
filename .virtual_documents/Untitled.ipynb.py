import json, requests, pandas as pd
from typing import Tuple


def get_token() -> str:
    """
    Get a THE TOKEN FROM local storage
    Args:
        None
    """
    with open(".token") as t:
        tok = t.readline()
    return tok.strip()


def http_query(dataset, lat, long) -> bool:
    """
    Get a response from url get
    Args:
        dataset (str): the dataset name
        lat (str): the latitude for the location
        long (str): the longitude for the location
    """
    HEADER = {
        "Authorization" : get_token()
    }
    query = ["https://api.dclimate.net/apiv3/grid-history/"
                + dataset + "/"
                + lat + "_" + long +"?"
                + "also_return_metadata=false&"
                + "use_imperial_units=true&"
                + "also_return_snapped_coordinates=true&"
                + "convert_to_local_time=true"]

    r = requests.get(query[0], headers=HEADER)
    #r.raise_for_status()
    print(r.json())
    row_data = r.json()["data"]

    raws = []

    for data in row_data:
        raws.append({"data": data, "value": row_data[data].split(" ")[0]})
    df = pd.DataFrame(raws)

    df.to_csv("json/" + dataset + "-" + lat + "_" + long + ".csv", index=False)

    return True


def town_to_lat_long(town) -> Tuple[str, str]:
    towns_map = [
        ["Miami", "25.762329613614614", "-80.19114735100034"],
        ["New York", "40.64136425563865", "-73.78201731266307"],
        ["Chicago", "41.86510407471184", "-87.69969903002156"],
        ["Las Vegas", "36.169819817986365", "-115.14034125787191"],
        ["Seattle", "47.60461047246771", "-122.33245824227117"],
        ["San Francisco", "37.77740029947461", "-122.40115963920373"],
        ["Washington", "38.90682577195005", "-77.04238707504109"],
        ["New Orleans", "30.01005090305327", "-90.06336574477528"],
        ["Palm Springs", "33.826330865812224", "-116.54404246241852"],
        ["San Diego", "32.723783379579274, -117.16668979753065"],
        ["Charleston", "32.7725713187095", "-79.91668374248282"]
    ]
    for single_town in towns_map:
        if single_town[0] == town:
            return single_town[1], single_town[-1]

    return "None", "None"


place = town_to_lat_long("Miami")


# get air quality


saved_u = http_query("era5_land_wind_u-hourly", place[0], place[1])


saved_v = http_query("era5_land_wind_v-hourly", place[0], place[1])




