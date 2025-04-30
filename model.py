from sqlalchemy import Column, Integer, String, Date
from db import Base

class Biodata(Base):
    __tablename__ = "biodata"
    
    id = Column(Integer, primary_key=True, index=True)
    fname = Column(String)
    lname = Column(String)
    address = Column(String)
    dob = Column(Date)
    phone = Column(String)
    email = Column(String)
    gender = Column(String)
    photo = Column(String)
    hobbies = Column(String)
