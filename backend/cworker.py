from celery import Celery

app = Celery("tasks", broker="pyamqp://user:user@rabbitmq:5672//")


@app.task
def reminder(description: str):
    print("Time to run! Today's run is " + description)
