# Створення бази даних.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os


load_dotenv()


database = create_engine(os.getenv('DATABASE'))


Session = sessionmaker(bind=database)
session = Session()



Base = declarative_base()

def create_db():
    Base.metadata.create_all(database)


def drop_db():
    Base.metadata.drop_all(database)