# Vacation-finder-training

vacation-finder-training is the vacator which pull data from dclimate server periodically and train models

### 1. Usage of the Fetcher.py file
That script job will download temperature, snowfall, wind, rainfall and solar data and store locally.
This will be done every 1 hour.

```
pip3 install -r requirements.txt
python3 Fetcher_download.py
```

You should have this structure from your root folder

```
├── dataset
│   ├── rainfall
│   ├── snowfall
│   ├── solar
│   ├── temp
│   └── wind

```

### 2. Automatic training of temperature forecast
This command will launch the API to get prediction or forecast value

```
uvicorn main:app --reload
```
