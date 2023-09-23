from ..dataBase.DataBase import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    created_at= Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
class todo(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True,nullable=False)
    task = Column(String,nullable=False)
    owner_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    
