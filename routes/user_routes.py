from fastapi import APIRouter, Request, Form, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from modules.database_module import db
from modules.auth_module import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("auth.html", {
        "request": request,
        "mode": "register",
        "message": request.query_params.get("message")
    })


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("auth.html", {
        "request": request,
        "mode": "login",
        "error": request.query_params.get("error"),
        "message": request.query_params.get("message")
    })


@router.post("/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    success = await db.create_user(username, password)
    if not success:
        # Возвращаем ту же страницу с сообщением об ошибке
        return templates.TemplateResponse("auth.html", {
            "request": request,
            "mode": "register",
            "error": "username_exists"
        }, status_code=400)
    return RedirectResponse("/login?message=registration_success", status_code=303)


@router.post("/login")
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    if not await db.verify_user(username, password):
        return RedirectResponse("/login?error=invalid_credentials", status_code=303)

    user = await db.get_user(username)
    session_id = await db.create_session(user['id'])

    response = RedirectResponse("/karno", status_code=303)
    response.set_cookie(key="session_id", value=str(session_id), httponly=True)
    return response


@router.get("/logout")
async def logout(response: Response):
    response = RedirectResponse("/login")
    response.delete_cookie(key="session_id")
    return response


@router.get("/change-password", response_class=HTMLResponse)
async def change_password_page(request: Request, session: dict = Depends(get_current_user)):
    return templates.TemplateResponse("change_password.html", {
        "request": request,
        "error": request.query_params.get("error")
    })


@router.post("/change-password")
async def change_password(
        request: Request,
        current_password: str = Form(...),
        new_password: str = Form(...),
        session: dict = Depends(get_current_user)
):
    user = await db.get_user(session['username'])
    if not await db.verify_user(user['username'], current_password):
        return RedirectResponse("/change-password?error=wrong_password", status_code=303)

    await db.change_password(user['username'], new_password)
    return RedirectResponse("/karno?message=password_changed", status_code=303)


@router.get("/change-password", response_class=HTMLResponse)
async def change_password_page(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("change_password.html", {
        "request": request,
        "error": request.query_params.get("error"),
        "username": user['username']  # Добавляем имя пользователя в контекст
    })


@router.post("/change-password")
async def change_password(
        request: Request,
        current_password: str = Form(...),
        new_password: str = Form(...),
        user: dict = Depends(get_current_user)
):
    if not await db.verify_user(user['username'], current_password):
        return RedirectResponse("/change-password?error=wrong_password", status_code=303)

    await db.change_password(user['username'], new_password)
    return RedirectResponse("/karno?message=password_changed", status_code=303)
