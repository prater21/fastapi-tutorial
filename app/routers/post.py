from fastapi import APIRouter, Path, HTTPException, status
from sqlalchemy import func
from database import db_dependency
from models import Like, Post, User
from schemas import CreatePost, ResponsePost, ResponsePosts
from typing import List, Optional
from oauth2 import user_dependency

router = APIRouter(prefix="/post", tags=["Posts"])


@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[ResponsePosts])
async def get_posts(
    user: user_dependency,
    db: db_dependency,
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = "",
):

    posts = (
        db.query(Post, func.count(Like.post_id).label("like_cnt"))
        .join(Like, Like.post_id == Post.id, isouter=True)
        .group_by(Post.id)
        .filter(Post.title.contains(search))
        .offset(offset)
        .limit(limit)
        # .all()
    )
    print(posts)
    # return posts
    ret = [
        {
            "post": post,
            "like": like,  # Handle null users (no match in User table)
        }
        for post, like in posts
    ]

    return ret


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponsePost)
async def get_post_by_id(
    user: user_dependency,
    db: db_dependency,
    id: int = Path(gt=0),
):
    post = db.query(Post).filter(Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found ID"
        )
    return post


# title: str content: str
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponsePost)
async def create_post(user: user_dependency, db: db_dependency, new_post: CreatePost):
    # print(post.model_dump())
    new_post = Post(**new_post.model_dump(), user_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.post("/{id}", status_code=status.HTTP_201_CREATED, response_model=ResponsePost)
async def update_post(
    user: user_dependency,
    db: db_dependency,
    update_post: CreatePost,
    id: int = Path(gt=0),
):
    # print(post.model_dump())
    post = db.query(Post).filter(Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found ID"
        )

    if user.id != post.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post.title = update_post.title
    post.content = update_post.content
    post.published = update_post.published

    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{id}", response_model=ResponsePost)
def delete_post(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Found ID {id}"
        )
    if user.id != post.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.delete()
    db.commit()

    return post
