from fastapi import FastAPI
from fastapi import Body,Response
import uvicorn
import tpcl_maker as tpcl
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os

from enum import Enum
from typing import Union

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static",html=True), name="static")

@app.get("/test")
async def page_test():
    with open("static/test-tpcl.html",encoding="utf-8") as f:
        page = f.read()
    return Response(content=page,media_type="text/html")


@app.get("/tpclmaker")
async def get_maketpcl():
    return {"message": "Hello tpcl World"}

@app.get("/tpclmaker/{jsonc_file}",response_class=HTMLResponse)
async def maketpcl_file(jsonc_file):
        conf = tpcl.read_jsonc_file(jsonc_file+".jsonc")
        ret = tpcl.tpcl_maker(conf)
        if ret:
            with open('tpcl_send.log','r',encoding='utf-8') as f:
                response = f.read()
                return f"<pre>{response}</pre>"

@app.post("/tpclmaker")
async def post_maketpcl(body=Body(...)):
    ret = tpcl.tpcl_maker(body)
    if ret:
        with open('tpcl_send.log','r',encoding='utf-8') as f:
            response = f.read()
            return {"data":response}
    return {}

@app.post("/tpclmaker/status")
async def get_status_post(body=Body(...)):
        data =  tpcl.analize_status(body)
        return data

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == '__main__':
    # コンソールで [$ uvicorn run:app --reload]でも可
    uvicorn.run("main:app",port=5020,reload=True,host="0.0.0.0")