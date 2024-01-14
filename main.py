from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, user
from app.database import Base, engine
from pydantic import BaseModel
from typing import List
import hashlib
import app.auth.auth_handler


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
