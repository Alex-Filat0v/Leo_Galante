from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from modules.database_module import db

security = HTTPBearer()


async def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail="Not authenticated",
            headers={"Location": "/login"},
        )

    session = await db.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail="Invalid session",
            headers={"Location": "/login"},
        )

    # Получаем полные данные пользователя
    user = await db.get_user_by_id(session['user_id'])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail="User not found",
            headers={"Location": "/login"},
        )

    return user
