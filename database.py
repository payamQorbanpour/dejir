from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///dejirbot.db', echo=True)
Base = declarative_base()

class MessageModel(Base):

    __tablename__ = "message"
    
    id = Column(Integer, primary_key=True)
    message = Column(String)
    label = Column(String)
    user_id = Column(String)
    is_approved = Column(Boolean)
    date = Column(Date)

    def __init__(self):
        self.date = datetime.utcnow()

Base.metadata.create_all(engine)
