# Vacation-finder-training

vacation-finder-training is the vacator which pull data from dClimate server periodically and train models

### 1. Usage of the Fetcher.py file
That script job will download temperature, snowfall, wind, rainfall and solar data and store locally.
This will be done every 2 hours.

Befre you run this script, you should get your dclimate token from [api.dclimate.net](https://api.dclimate.net) adn store it in your root repo in a hidden file called .token (just copy and paste)

```
pip3 install -r requirements.txt
python3 Fetcher_download.py
```

You should have this structure from your root folder

```
|vacation-finder-training
├── ...
├── dataset
│   ├── rainfall
│   ├── snowfall
│   ├── solar
│   ├── temp
│   └── wind

```

### 2. Automatic training of temperature forecast
This command will launch the API to get prediction or forecast value.

For Development and debugging:

```
python3 main.py
```

For final deployment:

```
uvicorn main:app --reload
```
