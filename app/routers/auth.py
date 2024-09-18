from fastapi import APIRouter, HTTPException, status, Depends
from database import db_dependency
from models import User
from utils import verify_pw
from oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


@router.post("/login")
async def login(db: db_dependency, user_info: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.email == user_info.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )
    if not verify_pw(user_info.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    # create token
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
