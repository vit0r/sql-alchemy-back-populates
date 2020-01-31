from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import sqlite, postgresql
from pathlib import Path
from uuid import uuid4

engine = create_engine(
    "postgresql://postgres:mysecretpassword@localhost/postgres", convert_unicode=True
)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as ex:
        print(ex)

    try:
        for r in range(1, 101):
            u = str(uuid4())
            p = Parent(id=u, name=f"Parents{u}")
            db_session.add(p)
            uc = str(uuid4())
            c = Child(id=uc, name=f"Child{uc}", parent_id=u)
            db_session.add(c)
            print(f"insert register {r}")
        db_session.commit()
    except Exception as ex:
        print(ex)
        db_session.rollback()
    finally:
        print("databse filled")


class Parent(Base):
    __tablename__ = "parent"
    id = Column(postgresql.UUID, primary_key=True)
    name = Column(postgresql.TEXT)
    child = relationship("Child", uselist=False, back_populates="parent")

    def __repr__(self):
        return f"\n{self.__tablename__}_id_{self.id}_parent_id_{self.parent_id}\n"


class Child(Base):
    __tablename__ = "child"
    id = Column(postgresql.UUID, primary_key=True)
    name = Column(postgresql.TEXT)
    parent_id = Column(postgresql.UUID, ForeignKey("parent.id"))
    parent = relationship("Parent", back_populates="child")

    def __repr__(self):
        return f"\n{self.__tablename__}_id_{self.id}_parent_id_{self.parent_id}\n"


def one_to_one():
    dataset = db_session.query(Child).filter(Child.parent_id == Parent.id)
    first_data = dataset.first()
    print("first register: ", first_data)
    all_data = dataset.all()
    print("all registers: ", all_data)


one_to_one()
