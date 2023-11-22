import uuid

from fastapi import FastAPI
from fastapi.responses import FileResponse

import automation

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/query/{item_id}")
def read_item(item_id: str):
    i = str(uuid.uuid1())
    automation.automate(uuid=i, ric_value=item_id)
    file_path = i + "-output.csv"
    return FileResponse(path=file_path,
                        filename="result.csv",
                        media_type='text/csv')
