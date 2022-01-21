# Copyright (C) 2021 Vladyslav Synytsyn
"""This module contains a class representation of the 'chat' table in DB."""

from datetime import datetime

from sqlalchemy import Column, String, TIMESTAMP, BigInteger, BOOLEAN
from sqlalchemy.orm import relationship

from sql import Base


class Chat(Base):
    __tablename__ = 'chat'

    chat_id = Column(BigInteger, primary_key=True, nullable=False, unique=True)
    name = Column(String, nullable=False)
    notify = Column(BOOLEAN, nullable=False, default=True)
    silent_mode = Column(BOOLEAN, nullable=False, default=False)
    language = Column(String, nullable=False, default="en")

    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())

    queue_ids = relationship(
        "Queue",
        back_populates='chat',
        cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return f"Chat(chat_id={self.chat_id}, name='{self.name}', " \
               f"queue_ids={str(self.queue_ids)}, notify={self.notify})"
