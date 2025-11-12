import uvicorn
from fastapi import FastAPI, Depends

from app.controllers.prediction import prediction_router
from app.controllers.stats_forecast import stats_forecast_router

app = FastAPI()
#app.include_router(prediction_router, prefix="/prediction")
app.include_router(stats_forecast_router, prefix="/stats-forecast")


@app.get('/index')
def index():
    return {
        'project_name': 'vertr-ml',
        'webmaster': 'anfemail@gmail.com',
        'created': '2025-02-02'
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8081, reload=True)
