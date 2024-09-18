from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP, func
from database import Base
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    published = Column(Boolean, default=True)
    reg_time = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship("User", back_populates="post")
    like = relationship("Like", back_populates="post")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    reg_time = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    post = relationship("Post", back_populates="user")


class Like(Base):
    __tablename__ = "likes"

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
    )

    post = relationship("Post", back_populates="like")
