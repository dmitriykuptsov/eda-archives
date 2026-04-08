from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    secret = Column(String(512))
    date = Column(String(50))
    name = Column(String(100))
    email = Column(String(50))
    location = Column(String(100))
    image_path = Column(String(1024))
    pdf_path = Column(String(1024))
    status = Column(String(50)) 