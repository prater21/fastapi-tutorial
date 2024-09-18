from fastapi import APIRouter, status, HTTPException, Path
from models import Like, User, Post
from oauth2 import user_dependency
from database import db_dependency
from utils import hash_pw
from schemas import LikeBase

router = APIRouter(prefix="/like", tags=["Like"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def like(user: user_dependency, db: db_dependency, like_info: LikeBase):

    post = db.query(Post).filter(Post.id == like_info.post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND POST"
        )

    duplicate = db.query(Like).filter(
        Like.user_id == user.id, Like.post_id == like_info.post_id
    )

    duplicate_vote = duplicate.first()
    if like_info.flag == True:
        if duplicate_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {user.id} has alredy voted on post {like_info.post_id}",
            )

        new_like = Like(post_id=like_info.post_id, user_id=user.id)
        db.add(new_like)
        db.commit()
        return {"message": "successfully liked"}

    else:
        if not duplicate_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="like does not exist"
            )
        duplicate.delete()
        db.commit()
        return {"message": "successfully unliked"}
