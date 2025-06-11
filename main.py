from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from routes.user_routes import router as user_router
from routes.karno_routes import router as karno_router
from modules.database_module import db
from modules.auth_module import get_current_user
import uvicorn
import os

app = FastAPI()

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(user_router)
app.include_router(karno_router)

@app.on_event("startup")
async def startup():
    await db.create_pool()

@app.get("/")
async def root(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id and await db.get_session(session_id):
        return RedirectResponse("/karno")
    return RedirectResponse("/login")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
