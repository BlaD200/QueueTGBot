"""This module contains a class representation of the 'queue' and 'queue_members' tables in DB."""

from datetime import datetime

from sqlalchemy import Column, Integer, TIMESTAMP, VARCHAR, BOOLEAN, ForeignKey, String, BigInteger
from sqlalchemy.orm import relationship

from sql import Base


class Queue(Base):
    __tablename__ = 'queue'

    queue_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    current_order = Column(Integer, nullable=False, default=0)
    notify = Column(BOOLEAN, nullable=False, default=True)
    message_id_to_edit = Column(Integer)

    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())

    chat_id = Column(BigInteger, ForeignKey('chat.chat_id'))
    chat = relationship(
        'Chat',
        back_populates='queue_ids',
        lazy=True
    )
    members = relationship('QueueMember',
                           cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"Queue(id={self.queue_id}, name='{self.name}', current_order={self.current_order}, " \
               f"created_at={self.created_at}, notify={self.notify}, message_id={self.message_id_to_edit})"


class QueueMember(Base):
    __tablename__ = 'queue_member'

    user_id = Column(BigInteger, nullable=False, primary_key=True)
    user_order = Column(Integer, nullable=False)
    fullname = Column(String, nullable=False)

    queue_id = Column(Integer, ForeignKey('queue.queue_id', ondelete='CASCADE'), primary_key=True)

    def __repr__(self) -> str:
        return f'QueueMember(queue_id={self.queue_id}, ' \
               f'user_id={self.user_id}, user_order={self.user_order}, fullname={self.fullname})'

    def __eq__(self, other):
        if type(other) is QueueMember:
            return self.queue_id == other.queue_id and self.user_id == other.user_id
        else:
            return False
