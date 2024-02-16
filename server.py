import os
import uuid
import datetime

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse

import automation
from LLM_integration import split_summary
import asset_mp
import asset_mp_refined
import event_mp
from apscheduler.schedulers.background import BackgroundScheduler
import json

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


@app.get("/query/current-price/{item_id}")
async def read_current_price(item_id: str):
    # 生成唯一的文件名
    unique_id = str(uuid.uuid1())
    file_path = f"./Output/{unique_id}-output.csv"

    # 假设automation函数接受一个参数来指定输出文件的路径
    try:
        # 调用automation函数生成CSV
        automation.automate(uuid=unique_id, ric_value=item_id)

        # 确认文件存在
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not generated.")

        # 读取CSV文件并获取TRDPRC_1的值
        df = pd.read_csv(file_path)
        if "TRDPRC_1" not in df.columns:
            raise HTTPException(status_code=404, detail="TRDPRC_1 not found in file.")

        trdprc_1_value = df["TRDPRC_1"].iloc[0]  # 假设我们只关心第一行的数据
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 删除文件
        if os.path.exists(file_path):
            os.remove(file_path)

    # 返回TRDPRC_1的值
    return JSONResponse(content={"TRDPRC_1": trdprc_1_value})

@app.get("/query/target-price/{item_id}")
async def read_current_price(item_id: str):
    # 生成唯一的文件名
    unique_id = str(uuid.uuid1())
    file_path = f"./Output/{unique_id}-output.csv"

    # 假设automation函数接受一个参数来指定输出文件的路径
    try:
        # 调用automation函数生成CSV
        automation.automate(uuid=unique_id, ric_value=item_id)

        # 确认文件存在
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not generated.")

        # 读取CSV文件并获取TRDPRC_1的值
        df = pd.read_csv(file_path)
        if "BID" not in df.columns:
            raise HTTPException(status_code=404, detail="BID not found in file.")

        bid_value = df["BID"].iloc[0]  # 假设我们只关心第一行的数据
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 删除文件
        if os.path.exists(file_path):
            os.remove(file_path)

    # 返回TRDPRC_1的值
    return JSONResponse(content={"BID": bid_value})


def format_timestamp(ts):
    # 将字符串转换为datetime对象
    date_obj = datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")

    # 获取日并确定正确的后缀
    day = date_obj.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    # 使用strftime格式化月份和年份，手动处理日和后缀
    formatted_date = date_obj.strftime(f"%b {day}{suffix} %Y")

    return formatted_date

def format_timestamp_two(ts):
    # 尝试将字符串转换为datetime对象，首先使用包含微秒的格式
    try:
        date_obj = datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        # 如果上述转换失败，尝试不包含微秒的格式
        date_obj = datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")

    # 获取日并确定正确的后缀
    day = date_obj.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    # 使用strftime格式化月份和年份，手动处理日和后缀
    formatted_date = date_obj.strftime(f"%b {day}{suffix} %Y")

    return formatted_date
@app.get("/query/inception/{item_id}")
async def read_inception(item_id: str):
    unique_id = str(uuid.uuid1())
    file_path = f"./Output/{unique_id}-output.csv"

    try:
        automation.automate(uuid=unique_id, ric_value=item_id)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not generated.")

        df = pd.read_csv(file_path)
        if "Timestamp" not in df.columns:
            raise HTTPException(status_code=404, detail="Timestamp not found in file.")

        timestamp_value = df["Timestamp"].iloc[0]
        formatted_timestamp = format_timestamp(timestamp_value)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
    return JSONResponse(content={"Timestamp": formatted_timestamp})

@app.get("/query/summarydate/{item_id}")
async def read_inception(item_id: str):
    unique_id = str(uuid.uuid1())
    file_path = f"./Output/{unique_id}-output.csv"

    try:
        automation.automate(uuid=unique_id, ric_value=item_id)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not generated.")

        df = pd.read_csv(file_path)
        if "Date" not in df.columns:
            raise HTTPException(status_code=404, detail="NewsDate not found in file.")

        timestamp_value = df["Date"].iloc[0]
        formatted_timestamp = format_timestamp_two(timestamp_value)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
    return JSONResponse(content={"Date": formatted_timestamp})

@app.get("/query/summary/{item_id}")
async def read_summary(item_id: str):
    unique_id = str(uuid.uuid1())
    file_path = f"./Output/{unique_id}-output.csv"

    try:
        # 假设automation函数根据unique_id和item_id生成CSV文件
        automation.automate(uuid=unique_id, ric_value=item_id)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not generated.")

        # 读取CSV文件
        df = pd.read_csv(file_path)
        if "Summary" not in df.columns:
            raise HTTPException(status_code=404, detail="Summary column not found in file.")

        # 假设我们只关心第一行的Summary数据
        summary_str = df["Summary"].iloc[0]
        # 解析Summary列的字符串值为JSON
        summary_json = json.loads(summary_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 删除文件
        if os.path.exists(file_path):
            os.remove(file_path)

    # 以JSON格式返回Summary数据
    return JSONResponse(content={"Summary": summary_json})



@app.get("/split/{item_id}")
def split_sum(item_id:str):
    splited = split_summary.split_summary(item_id).split('\n-')
    return splited




