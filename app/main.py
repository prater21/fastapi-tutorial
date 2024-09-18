from fastapi import FastAPI
import models
from database import engine
from routers import post, user, auth, like

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)
