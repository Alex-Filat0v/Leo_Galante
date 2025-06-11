from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from modules.karno_module import minimize_sop, minimize_pos, generate_kmap_indices
from fastapi.responses import RedirectResponse
from modules.database_module import db


templates = Jinja2Templates(directory="templates")
karno_router = APIRouter()

karno_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@karno_router.get("/karno", response_class=HTMLResponse)
async def karno_page(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id and await db.get_session(session_id):
        return templates.TemplateResponse("main.html", {"request": request})
    return RedirectResponse("/login")


@karno_router.post("/karno/minimize")
async def minimize_karno(
    method: str = Form(...),
    variables: str = Form(...),
    values: str = Form(...)
):
    # Преобразование входных данных
    vars_list = variables.split(",")  # ["A", "B", "C", "D"]
    values_list = [int(x) for x in values.split(",")]  # [1,0,1,...]
    bits = generate_kmap_indices()

    if method == "SOP":
        result = minimize_sop(bits, values_list, vars_list)
    else:
        result = minimize_pos(bits, values_list, vars_list)

    return JSONResponse({"result": result})
