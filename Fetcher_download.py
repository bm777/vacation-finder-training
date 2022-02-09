
import tzlocal
from Fetcher import Dataset
#from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def process_download():
    d = Dataset()
    list_town = ["Miami", "New York", "Las Vega", "Chicago", "Seattle", "San Francisco", "Washington","New Orleans", "Palm Springs", "San Diego", "Charleston"]
    list_dataset = ["temp", "rainfall", "snowfall", "wind", "solar"]
    for town in list_town:
        for dataset in list_dataset:
            print(f"-dataset: {dataset} -town: {town}")
            res = d.download(town, dataset)
            d.save(res)


process_download()

scheduler = BlockingScheduler(timezone=str(tzlocal.get_localzone()))
scheduler.add_job(process_download, "interval", hours=1)
scheduler.start()
