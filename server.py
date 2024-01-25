import os
import uuid

from fastapi import FastAPI
from fastapi.responses import FileResponse

import automation
from LLM_integration import split_summary

app = FastAPI()


class FileResponseDeleteAfter(FileResponse):
    def __init__(self, path: str, *args, **kwargs):
        super().__init__(path, *args, **kwargs)
        self.file_path = path

    async def __call__(self, scope, receive, send):
        await super().__call__(scope, receive, send)
        if os.path.exists(self.file_path):
            os.remove(self.file_path)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/query/{item_id}")
def read_item(item_id: str):
    i = str(uuid.uuid1())
    automation.automate(uuid=i, ric_value=item_id)
    file_path = i + "-output.csv"
    return FileResponseDeleteAfter(path=file_path,
                                   filename="result.csv",
                                   media_type='text/csv')

@app.get("/split/{item_id}")
def split_sum(item_id:str):
    splited = split_summary.split_summary(item_id).split('\n-')
    return splited




