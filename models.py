# models.py
from sqlalchemy import Column, Integer, String, Text, Float
from db import Base

class ResumeReview(Base):
    __tablename__ = 'resume_reviews'
    id = Column(Integer, primary_key=True)
    resume_text = Column(Text, nullable=False)
    role = Column(String(100), nullable=False)
    score = Column(Float, nullable=False)
    explanation = Column(Text, nullable=False)
    filename = Column(String(120))

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    must_have = Column(Text, nullable=False)
    nice_to_have = Column(Text, nullable=False)
