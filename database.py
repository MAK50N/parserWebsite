from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import exists


base = declarative_base()


class New(base):
    __tablename__ = "news"
    id = Column(Integer(), primary_key=True)
    time = Column(String(), nullable=False)
    title = Column(String(), nullable=False)
    text = Column(String(), nullable=False)


class Database:
    def __init__(self):
        self.DATABASE_URI = f"postgresql://postgres:1@localhost:5432/news"
        self.engine = create_engine(self.DATABASE_URI, echo=True)


    def create_database(self):
        if database_exists(self.DATABASE_URI) is False:
            create_database(self.DATABASE_URI)
        base.metadata.drop_all(self.engine)
        base.metadata.create_all(self.engine)

    def append(self, news_list):
        self.create_database()
        Session = sessionmaker(bind=self.engine)
        session = Session()
        for new in news_list:
            if session.query(exists().where(New.title == new.title)).scalar() is False:
                session.add(new)
        session.commit()
        session.close()

    def get(self, id_new):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        result = session.query(New).filter(New.id == id_new).first()
        session.close()
        return result
