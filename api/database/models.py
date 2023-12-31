import enum

from sqlalchemy import Column, Integer, String, func, ForeignKey, Boolean,Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()


class RoleNames(enum.Enum):
    admin: str = 'admin'
    moderator: str = 'moderator'
    user: str = 'user'

    @staticmethod
    def get_max_role_len():
        return len(max(list(RoleNames.__members__), key=lambda item: len(item)))


# class Role(Base):
#     __tablename__ = "roles"
#     id = Column(Integer, primary_key=True)
#     name = Column(String(RoleNames.get_max_role_len()), default=RoleNames.user)
#     can_post_own_pict = Column(Boolean, default=True)
#     can_del_own_pict = Column(Boolean, default=True)
#     can_mod_own_pict = Column(Boolean, default=True)
#
#     can_post_own_comment = Column(Boolean, default=True)
#     can_mod_own_comment = Column(Boolean, default=True)
#     can_del_own_comment = Column(Boolean, default=False)
#
#     can_post_tag = Column(Boolean, default=True)
#     can_mod_tag = Column(Boolean, default=False)
#     can_del_tag = Column(Boolean, default=False)
#
#     can_post_not_own_pict = Column(Boolean, default=False)
#     can_mod_not_own_pict = Column(Boolean, default=False)
#     can_del_not_own_pict = Column(Boolean, default=False)
#
#     can_post_not_own_comment = Column(Boolean, default=False)
#     can_mod_not_own_comment = Column(Boolean, default=False)
#     can_del_not_own_comment = Column(Boolean, default=False)

#    base_role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)


# TODO: 'user' role is the base one, 'moderator' and 'admin' should be based on 'user' but with laveraged privileges
# @event.listens_for(Role.base_role_id, 'set')
# def base_role_validation(target, value, oldvalue, initiator):
#     return value if target.id != value else None


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    # role_id = Column(Integer, ForeignKey(Role.id, ondelete="CASCADE"))
    confirmed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    slug = Column(String(255), unique=True, nullable=False)
    avatar = Column(String(1024), nullable=True)
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


picture_m2m_tag = Table(
    "picture_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("picture_id", Integer, ForeignKey("pictures.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Picture(Base):
    __tablename__ = "pictures"
    id = Column(Integer, primary_key=True, index=True)
    picture_url = Column(String(1024))
    description = Column(String(10000))
    user_id = Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    update = Column(Boolean, default=False)
    tags = relationship("Tag", secondary=picture_m2m_tag, backref="pictures")
    user = relationship("User", backref="pictures")


class TransformedPicture(Base):
    __tablename__ = 'transformed_pictures'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    picture_id = Column(Integer, ForeignKey(Picture.id, ondelete="CASCADE"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    picture = relationship('Picture', backref="transformed_pictures")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    text = Column(String(10000))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    picture_id = Column(Integer, ForeignKey(Picture.id, ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship('User', backref="comments")
    picture = relationship('Picture', backref="comments")

