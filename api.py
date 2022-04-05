from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

db = []

class Message(BaseModel):
    msg_id: int
    name: str
    age: int
    message: str
    createDate: datetime

@app.get("/messages/")
def get_data():
    return db


@app.get("/messages/{message_id}")
def get_data(message_id: int):
    return next(
        (db[message_id - 1] for msg in db if msg["msg_id"] == message_id), "message not found"
    )


@app.post("/message/")
def post_data(message: Message):
    new_msg = message.dict()
    if new_msg["msg_id"] == 0: new_msg["msg_id"] = 1
    for msg in db:
        if msg["msg_id"] in [0, msg["msg_id"]]:
            new_msg["msg_id"] = db[len(db) - 1]["msg_id"] + 1
    db.append(new_msg)
    return db


@app.put("/messages/{message_id}/update/")
def update_data(message_id: int, message: Message):
    update_msg = message.dict()
    if message_id <= 0 or message_id > len(db):
        return {"error": "no message with such id"}
    if update_msg["msg_id"] != message_id:
        return {"error": "message id does not match editted message"}
    for msg in db:
        if msg["msg_id"] in (message_id, update_msg["msg_id"]):
            db.remove(msg)
    db.insert((message_id - 1), update_msg)
    return db[message_id - 1]


@app.delete("/delete/{message_id}")
def delete_data(message_id: int):
    if message_id <= 0 or message_id > len(db):
        return {"error": "no message with such id"}
    for msg in db:
        if msg["msg_id"] == message_id:
            db.remove(msg)
    return db