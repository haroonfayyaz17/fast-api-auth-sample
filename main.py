from fastapi import FastAPI
from app.routers import auth, user
from app.database import Base, engine
from pydantic import BaseModel
from typing import List
import hashlib
import app.auth.auth_handler


app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)

print('app: ', app)

@app.on_event("startup")
def startup():
    print('startup')
    Base.metadata.create_all(engine)

# @app.on_event("shutdown")
# def shutdown():
#     print('shutdown')
#     for tbl in reversed(Base.metadata.sorted_tables):
#         # print('tbl: ', tbl)
#         tbl.drop(engine)
