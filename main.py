from fastapi import FastAPI

# application / services
import Services.SchedulerService as sch


app = FastAPI()

@app.on_event("startup")
def run_scheduler():
    schedule_service = sch.Scheduler()
    schedule_service.start()

@app.get("/")
async def root():
    return {"message": "Hello World"}


