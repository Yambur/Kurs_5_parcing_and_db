from src.config import config
from src.dbmanager import DBManager
from src.hh_api import HH_vacancy

params = config()
db = DBManager(params)
db.create_db()
db.create_tables()
hh = HH_vacancy()
company_vacancies = hh.get_vacancies()
# [{company: name, url_vacancies: url, vacancies: [{vacancy: name, url: url_vacancy, salary: salary},{},{}]},{},{}]
for company in company_vacancies:
    db.insert_data(company)
