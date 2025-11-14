import uvicorn
from fastapi import FastAPI

from app.controllers.ml_forecast import ml_forecast_router
from app.controllers.stats_forecast import stats_forecast_router

app = FastAPI()
app.include_router(stats_forecast_router, prefix="/stats-forecast")

app.include_router(ml_forecast_router, prefix="/ml-forecast")
@app.get('/index')
def index():
    return {
        'project_name': 'vertr-ml',
        'webmaster': 'anfemail@gmail.com',
        'created': '2025-02-02'
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8081, reload=True)
