import asyncio
from websockets.server import serve
import json
from time import time
from src.resp.serializer import Serializer

async def echo(websocket):
    async for message in websocket:
        now = time()
        serialized = Serializer().serialize(json.loads(message))
        await websocket.send(serialized)
        then = time()
        print(str(int((then-now)*100))+"ms")

async def main():
    async with serve(echo, "localhost", 8765, max_size=2**25):
            
        await asyncio.Future()  # run forever

asyncio.run(main())