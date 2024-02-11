from fastapi import FastAPI
from resources import add_run

app = FastAPI()


@app.get("/healthcheck")
async def root():
    # need to add some health checks here
    return {"your app is working :)"}


@app.post("/runs")
async def root(week: int, day: int, details: str):
    """
    Add planned runs.
    """
    add_run(week, day, details)


@app.get("/runs")
async def root():
    """
    View all runs.
    """
