import asyncio
from websockets.server import serve
import sys
from time import time
from src.resp.serializer import Serializer
from src.pydis import Pydis
from src.datastore.persist import STORAGE_SERVICE
from src.datastore.logger import LOGGER_SERVICE

pydisapp = Pydis()


async def echo(websocket):
    async for message in websocket:
        now = time()
        output = pydisapp.process_json(message.encode("utf-8"))
        then = time()
        await websocket.send(output)
        
        print("%20fms" %((then-now)*1000))

async def main():
    async with serve(echo, "localhost", 8765, max_size=2**25):
            
        await asyncio.Future()  # run forever

try:
    asyncio.run(main())
except KeyboardInterrupt:
    STORAGE_SERVICE.stop()
    LOGGER_SERVICE.stop()
    sys.exit(0)