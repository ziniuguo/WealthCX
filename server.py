import os
import uuid
import datetime
import refinitiv.data as rd
import pandas as pd
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse

import automation
from LLM_integration import split_summary
import asset_mp
import asset_mp_refined
import event_mp
import asset_merge
from apscheduler.schedulers.background import BackgroundScheduler
import json

from LLM_integration.get_chat_response import get_chat_response
from TestDataSourceAPI.test_refinitiv import generate_and_save_chart,ref_market_signal
import logging


# Configure logging
logging.basicConfig(filename='scheduled_task.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')
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
    asset_merge.asset_merge()

# 使用scheduler装饰器来设置定时任务，每天晚上3点执行on_startup函数
@scheduler.scheduled_job("cron", hour=3)
def scheduled_task():
    try:
        on_startup()
        logging.info("Scheduled task executed successfully.")
    except Exception as e:
        logging.error(f"Scheduled task failed: {e}")

@app.on_event("startup")
async def startup_event():
    # on_startup()
    scheduler.start()
    os.environ["RD_LIB_CONFIG_PATH"] = "./Configuration"
    rd.open_session()
    pass


# 在应用关闭时结束 RDP 会话
@app.on_event("shutdown")
async def shutdown_event():
    rd.close_session()

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


def remove_file(path: str):
    if os.path.exists(path):
        os.remove(path)

@app.get("/query/pic/{item_id}")
async def read_item(item_id: str, background_tasks: BackgroundTasks):
    # Generate a new UUID
    chart_uuid = str(uuid.uuid4())


    try:
        chart_path = generate_and_save_chart(uuid=chart_uuid, item_id=item_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    background_tasks.add_task(remove_file, chart_path)
    return FileResponse(path=chart_path, filename=f"{chart_uuid}.png", media_type='image/png')

@app.get("/query/current-price/{item_id}")
async def read_current_price(item_id: str):
    unique_id = str(uuid.uuid1())
    file_path = f"./Output/{unique_id}-output.csv"

    try:
        automation.automate(uuid=unique_id, ric_value=item_id)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not generated.")
        df = pd.read_csv(file_path)
        if "TRDPRC_1" not in df.columns:
            raise HTTPException(status_code=404, detail="TRDPRC_1 not found in file.")
        trdprc_1_value = df["TRDPRC_1"].iloc[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
    return JSONResponse(content={"TRDPRC_1": trdprc_1_value})

@app.get("/query/target-price/{item_id}")
async def read_current_price(item_id: str):
    unique_id = str(uuid.uuid1())
    file_path = f"./Output/{unique_id}-output.csv"

    try:
        automation.automate(uuid=unique_id, ric_value=item_id)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not generated.")

        df = pd.read_csv(file_path)
        if "BID" not in df.columns:
            raise HTTPException(status_code=404, detail="BID not found in file.")

        bid_value = df["BID"].iloc[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    return JSONResponse(content={"BID": bid_value})



def format_timestamp(ts):
    try:
        # Try parsing the input string as a timestamp
        date_obj = datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        try:
            # If parsing as timestamp fails, try parsing as pure date
            date_obj = datetime.datetime.strptime(ts, "%Y-%m-%d")
        except ValueError:
            # If both parsing attempts fail, return None
            return None

    day = date_obj.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    formatted_date = date_obj.strftime(f"%b {day}{suffix} %Y")

    return formatted_date

def format_timestamp_two(ts):
    try:
        date_obj = datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        date_obj = datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")

    day = date_obj.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

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

        try:
            timestamp_value = df["Timestamp"].iloc[0]
        except KeyError as ke:
            print("no timestamp found, using Date.1")
            timestamp_value = df["Date.1"].iloc[0]
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
        automation.automate(uuid=unique_id, ric_value=item_id)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not generated.")

        df = pd.read_csv(file_path)
        if "Summary" not in df.columns:
            raise HTTPException(status_code=404, detail="Summary column not found in file.")

        summary_str = df["Summary"].iloc[0]
        summary_json = json.loads(summary_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    return JSONResponse(content={"Summary": summary_json})



@app.get("/split/{item_id}")
def split_sum(item_id:str):
    splited = split_summary.split_summary(item_id).split('\n-')
    return splited

@app.get("/query/all/{item_id}")
async def read_current_price(item_id: str):
    unique_id = str(uuid.uuid1())
    file_path = f"./Output/{unique_id}-output.csv"

    try:
        automation.automate(uuid=unique_id, ric_value=item_id)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not generated.")

        df = pd.read_csv(file_path)
        if "BID" not in df.columns:
            raise HTTPException(status_code=404, detail="BID not found in file.")
        if "Summary" not in df.columns:
            raise HTTPException(status_code=404, detail="Summary column not found in file.")

        bid_value = df["BID"].iloc[0]
        trdprc_1_value = df["TRDPRC_1"].iloc[0]
        try:
            inception = df["Timestamp"].iloc[0]
        except KeyError as ke:
            print("The df has no field timestamp. Use Date.1 instead")
            inception = df["Date.1"].iloc[0]
        formatted_timestamp = format_timestamp(inception)
        summary_str = df["Summary"].iloc[0]
        summary_json = json.loads(summary_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
    return JSONResponse(content={"BID": bid_value,"TRDPRC_1":trdprc_1_value,"Date": formatted_timestamp,"Summary": summary_json})

@app.post("/chat_bot")
async def chat_bot(request: Request):
    try:
        # Receive and parse JSON payload from the request body
        body = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    output = get_chat_response(body)
    return output

@app.post("/signal")
async def market_signal(item_id:str):
    try:
        signal_json = await ref_market_signal(item_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return signal_json