"""This module contains a class representation of the 'chat' table in DB."""

from datetime import datetime

from sqlalchemy import Column, String, TIMESTAMP, BigInteger
from sqlalchemy.orm import relationship

from sql import Base


class Chat(Base):
    __tablename__ = 'chat'

    chat_id = Column(BigInteger, primary_key=True, nullable=False, unique=True)
    name = Column(String, nullable=False)

    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())

    queue_ids = relationship(
        "Queue",
        back_populates='chat',
        cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return f"Chat(chat_id={self.chat_id}, name='{self.name}', queue_ids={str(self.queue_ids)})"
