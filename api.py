from parser import Parser
from database import Database
import uvicorn as uv
import schedule
from fastapi import FastAPI

api = FastAPI()
database = Database()
parser = Parser()

def update():
    parser.get()
    database.append(parser.info)

@api.get("/")
async def root():
    return {"Enter /{id_new} to get new"}

@api.get("/{id_new}")
async def get(id_new: int):
    return database.get(id_new)


if __name__ == '__main__':
    update()

    uv.run(
        "api:api",
        host='localhost',
        port=8000,
        reload=True
    )

    schedule.every().hour.do(update())
    while True:
        schedule.run_pending()
