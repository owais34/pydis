# from resp.serializer import Serializer

# print(Serializer().serialize({"list":["this","is","a","list"],"number":12445455}))
from typing import Annotated
from uuid import uuid4
from pydantic import BaseModel
from fastapi import FastAPI,Header,Response,status,Request
from src.resp.deserializer import Deserializer
from src.resp.serializer import Serializer
import json
import os

app = FastAPI()

token_dict = {}

password_server = "password"

class AuthItem(BaseModel):
    password: str

@app.post("/")
async def handle_commnds(request: Request):
    bytes_form = await request.body()
    deserialized = Deserializer().deserialize(bytes_form.decode("utf-8"))
    print(deserialized)
    return Serializer().serialize(deserialized)

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

