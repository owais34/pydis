

from typing import Annotated
from uuid import uuid4
from pydantic import BaseModel
from time import time,time_ns
from contextlib import asynccontextmanager
from fastapi import FastAPI,Header,Response,status,Request
from src.resp.deserializer import Deserializer
from src.resp.serializer import Serializer
from src.datastore.persist import STORAGE_SERVICE
from src.datastore.logger import LOGGER_SERVICE
from src.pydis import Pydis
import json
import os

token_dict = {}

# uvicorn app:app --reload     

password_server = "password"

class AuthItem(BaseModel):
    password: str

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield
    STORAGE_SERVICE.stop()
    LOGGER_SERVICE.stop()


app = FastAPI(lifespan=lifespan)
pydisapp = Pydis()

@app.post("/resp")
async def handle_commands_resp(request: Request):
    
    bytes_form = await request.body()
    timenow = time()
    op=pydisapp.process_serialized(bytes_form)
    timethen=time()
    print("time to serve resp :"+str((timethen-timenow)*1000)+"ms")
    return op

@app.post("/json")
async def handle_commands_json(request: Request):
    
    json_form = await request.body()
    timenow = time()
    op=pydisapp.process_json(json_form)
    timethen=time()
    print("time to serve json :"+str((timethen-timenow)*1000)+"ms")
    return op

@app.get("/")
def get_hello():
    return "Hello "


@app.post("/authorize")
def authorize(X_Forwarded_For: Annotated[list[str] | None, Header()] = None,authItem: AuthItem = None, response: Response = None):
    if authItem.password == password_server:
        source_ip = X_Forwarded_For[0]
        token = uuid4()
        token_dict[token]=source_ip
        return {"token": token}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message":"Wrong credentials"}



