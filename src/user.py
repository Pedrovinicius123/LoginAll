from sqlalchemy import declarative_base, Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__="user"
    id = Column(Integer, primary_key=True)
    plataform = Column(String)
    password = Column(String)
