import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func, Date, Enum, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role(enum.Enum):
    admin: str = 'admin'
    moderator: str = 'moderator'
    user: str = 'user'


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    roles = Column('role', Enum(Role), default=Role.user)
    confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


photo_m2m_tag = Table(
    "photo_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("photo_id", Integer, ForeignKey("photos.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True, index=True)
    photo_url = Column(String())
    description = Column(Text)
    user_id = Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    update = Column(Boolean, default=False)
    tags = relationship("Tag", secondary=photo_m2m_tag, backref="photos")
    user = relationship("User", backref="photos")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(25), unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))

    user = relationship('User', backref="tags")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    comment_text = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    photo_id = Column(Integer, ForeignKey(Photo.id, ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey(User.id))

    user = relationship('User', backref="comments")
    photo = relationship('Photo', backref="comments")


class UpdatePhoto(Base):
    __tablename__ = 'update_photo'

    id = Column(Integer, primary_key=True)
    photo_url = Column(String, nullable=False)
    photo_id = Column(Integer, ForeignKey(Photo.id, ondelete="CASCADE"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    update_photo = relationship('Photo', backref="update_photo")


class RatePhoto(Base):
    __tablename__ = 'rates_photos'

    id = Column(Integer, primary_key=True)
    rate = Column("rate", Integer, default=0)
    photo_id = Column(Integer, ForeignKey(Photo.id, ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    photo = relationship('Photo', backref="rates_photos")
    user = relationship('User', backref="rates_photos")




