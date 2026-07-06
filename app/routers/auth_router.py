from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db

from app.schemas.user_schema import UserRegister

from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
        request: UserRegister,
        db: Session = Depends(get_db)
):

    return AuthService.register(
        db,
        request
    )


@router.post("/login")
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):

    return AuthService.login(
        db,
        form_data.username,   # email
        form_data.password
    )