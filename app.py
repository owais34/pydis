

from typing import Annotated
from uuid import uuid4
from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi import FastAPI,Header,Response,status,Request
from src.resp.deserializer import Deserializer
from src.resp.serializer import Serializer
from src.datastore.globaldata import GlobalDataStore
from src.datastore.persist import RUN_STORAGE_SERVICE
import json
import os

token_dict = {}

GLOBAL_DATA_STORE = GlobalDataStore()

password_server = "password"



class AuthItem(BaseModel):
    password: str

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield
    global RUN_STORAGE_SERVICE
    RUN_STORAGE_SERVICE = False


app = FastAPI(lifespan=lifespan)


@app.post("/")
async def handle_commnds(request: Request):
    bytes_form = await request.body()
    #deserialized = Deserializer().deserialize(bytes_form.decode("utf-8"))
    deserialized = bytes_form.decode("utf-8").split(" ")
    return GLOBAL_DATA_STORE.process_command(deserialized)

@app.post("/serialize")
async def handleSerialize(request: Request):
    form =  await request.body()
    serialized = Serializer().serialize(json.loads(form))
    if os.path.exists("demofile2.txt"):
        os.remove("demofile2.txt")
    f = open("demofile2.txt", "ab")
    bytess= bytes(serialized,"utf-8")
    f.write(bytess)
    f.close()
    return "+OK\r\n"

@app.post("/deserialize")
async def handleDeserialize(request: Request):
    bytes_form = await request.body()
    deserialized = Deserializer().deserialize(bytes_form.decode("utf-8"))
    return deserialized

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

