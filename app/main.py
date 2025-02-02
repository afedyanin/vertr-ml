from fastapi import FastAPI, Depends

from app.controllers.prediction import prediction_router

app = FastAPI()
app.include_router(prediction_router, prefix="/prediction")

@app.get('/index')
def index():
    return {
            'project_name': 'project name',
            'webmaster': 'anfemail@gmail.com',
            'created': '2025-02-02'
            }

