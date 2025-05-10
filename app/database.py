from databases import Database
from sqlalchemy import MetaData, create_engine

DATABASE_URL = "postgresql://avitect:avitectpass@db:5432/avitectdb"

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)
