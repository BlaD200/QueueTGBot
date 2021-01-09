"""This module contains a class representation of the 'queue' and 'queue_members' tables in DB."""

from datetime import datetime

from sqlalchemy import Column, Integer, TIMESTAMP, VARCHAR, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship

from sql import Base


class Queue(Base):
    __tablename__ = 'queue'

    queue_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    notify = Column(BOOLEAN, nullable=False, default=True)

    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())

    chat_id = Column(Integer, ForeignKey('chat.chat_id'))
    chat = relationship(
        'Chat',
        back_populates='queue_ids',
        lazy=True
    )
    members = relationship('QueueMembers')

    def __repr__(self):
        return f"Queue(id={self.queue_id}, name='{self.name}', created_at={self.created_at}, notify={self.notify})"


class QueueMembers(Base):
    __tablename__ = 'queue_members'

    user_id = Column(Integer, nullable=False, primary_key=True)
    user_order = Column(Integer, nullable=False)
    current_order = Column(Integer, nullable=False, default=0)

    queue_id = Column(Integer, ForeignKey('queue.queue_id', ondelete='CASCADE'), primary_key=True)

    def __repr__(self) -> str:
        return f'QueueMembers(queue_id={self.queue_id}, ' \
               f'user_id={self.user_id}, user_order={self.user_order}, current_order={self.current_order})'
