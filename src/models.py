from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="author")
    comments: Mapped[list["Comments"]] = relationship(back_populates="author")
    following: Mapped[list["Followers"]] = relationship(
        "followers", foreign_keys=["followers.follower_id"], back_populates="follower")
    followers_list: Mapped[list["Followers"]] = relationship(
        "followers", foreign_keys=["followers.followed_id"], back_populates="followers")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    publicacion: Mapped[str] = mapped_column(String(120), nullable=False)
    descripcion: Mapped[str] = mapped_column(nullable=False)
    fecha: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    author: Mapped["User"] = relationship(back_populates="posts")
    shares: Mapped[list["PostShares"]] = relationship(back_populates="post")
    comments: Mapped[list["Comments"]] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "publicacion": self.publicacion,
            "descripcion": self.descripcion,
            "fecha": self.fecha,
            "author_id": self.author_id,
        }


class Comments(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    texto: Mapped[str] = mapped_column(String(120), nullable=False)
    fecha: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "texto": self.texto,
            "fecha": self.fecha,
            "author_id": self.author_id,
            "post_id": self.post_id,
        }


class Followers(db.Model):
    __tablename__ = "follower"
    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[str] = mapped_column(nullable=False)

    follower_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    followed_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    follower: Mapped["User"] = relationship(
        "User", foreign_keys=[follower_id], back_populates="following")
    followed: Mapped["User"] = relationship(
        "User", foreign_keys=[followed_id], back_populates="followers_list")

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "followed_id": self.followed_id,
            "fecha": self.fecha,
        }


class PostShares(db.Model):
    __tablename__ = "post_share"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    receiver_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    fecha: Mapped[str] = mapped_column(nullable=False)

    sender: Mapped["User"] = relationship(
        "User", foreign_keys=[sender_id]
    )
    receiver: Mapped["User"] = relationship(
        "User", foreign_keys=[receiver_id]
    )
    post: Mapped["Post"] = relationship(back_populates="shares")

    def serialize(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "post_id": self.post_id,
            "fecha": self.fecha,
        }
