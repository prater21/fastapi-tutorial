from fastapi import APIRouter, status, HTTPException, Path
from models import User
from database import db_dependency
from schemas import CreateUser, ResponseUser
from utils import hash_pw

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency):
    users = db.query(User).all()
    return users


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency, id: int = Path(gt=0)):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND ID"
        )
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseUser)
async def create_user(db: db_dependency, user: CreateUser):
    duplicate = db.query(User).filter(User.email == user.email).first()
    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="duplicate eamil"
        )

    # hash password
    user.password = hash_pw(user.password)

    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
