from typing import Annotated
from uuid import uuid4
from pydantic import BaseModel
from time import time
from contextlib import asynccontextmanager
from fastapi import FastAPI,Header,Response,status,Request
from src.datastore.persist import STORAGE_SERVICE
from src.datastore.logger import LOGGER_SERVICE
from src.pydis import Pydis

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
    op=pydisapp.process_serialized(bytes_form)
    return op

@app.post("/json")
async def handle_commands_json(request: Request):
    
    json_form = await request.body()
    op=pydisapp.process_json(json_form)
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



