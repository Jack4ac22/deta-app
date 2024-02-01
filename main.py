from features.books.book_router import router as book_router
from features.quizzes.quiz_router import router as quiz_router
from features.security.auth import router as auth_router
from features.users.user_router import router as user_router
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import certifi
# from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
import os
from bson import ObjectId

app = FastAPI()

try:
    mongoURL = os.getenv('NEXT_PUBLIC_ATLAS_URI')
    client = MongoClient(mongoURL)
    app.database = client["bibleDataSet"]
except Exception as e:
    print(f"An error occurred: {e}")

# @asynccontextmanager
# async def lifespan(app):
#     # create mongo connection
#     app.mongodb_client = AsyncIOMotorClient(os.getenv('NEXT_PUBLIC_ATLAS_URI'), tlsCAFile=certifi.where())
#     app.database = client["mydatabase"]
#     yield
#     # close mongo connection
#     app.mongodb_client.close()


# app = FastAPI(lifespan=lifespan)


# @app.on_event("startup")
# def startup_db_client():
#     app.mongodb_client = MongoClient(os.getenv('NEXT_PUBLIC_ATLAS_URI'), tlsCAFile=certifi.where())
#     app.database = app.mongodb_client["bibleDataSet"]


# @app.on_event("shutdown")
# def shutdown_db_client():
#     app.mongodb_client.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def healthchecker():
    return {"status": "success", "message": "The API is up and running"}


@app.get("/test")
def testfunc(request: Request):
    users = list(request.app.database["users"].find(limit=100))
    for user in users:
        if isinstance(user['_id'], ObjectId):
            str_id = str(user['_id'])
            user['_id'] = str_id
    return users


app.include_router(auth_router, prefix="")
# app.include_router(book_router, tags=["books"], prefix="/book")
app.include_router(user_router, tags=["users"], prefix="/users")
app.include_router(quiz_router, tags=["quiz"], prefix="/quiz")
