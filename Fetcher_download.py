
import tzlocal
from Fetcher import Dataset
#from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def process_download():
    d = Dataset()

    list_dataset = ["temp", "rainfall", "snowfall", "wind", "solar"]

    for dataset in list_dataset:
        print("dataset: ", dataset)
        res = d.download("Miami", dataset)
        d.save(res)
        

process_download()

scheduler = BlockingScheduler(timezone=str(tzlocal.get_localzone()))
scheduler.add_job(process_download, "interval", hours=1)
scheduler.start()