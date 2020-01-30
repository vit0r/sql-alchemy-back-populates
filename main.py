from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import sqlite, postgresql
from pathlib import Path

# sqlite.INTEGER change to postgresql.UUID

engine = create_engine("sqlite:///database.db", convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)
    init_db()


class Parent(Base):
    __tablename__ = "parent"
    id = Column(sqlite.INTEGER, primary_key=True)
    child = relationship("Child", uselist=False, back_populates="parent")

    def __repr__(self):
        return f"{self.__tablename__}_id_{self.id}_parent_id_{self.parent_id}"

class Child(Base):
    __tablename__ = "child"
    id = Column(sqlite.INTEGER, primary_key=True)
    parent_id = Column(sqlite.INTEGER, ForeignKey("parent.id"))
    parent = relationship("Parent", back_populates="child")

    def __repr__(self):
        return f"{self.__tablename__}_id_{self.id}_parent_id_{self.parent_id}"

if Path("database.db").exists():
    r = db_session.query(Child).filter(Child.parent_id == Parent.id).all()
    print(r)
else:
    init_db()