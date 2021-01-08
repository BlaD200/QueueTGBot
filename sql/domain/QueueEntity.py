from sqlalchemy import Column, Integer, TIMESTAMP, VARCHAR, BOOLEAN, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Queue(Base):
    __tablename__ = 'queue'

    queue_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, nullable=False)
    name = Column(VARCHAR(255), nullable=False)
    notify = Column(BOOLEAN, nullable=False, default=True)

    chat = relationship(
        'ChatQueues',
        back_populates='queue_ids'
    )
    members = relationship('QueueMembers')

    def __repr__(self):
        return f"Queue(id={self.queue_id}, name={self.name}, created_at={self.created_at}, notify={self.notify}"


class ChatQueues(Base):
    __tablename__ = 'chat_queues'

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    chat_id = Column(Integer, nullable=False)

    queue_ids = relationship(
        "Queue",
        back_populates='chat',
        cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        ...


class QueueMembers(Base):
    __tablename__ = 'queue_members'

    user_id = Column(Integer, nullable=False, primary_key=True)
    user_order = Column(Integer, nullable=False)
    current_order = Column(Integer, nullable=False, default=0)

    queue_id = Column(Integer, ForeignKey('queue.queue_id', ondelete='CASCADE'), primary_key=True)

    def __repr__(self) -> str:
        return super().__repr__()
