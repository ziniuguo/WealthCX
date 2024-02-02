import os
import uuid


from fastapi import FastAPI
from fastapi.responses import FileResponse

import automation
from LLM_integration import split_summary
import asset_mp
import asset_mp_refined
import event_mp
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()
scheduler = BackgroundScheduler()

class FileResponseDeleteAfter(FileResponse):
    def __init__(self, path: str, *args, **kwargs):
        super().__init__(path, *args, **kwargs)
        self.file_path = path

    async def __call__(self, scope, receive, send):
        await super().__call__(scope, receive, send)
        if os.path.exists(self.file_path):
            os.remove(self.file_path)


def on_startup():
    item_id = "JPM"  # 你可以指定要自动执行的参数
    asset_mp.asset_mp()
    event_mp.event_mp()
    asset_mp_refined.asset_mp_refined()

# 使用scheduler装饰器来设置定时任务，每天晚上3点执行on_startup函数
@scheduler.scheduled_job("cron", hour=3)
def scheduled_task():
    on_startup()

@app.on_event("startup")
async def startup_event():
    # on_startup()
    scheduler.start()
    pass

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/query/{item_id}")
def read_item(item_id: str):
    i = str(uuid.uuid1())
    automation.automate(uuid=i, ric_value=item_id)
    file_path = "./Output/"+ i + "-output.csv"
    return FileResponseDeleteAfter(path=file_path,
                                   filename="result.csv",
                                   media_type='text/csv')

@app.get("/split/{item_id}")
def split_sum(item_id:str):
    splited = split_summary.split_summary(item_id).split('\n-')
    return splited




