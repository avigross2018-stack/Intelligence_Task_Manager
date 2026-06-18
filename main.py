from fastapi import FastAPI, HTTPException, status
import uvicorn
from routes import agent_routes
from routes import mission_routes
from routes import report_routes


app = FastAPI()

app.include_router(agent_routes.router)
app.include_router(mission_routes.router)
app.include_router(report_routes.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)