from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from modules.karno_module import KarnoMap
from modules.auth_module import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/karno", response_class=HTMLResponse)
async def karno_page(request: Request, _: dict = Depends(get_current_user)):
    return templates.TemplateResponse("main.html", {
        "request": request,
        "variables": ["A", "B", "C"],
        "simplification_type": "sop",
        "cell_values": [
            [0, 0, 0, 0],
            [0, 1, 0, 0]
        ]
    })


@router.post("/simplify", response_class=HTMLResponse)
async def simplify(
        request: Request,
        variables: str = Form(...),
        simplification_type: str = Form(...),
        cell_0_0: str = Form(...),
        cell_0_1: str = Form(...),
        cell_0_2: str = Form(...),
        cell_0_3: str = Form(...),
        cell_1_0: str = Form(...),
        cell_1_1: str = Form(...),
        cell_1_2: str = Form(...),
        cell_1_3: str = Form(...),
        _: dict = Depends(get_current_user)
):
    try:
        var_list = [v.strip() for v in variables.split(",") if v.strip()]
        cell_values = [
            [int(cell_0_0), int(cell_0_1), int(cell_0_2), int(cell_0_3)],
            [int(cell_1_0), int(cell_1_1), int(cell_1_2), int(cell_1_3)]
        ]

        result = KarnoMap.simplify(var_list, cell_values, simplification_type)

        return templates.TemplateResponse("main.html", {
            "request": request,
            "variables": var_list,
            "simplification_type": simplification_type,
            "cell_values": cell_values,
            "result": result
        })
    except Exception as e:
        return templates.TemplateResponse("main.html", {
            "request": request,
            "error": str(e),
            "variables": variables.split(","),
            "simplification_type": simplification_type,
            "cell_values": [
                [int(cell_0_0), int(cell_0_1), int(cell_0_2), int(cell_0_3)],
                [int(cell_1_0), int(cell_1_1), int(cell_1_2), int(cell_1_3)]
            ]
        })
