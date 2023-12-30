import asyncio
import uvicorn
import datetime
from fastapi import FastAPI, Request
from sse_starlette import EventSourceResponse

app = FastAPI()

STREAM_DELAY = 1  # second

@app.get("/sse")
async def message_stream(request: Request):
    def new_messages():
        # Add logic here to check for new messages
        yield 'Hello World'
    async def event_generator():
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            # Checks for new messages and return them to client if any
            if new_messages():
                yield {"data": str(datetime.datetime.now())}

            await asyncio.sleep(STREAM_DELAY)
    return EventSourceResponse(event_generator())

@app.get("/")
async def root():
    return {"message": "Hello World"}

