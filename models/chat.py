from sqlalchemy import Column, Integer, text, TEXT, ForeignKey, String, Null
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP
import uuid

from core.db import Base


class Chat(Base):
    __tablename__ = "chat"
    chat_id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    post_id = Column(Integer, ForeignKey("post.post_id"), nullable=False)
    room_id = Column(Integer, nullable=False)
    sender_id = Column(Integer, ForeignKey("account.account_id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("account.account_id"), nullable=False)
    sender_account = relationship("Account", foreign_keys=[sender_id])
    receiver_account = relationship("Account", foreign_keys=[receiver_id])
    is_photo = Column(TINYINT, default=0)
    chat_str = Column(TEXT)
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )
    mysql_engine = "InnoDB"


class Room(Base):
    __tablename__ = "room"
    room_id = Column(String, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    post_id = Column(Integer, ForeignKey("post.post_id"), nullable=False)
    rooms_of_seller = relationship("Post", foreign_keys=[post_id], backref="chat_rooms")
    buyer_id = Column(Integer, ForeignKey("account.account_id"), nullable=False)
    rooms_of_buyer = relationship("Account", foreign_keys=[buyer_id], backref="chat_rooms")
    status = Column(TINYINT, default=Null, comment="Null: 모두 읽기 가능, user_id: 해당 user_id 만 읽을 수 있음, -1: 아무도 못읽음")
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )
    mysql_engine = "InnoDB"


class Message(Base):
    __tablename__ = "message"
    message_id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    room_id = Column(String, ForeignKey("room.room_id"), nullable=False)
    is_from_buyer = Column(TINYINT, nullable=False)
    content = Column(String, nullable=False)
    read = Column(TINYINT, default=0)
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    mysql_engine = "InnoDB"