from sqlalchemy import Column, Integer, String, Float
from app.database.database import Base


class UserData(Base):
    __tablename__ = "user_data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    item = Column(String)
    price = Column(Float)


class AdminData(Base):
    __tablename__ = "admin_data"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    status = Column(String)
    name = Column(String, index=True)
    email = Column(String, index=True)