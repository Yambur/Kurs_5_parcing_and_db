from src.config import config
from src.dbmanager import DBManager

params = config()
db = DBManager(db_name='db_name', **params)