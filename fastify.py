# main.py

import uvicorn
from fastapi import FastAPI
import time
app = FastAPI()


@app.get("/")
async def read_root():
    return {"msg": "time is done"}




if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)