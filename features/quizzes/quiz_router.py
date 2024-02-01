from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Depends, Query


router = APIRouter()


@router.get("/quiztest")
def test():
    return {"message": "hello world"}
