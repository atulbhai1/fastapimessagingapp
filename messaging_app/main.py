from fastapi import FastAPI
from .config import settings
#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time
from . import models
from .database import engine, get_db
from .router import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]
#models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'], allow_headers=["*"],)
#for raw sql↓
"""while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='173955',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected")
        break
    except Exception as error:
        print('Failed')
        print(error)
        time.sleep(2)"""
#put "uvicorn messaging_app.main:app --reload" in terminal(remove "")
#uvicorn is the needed package
#main is the file name
#messaging_app is the variable name
# --reload tells it to automatically reload
# put it ONLY in the terminal for THIS venv

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
@app.get("/")
def root():
    return {"message": "Hello Guys!!!"}

# go to /docs for documentation!!!

